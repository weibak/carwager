from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(blank=True, null=True)
    slug = models.SlugField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)


class Tags(models.Model):
    title = models.CharField(max_length=100)
    posts = models.ManyToManyField(News)
