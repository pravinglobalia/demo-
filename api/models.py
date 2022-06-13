
from django.db import models
from django.contrib.auth.models import User 
# Create your models here.
CATEGORY = (
    ('S', 'Shirt'),
    ('SP', 'Sport Wear'),
    ('OW', 'Out Wear'),
    ('el','electronics'),
    ('d','drink'),
    ('su','school',)
)

LABEL = (
    ('N', 'New'),
    ('BS', 'Best Seller')
)



class Item(models.Model):
    item_name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY, max_length=2)
    label = models.CharField(choices=LABEL, max_length=2)
    description = models.TextField()
    image = models.ImageField(upload_to="static/assetes/images")
    quantity = models.IntegerField(default=1)
    discounted_price=models.FloatField(null=True)
    

    def __str__(self) -> str:
        return str(self.id)

class Cart(models.Model):
    user  = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    total_item = models.PositiveIntegerField(default=1)
    totalamount= models.IntegerField(null=True)
    
    def __str__(self) -> str:
        return str(self.item.item_name)

class Contact(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=120)
    subject = models.CharField(max_length=120)
    message = models.TextField(max_length=120)

class OrderItem(models.Model):
    oder_item = models.ForeignKey(Item,on_delete=models.CASCADE)

class Order(models.Model):
    user = models.ForeignKey(Item,on_delete=models.CASCADE)
    # all_item = models.ManyToManyField
    oder_date= models.DateField() 

    

class OrderDetail(models.Model):

    id = models.BigAutoField(primary_key=True)
    customer_email = models.EmailField(verbose_name='Customer Email')
    product = models.ForeignKey(Cart, verbose_name='Product', on_delete=models.CASCADE, null=True)
    amount = models.IntegerField(verbose_name='Amount')
    stripe_payment_intent = models.CharField(max_length=200)
    # This field can be changed as status
    has_paid = models.BooleanField(default=False, verbose_name='Payment Status')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
