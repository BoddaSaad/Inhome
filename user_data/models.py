from django.contrib.auth.models import AbstractUser , User
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
class Cuser(AbstractUser):
    select_lan = [
        ("A", "Arabic"),
        ("E", "English"),
    ]
    username=models.CharField(max_length=400,unique=False)
    email = models.CharField(max_length=400,unique=True)
    Provides_services = models.BooleanField(default=False)
    request_services = models.BooleanField(default=True)
    phone = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    location = models.CharField(max_length=500, null=True)
    lan = models.CharField(max_length=50, choices=select_lan, default='A')
    name = models.CharField(max_length=150)
    latitude = models.CharField(max_length=250)
    longitude=models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # تغيير الحقل المطلوب هنا

    def __str__(self):
        return self.email
    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)

class Services(models.Model):
    name = models.CharField(max_length=500)
    photo = models.ImageField(upload_to=None)
    detal = models.TextField()
    name_english=models.CharField(max_length=500,null=True)
    detal_by_english=models.TextField(null=True)
    def __str__(self) -> str:
        return self.name

class Brovides_services(models.Model):
    user = models.OneToOneField(Cuser, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    pic_id = models.ImageField(upload_to=None)
    pic_id2 = models.ImageField(upload_to=None)
    personlity_pic = models.ImageField(upload_to=None)
    rating = models.FloatField(default=3)
    indebtedness=models.IntegerField(default=0)
    debt_cleared_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    
    
    
    
    def clean(self):
     
        # التحقق مما إذا كان المستخدم يقدم خدمات
        if not self.user.Provides_services:
            raise ValidationError("This user is not allowed to provide services.")

    def save(self, *args, **kwargs):
        if self.indebtedness == 0:
            self.debt_cleared_at = timezone.now()
        self.clean()
        self.indebtedness=self.indebtedness/10
        super(Brovides_services, self).save(*args, **kwargs)

    # متوسط التقييم
    def __str__(self) -> str:
        return self.user.username
    


    def update_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            self.rating = ratings.aggregate(models.Avg('rating'))['rating__avg']
            self.save()

class Rating(models.Model):
    service_provider = models.ForeignKey(Brovides_services, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(Cuser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # قيمة التقييم (1-5)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('service_provider', 'user')  # كل مستخدم يمكنه تقييم مقدم الخدمة مرة واحدة فقط
#client rating
class ClientRating(models.Model):
    client = models.ForeignKey(Cuser, on_delete=models.CASCADE, related_name="client_ratings")
    provider = models.ForeignKey(Cuser, on_delete=models.CASCADE, related_name="provider_ratings")
    rating = models.PositiveIntegerField()  # قيمة التقييم (1-5)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('client', 'provider')  # كل مقدم خدمة يمكنه تقييم العميل مرة واحدة فقط

#class Request_services(models.Model):
    #user = models.OneToOneField(Cuser, on_delete=models.CASCADE)
    #image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)

class Order_service(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    user = models.ForeignKey(Cuser, on_delete=models.CASCADE)
    type_service = models.CharField(max_length=500)
    time = models.CharField(max_length=50)
    location = models.CharField(max_length=100,null=True)
    latitude = models.CharField(max_length=250)
    longitude=models.CharField(max_length=250)
    file = models.FileField(upload_to='media/' ,null=True)
    descrtion=models.TextField()
    count = models.PositiveIntegerField(default=1)
    status_choices = [
        
        ('P', 'Pending'),
        ('offer','offer'),
        ('Complete','Complete')
        
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=100,choices=status_choices,default='p')
    
    
    
    
    def __str__(self) -> str:
        return self.type_service


class ServiceProviderOffer(models.Model):
    time_arrive=models.CharField(max_length=50)
    order = models.ForeignKey(Order_service, on_delete=models.CASCADE, related_name="offers")
    provider = models.ForeignKey(Cuser, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # تحديد سعر للخدمة
    comment = models.TextField(null=True, blank=True)  # ملاحظات إضافية من مقدم الخدمة
    created_at = models.DateTimeField(auto_now_add=True)
    status_choices = [
        
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
        ('C', 'Canceled'),
        ('Complete','Complete')
        
        
    ]
    status = models.CharField(max_length=100, choices=status_choices, default='P')
    
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['order', 'provider'], name='unique_provider_offer_per_order')
    ]
    
    def __str__(self) -> str:
        return f"عرض:{self.order.service.name}"
    


class Notfications_Broviders(models.Model):
    title = models.CharField(max_length=300)
    content = models.CharField(max_length=500)
    brovider = models.ForeignKey(Cuser, on_delete=models.CASCADE)
    title_english=models.CharField(max_length=300)
    content_english=models.CharField(max_length=500)
    id_offer=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    seen=models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.title


class notfications_client(models.Model):
    title = models.CharField(max_length=300)
    content = models.CharField(max_length=500)
    user = models.ForeignKey(Cuser, on_delete=models.CASCADE)
    title_english=models.CharField(max_length=300)
    content_english=models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    seen=models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.title


class Refused_order_from_provider(models.Model):
    provider=models.ForeignKey(Brovides_services, on_delete=models.CASCADE)
    order=models.ForeignKey(Order_service,on_delete=models.CASCADE)



class Send_offer_from_provider(models.Model):
    provider=models.ForeignKey(Brovides_services, on_delete=models.CASCADE)
    order=models.ForeignKey(Order_service,on_delete=models.CASCADE)
    