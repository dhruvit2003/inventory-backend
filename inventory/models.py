from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    no_of_available_item = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class BuyingTransaction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='buying_transactions')
    no_of_item = models.IntegerField()
    price_of_one_piece = models.DecimalField(max_digits=10, decimal_places=2)
    total_rupees = models.DecimalField(max_digits=12, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_rupees = self.no_of_item * self.price_of_one_piece
        
        # Update available items count
        self.item.no_of_available_item += self.no_of_item
        self.item.save()
        
        super().save(*args, **kwargs)

class SellingTransaction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='selling_transactions')
    no_of_item = models.IntegerField()
    price_of_one_piece = models.DecimalField(max_digits=10, decimal_places=2)
    total_rupees = models.DecimalField(max_digits=12, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_rupees = self.no_of_item * self.price_of_one_piece
        
        # Update available items count
        if self.item.no_of_available_item >= self.no_of_item:
            self.item.no_of_available_item -= self.no_of_item
            self.item.save()
            super().save(*args, **kwargs)
        else:
            raise ValueError("Not enough items in stock")