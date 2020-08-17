from django.db import models

# Create your models here.
class Customertbl(models.Model):
    UserName=models.CharField(null=True,max_length=50)
    EmailId=models.EmailField()
    Password=models.CharField(max_length=20)
    Otp_num=models.CharField(max_length=10,default=False)
    Extra_Id=models.CharField(max_length=10,default=False)
    is_varified=models.BooleanField(default=False)
    
class Producttbl(models.Model):
    ProductName=models.CharField(null=True,max_length=50)
    Image=models.ImageField(upload_to="image/",default="image/logo.png",null=False)
    ProductPrice=models.FloatField()

class Carttbl(models.Model):
    user_to_id=models.ForeignKey(Customertbl,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Producttbl,on_delete=models.CASCADE)
    Quantity=models.IntegerField(default=1)
    Total_price=models.FloatField()

class Transactiontbl(models.Model):
    made_by = models.ForeignKey(Carttbl,on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True,max_length=100,null=True,blank=True)
    checksum = models.CharField(max_length=100,null=True,blank=True)
    
