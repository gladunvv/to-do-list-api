from django.db import models
from django.conf import settings


class Marker(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='markers', on_delete=models.CASCADE)
    name = models.CharField('Marker name', max_length=30, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Marker'
        verbose_name_plural = 'Markers'

    def __str__(self):
        return self.name


class ToDoList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lists', on_delete=models.CASCADE)
    name = models.CharField('List name', max_length=30, unique=True)
    marker = models.ForeignKey(Marker, related_name='todo_lists', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('name',)
        verbose_name = 'List'
        verbose_name_plural = 'Lists'

    def __str__(self):
        return self.name


class Item(models.Model):
    PRIORITY_CHOICES = (
        (1, 'Low'),
        (2, 'Normal'),
        (3, 'High'),
    )
    title = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now_add=True)
    notification_date = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    complited = models.BooleanField(default=False)
    todo_list = models.ForeignKey(ToDoList, related_name='items', on_delete=models.CASCADE)

    class Meta:
        ordering =('title',)
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.title
