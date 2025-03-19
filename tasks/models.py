from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class TaskModel(models.Model):
    # Constants for status choices
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_POSTPONED = 'postponed'

    STATUS_CHOICES = [
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_POSTPONED, 'Postponed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_IN_PROGRESS)
    assigned_users = models.ManyToManyField(User, related_name='tasks_assigned', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def clean(self):
        # Validate due_date to ensure it's in the future
        if self.due_date and self.due_date <= timezone.now():
            raise ValidationError({'due_date': 'Due date must be in the future.'})

    def __str__(self):
        return f'{self.title} - {self.pk}'




