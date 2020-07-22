from django.db import models

# Create your models here.
class Customertbl(models.Model):
    UserName=models.CharField(null=True,max_length=50)
    EmailId=models.EmailField()
    Password=models.CharField(max_length=20)
    Otp_num=models.CharField(max_length=10,default=False)
    Extra_Id=models.CharField(max_length=10,default=False)
    is_varified=models.BooleanField(default=False)
