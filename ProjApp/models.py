
from turtle import ondrag
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField

# Create your models here.

class Topic(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150,unique=True)
    class Meta:
        ordering = ['title']
        
    def __str__(self) -> str:
        return self.title
class Category(models.Model):
    user = models.ForeignKey(User, related_name='topic_created', on_delete=models.CASCADE)
    subject = models.ForeignKey(Topic, related_name='topic',on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='category_group', blank=True)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    view = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']
    def __str__(self) -> str:
        return self.title
    
class Module(models.Model):
    category = models.ForeignKey(Category, related_name='category',on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['category'])
    class Meta:
        ordering = ['order']
    def __str__(self) -> str:
        return f'{self.order}. {self.title}'

class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents',on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, \
  limit_choices_to={'model__in':('text','video','image','file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type','object_id')
    order = OrderField(blank=True,for_fields=['module'])
    class Meta:
        ordering = ['order']
    
class ItemBase(models.Model):
    user = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updaed = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
    def __str__(self) -> str:
        return self.title
    
class Text(ItemBase):
    content = models.TextField()
    
class File(ItemBase):
    file = models.FileField(upload_to='files')
    
class Image(ItemBase):
    image = models.FileField(upload_to='images')
class Video(ItemBase):
    url = models.URLField()
    