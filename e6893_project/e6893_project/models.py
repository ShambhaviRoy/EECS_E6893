from django.db import models

COLOR_CHOICES = (
    ('green','GREEN'),
    ('blue', 'BLUE'),
    ('red','RED'),
    ('orange','ORANGE'),
    ('black','BLACK'),
)

class MyModel(models.Model):
  color = models.CharField(max_length=6, choices=COLOR_CHOICES, default='green')