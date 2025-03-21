# Generated by Django 4.2.20 on 2025-03-18 14:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0002_alter_taskmodel_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmodel',
            name='assigned_users',
            field=models.ManyToManyField(blank=True, null=True, related_name='tasks_assigned', to=settings.AUTH_USER_MODEL),
        ),
    ]
