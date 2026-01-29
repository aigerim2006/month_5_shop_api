from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField() 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title
    
    def reviews_texts(self):
        return [i.text for i in self.reviews.all()]
    
    def rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(i.stars for i in reviews)/reviews.count(), 2)
        return 0
    

CHOICES = (
    (i, i) for i in range(1, 6)
)


class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=CHOICES, default=5)
    
    def __str__(self):
        return self.text


