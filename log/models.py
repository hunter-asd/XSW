from django.db import models

# Create your models here.


class Explog(models.Model):

    shot = models.IntegerField(primary_key=True,null=False)
    title = models.CharField(max_length=100,null=False)
    content = models.TextField()
    author = models.CharField(max_length=40)
    edit_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return"<log:shot:{}>".format(self.shot)









































