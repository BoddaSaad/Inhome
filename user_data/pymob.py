import requests
import json

url = "https://accept.paymob.com/v1/intention/"

payload = json.dumps({
  "amount": 10,
  "currency": "EGP",
  "expiration": 5800,
  "payment_methods": [
    123,
    "Shopify Mobile wallet IFrame"
  ],
    # هنا ضع ال Integration ID الصحيح
  "items": [
    {
      "name": "Item name 1",
      "amount": 10,
      "description": "Watch",
      "quantity": 1
    }
  ],
  "billing_data": {
    "apartment": "6",
    "first_name": "Ammar",
    "last_name": "Sadek",
    "street": "938, Al-Jadeed Bldg",
    "building": "939",
    "phone_number": "+96824480228",
    "country": "OMN",
    "email": "AmmarSadek@gmail.com",
    "floor": "1",
    "state": "Alkhuwair"
  },
  "special_reference": "ABCDE8121",
  "customer": {
    "first_name": "Ammar",
    "last_name": "Sadek",
    "email": "AmmarSadek@gmail.com",
    "extras": {
      "re": "22"
    }
  },
  "extras": {
    "ee": 22
  }
})

headers = {
  'Authorization': 'Token egy_sk_live_14f1e3155d5eec96fbb12370ab4b63de4e5532dedc6513bb583909666929fc41',  # تأكد من استخدام ال API Token الصحيح
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
