from django.db import models
import django.db.models.deletion as django_on_delete
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    publish_date = models.DateField(null=True, blank=True)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comment', on_delete=django_on_delete.CASCADE)
    text = models.CharField(max_length=500)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.post.title
