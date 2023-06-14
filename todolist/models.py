from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=False)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('tasks', args=[str(self.id)])

    def set_due_date(self, user_input):
        self.created = user_input
        time_difference = timezone.now() - self.created
        self.due_date = self.created + time_difference

    def __str__(self):
        return self.title


    class Meta:
        ordering = ['complete']

def Time_period():
    return timezone.now() +timezone.timedelta(days='period')

class Task_list(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title


class Tasks (models.Model):
    Name= models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=Time_period)
    Task_list = models.ForeignKey(Task_list, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse(
            "item-update", args=[str(self.todo_list.id), str(self.id)]
        )

    def __str__(self):
        return f"{self.Name}: due {self.due_date}"

    class Meta:
        ordering = ["due_date"]