from django.db import models


class Post (models.Model):
    title = models.CharField(max_length=100,db_index=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    film = models.ForeignKey('Film', on_delete=models.CASCADE)
    def __str__(self):
        return self.title


class Film(models.Model):
    title = models.CharField(max_length=100,db_index=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
