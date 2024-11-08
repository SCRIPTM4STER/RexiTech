from django.db import models
import random
import string
from django.contrib.auth.models import User


def generate_random_code(length=8):
    """
    Generates a random alphanumeric code consisting of uppercase letters and numbers.
    
    Parameters:
    length (int): The length of the code to be generated. Default is 8.
    
    Returns:
    str: A random alphanumeric code.
    """
    # Define the character set: uppercase letters and numbers
    letters = string.ascii_uppercase  # A-Z
    numbers = '12345678912'  # 1-12
    characters = letters + numbers

    random_code = ''.join(random.choice(characters) for _ in range(length))
    return random_code


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Product ID", unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Only generate a new product_id if it's not already set
        if not self.product_id:
            unique_code_generated = False
            while not unique_code_generated:
                new_code = generate_random_code()
                # Check if the code already exists in the database
                if not Product.objects.filter(product_id=new_code).exists():
                    self.product_id = new_code
                    unique_code_generated = True
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} Image"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    rating = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review of {self.product}"

    class Meta:
        ordering = ['-date']
