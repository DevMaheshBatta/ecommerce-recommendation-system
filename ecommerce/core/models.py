from django.db import models
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    desc=models.TextField(max_length=500)
    phonenumber=models.IntegerField()

    def __str__(self):
      return self.name    
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50,default="")
    subcategory=models.CharField(max_length=50,default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300  )
    image = models.ImageField(upload_to='images/images')


    
    def __str__(self):
      return self.product_name
    



class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address1 = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    amount = models.IntegerField()
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return self.name


class OrderUpdate(models.Model):
   update_id =models.AutoField(primary_key=True)
   order_id= models.IntegerField(default="")
   update_desc =models.CharField(max_length=5000)
   delivered=models.BooleanField(default="False")
   timestamp =models.DateField(auto_now_add=True)
   def __str__(self):
      return self.update_desc[0:7]+ "..."  
