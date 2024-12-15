from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(
        max_length=20, choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High")]
    )
    status = models.BooleanField(default=False)  # False: Incomplete, True: Complete
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.title
