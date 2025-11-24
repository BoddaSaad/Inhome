# Multiple File Upload Feature for Order Service

## Overview
This feature allows users to upload multiple files (images and videos) when creating an order service. The implementation maintains backward compatibility with the existing single file field.

## API Usage

### Creating an Order with Multiple Files

**Endpoint:** `POST /order_service/<service_id>/`

**Content-Type:** `multipart/form-data`

**Request Parameters:**
- `type_service` (string): Type of service
- `time` (string): Preferred time for the service
- `latitude` (string): Location latitude
- `longitude` (string): Location longitude
- `descrtion` (text): Description of the order
- `count` (integer): Quantity (default: 1)
- `files` (array of files): Multiple files to upload (NEW)
- `file` (file): Single file (legacy support, optional)

**Example using curl:**
```bash
curl -X POST "http://example.com/order_service/1/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "type_service=Plumbing" \
  -F "time=10:00 AM" \
  -F "latitude=30.0444" \
  -F "longitude=31.2357" \
  -F "descrtion=Need urgent plumbing service" \
  -F "count=1" \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg" \
  -F "files=@video1.mp4"
```

**Example using Python requests:**
```python
import requests

url = "http://example.com/order_service/1/"
headers = {
    "Authorization": "Bearer YOUR_JWT_TOKEN"
}
data = {
    "type_service": "Plumbing",
    "time": "10:00 AM",
    "latitude": "30.0444",
    "longitude": "31.2357",
    "descrtion": "Need urgent plumbing service",
    "count": 1
}
files = [
    ("files", ("image1.jpg", open("image1.jpg", "rb"), "image/jpeg")),
    ("files", ("image2.jpg", open("image2.jpg", "rb"), "image/jpeg")),
    ("files", ("video1.mp4", open("video1.mp4", "rb"), "video/mp4"))
]

response = requests.post(url, headers=headers, data=data, files=files)
print(response.json())
```

**Example using JavaScript (Fetch API):**
```javascript
const formData = new FormData();
formData.append('type_service', 'Plumbing');
formData.append('time', '10:00 AM');
formData.append('latitude', '30.0444');
formData.append('longitude', '31.2357');
formData.append('descrtion', 'Need urgent plumbing service');
formData.append('count', 1);

// Add multiple files
const fileInput = document.getElementById('fileInput');
for (let i = 0; i < fileInput.files.length; i++) {
    formData.append('files', fileInput.files[i]);
}

fetch('http://example.com/order_service/1/', {
    method: 'POST',
    headers: {
        'Authorization': 'Bearer YOUR_JWT_TOKEN'
    },
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

**Success Response:**
```json
{
    "done": "Order created successfully"
}
```

## Response Format

### Getting Order Details

When retrieving order details, the response now includes a `files` array containing all uploaded files:

**Example Response:**
```json
{
    "id": 123,
    "service": 1,
    "user": 5,
    "type_service": "Plumbing",
    "time": "10:00 AM",
    "latitude": "30.0444",
    "longitude": "31.2357",
    "descrtion": "Need urgent plumbing service",
    "count": 1,
    "status": "P",
    "created_at": "2024-11-24T01:30:00Z",
    "file": null,  // Legacy field (optional)
    "files": [
        {
            "id": 1,
            "file": "http://example.com/media/image1.jpg",
            "uploaded_at": "2024-11-24T01:30:00Z"
        },
        {
            "id": 2,
            "file": "http://example.com/media/image2.jpg",
            "uploaded_at": "2024-11-24T01:30:01Z"
        },
        {
            "id": 3,
            "file": "http://example.com/media/video1.mp4",
            "uploaded_at": "2024-11-24T01:30:02Z"
        }
    ],
    "service_name": "Plumbing Service",
    "name": "John Doe"
}
```

### Order Details in Provider View

When providers view order details (e.g., in `GET_orders` serializer), the response includes:

```json
{
    "id": 1,
    "order": 123,
    "status": "A",
    "order_details": {
        "service": "Plumbing Service",
        "user": "John Doe",
        "id_user": 5,
        "type_service": "Plumbing",
        "time": "10:00 AM",
        "location": "Cairo, Egypt",
        "file": null,  // Legacy field
        "files": [
            "http://example.com/media/image1.jpg",
            "http://example.com/media/image2.jpg",
            "http://example.com/media/video1.mp4"
        ],
        "count": 1,
        "id_order": 123,
        "phone": "1234567890",
        "latitude": "30.0444",
        "longitude": "31.2357"
    }
}
```

## Database Schema

### OrderFile Model

| Field | Type | Description |
|-------|------|-------------|
| id | BigAutoField | Primary key |
| order | ForeignKey | Reference to Order_service |
| file | FileField | The uploaded file |
| uploaded_at | DateTimeField | Timestamp when file was uploaded |

### Order_service Model Changes

- The `file` field is now optional (`blank=True`)
- New related field `files` (reverse relation from OrderFile)

## Migration

A new migration `0012_alter_order_service_file_orderfile.py` has been created:
- Alters the `file` field on `order_service` to make it optional
- Creates the new `OrderFile` model

To apply the migration:
```bash
python manage.py migrate
```

## Backward Compatibility

The implementation maintains full backward compatibility:
1. The old `file` field still exists and can be used
2. Clients not yet updated can continue using the single `file` field
3. When reading orders, both `file` and `files` are returned
4. The `files` array will include the legacy `file` if no new files are uploaded

## Testing

Run the test suite to verify the functionality:
```bash
python manage.py test user_data.tests.OrderFileTestCase
```

The test suite includes:
- Testing OrderFile model creation
- Testing orders with multiple files
- Testing serialization of orders with files

## Notes

- File uploads are stored in the `media/` directory
- Maximum number of files is not limited at the model level
- File size limits should be configured at the web server level
- Supported file types should be validated at the application level if needed
