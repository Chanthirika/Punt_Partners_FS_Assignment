from django.db import models

# Example model (can be customized as needed)
class ExampleModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
