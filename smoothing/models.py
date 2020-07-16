from django.db import models
from django.utils import timezone
import os
from uuid import uuid4
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

def path_rename(instance, filename):
    upload_to = 'images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


# Create your models here.
class Picture(models.Model):
    img = models.ImageField(upload_to=path_rename)
    def __str__(self):
        return self.img.url


@receiver(pre_delete, sender=Picture)
def delete_image(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.img:
         instance.img.delete(False)            