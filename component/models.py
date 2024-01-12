from django.db import models
from canvas.models import Canvas

class Component(models.Model):
    COMPONENT_TYPE_CHOICES = [
        ('Background', 'Background'),
        ('Sticker', 'Sticker'),
        ('Text', 'Text')
    ]
    COMPONENT_SOURCE_CHOICES = [
        ('Upload', 'Upload'),
        ('AI', 'AI')
    ]

    canvas_id = models.ForeignKey(Canvas, on_delete=models.CASCADE)
    component_type = models.CharField(max_length=20, choices=COMPONENT_TYPE_CHOICES)
    component_source = models.CharField(max_length=20, choices=COMPONENT_SOURCE_CHOICES)
    component_url = models.CharField(max_length=500)
    position_x = models.FloatField()
    position_y = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.canvas.id} - {self.component_type}"