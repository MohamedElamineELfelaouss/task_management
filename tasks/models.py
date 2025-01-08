from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError


class Task(models.Model):
    """
    Represents a task created by a user, with attributes for title, description,
    due date, priority, and status.
    """

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks"
    )  # A user can have multiple tasks
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def clean(self):
        """
        Ensure the due date is not in the past.
        """
        if self.due_date < date.today():
            raise ValidationError("Due date cannot be in the past.")

    def save(self, *args, **kwargs):
        self.clean()
        super(Task, self).save(*args, **kwargs)

    class Meta:
        ordering = ["due_date"]
