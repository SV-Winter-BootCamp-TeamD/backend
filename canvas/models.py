from django.db import models

class Canvas(models.Model):
    canvas_name = models.CharField(max_length=100)
    owner_id = models.IntegerField(default=0)
    canvas_preview_url= models.CharField(max_length=1000, default='default_preview_url')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.canvas_name

class CanvasMember(models.Model):
    canvas_id = models.ForeignKey(Canvas, on_delete=models.CASCADE, db_column='canvas_id')
    member_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)