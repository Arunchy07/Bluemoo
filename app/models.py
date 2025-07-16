from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.

CATEGORY_CHOICES=(
  ('CR','Curd'),
  ('ML','Milk'),
  ('LS','Lassi'),
  ('MS','Milkshake'),
  ('PN','Panner'),
  ('GH','Ghee'),
  ('CZ','Cheese'),
  ('IC','Ice-Creams'),
  
  
)

class Product(models.Model):
  title = models. CharField (max_length=100)
  selling_price = models. FloatField()
  discounted_price = models. FloatField()
  description = models. TextField()
  composition = models. TextField(default='')
  prodapp = models. TextField(default='')
  category = models. CharField(choices=CATEGORY_CHOICES, max_length=2)
  product_image = models. ImageField(upload_to='product')
  
  def _str_(self):
   return self.title
 
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
      
class Cart(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)
  
  @property
  def total_cost(self):
    return self.quantity * self.product.discounted_price