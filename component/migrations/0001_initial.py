# Generated by Django 5.0.1 on 2024-01-15 15:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('canvas', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component_type', models.CharField(choices=[('Background', 'Background'), ('Sticker', 'Sticker'), ('Text', 'Text')], max_length=20)),
                ('component_source', models.CharField(choices=[('Upload', 'Upload'), ('AI', 'AI')], max_length=20)),
                ('component_url', models.CharField(max_length=500)),
                ('position_x', models.FloatField()),
                ('position_y', models.FloatField()),
                ('width', models.IntegerField(default=100)),
                ('height', models.IntegerField(default=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('canvas_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='canvas.canvas')),
            ],
        ),
    ]
