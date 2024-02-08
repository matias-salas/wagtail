from django.db import models

class Subscribers(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"