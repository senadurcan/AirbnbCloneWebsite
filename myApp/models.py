from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify



# Create your models here.

class Kategori(models.Model):
    isim = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    slug = models.SlugField(null=True , unique=True , db_index=True , blank=True , editable=False)

    def save(self, *args , **kwargs):
        self.slug = slugify(self.isim)
        super().save(*args , **kwargs)

    def __str__(self):
        return self.isim

class Post(models.Model):
    id = models.UUIDField(primary_key=True , db_index= True , default=uuid.uuid4 , editable=False)
    isim = models.CharField(max_length=50)
    evsahibi = models.ForeignKey(User , on_delete= models.CASCADE , null=True)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE , null=True)
    like = models.ManyToManyField(User , related_name="like")
    uzaklik = models.CharField(max_length=50)
    location = models.CharField(max_length= 150)
    yildiz = models.IntegerField(null=True)
    fiyat = models.IntegerField(null=True)
    bilgi = models.TextField(max_length=150)
    resim1 = models.FileField(upload_to='postpic/')
    resim2 = models.FileField(upload_to='postpic/')
    resim3 = models.FileField(upload_to='postpic/')
    resim4 = models.FileField(upload_to='postpic/')
    resim5 = models.FileField(upload_to='postpic/')
    slug = models.SlugField(null=True , unique=True , db_index=True , blank=True , editable=False)


    def save(self,*args, **kwargs):
        self.slug = slugify(self.isim)
        super().save(*args , **kwargs)
    
    def __str__(self):
        return self.isim
    
class Profil(models.Model):
    id = models.UUIDField(primary_key=True , db_index= True , default=uuid.uuid4 , editable=False)
    kullanici = models.OneToOneField(User, on_delete=models.CASCADE)
    isim = models.CharField(max_length=50)
    soyisim = models.CharField(max_length=50)
    telefon = models.CharField(max_length=50)
    profilresim = models.FileField(upload_to='profilpic/' ,default='profilpic/default.jpg',blank=True)
    meslek = models.CharField(max_length=50)
    slug = models.SlugField(null=True , unique= True , db_index=True , blank=True , editable=False)

    def save(self, *args , **kwargs):
        self.slug = slugify(self.id)
        super().save(*args , **kwargs)

    def __str__(self):
        return str(self.isim)
    

class Yorum(models.Model):
   post = models.ForeignKey(Post,related_name='yorum',on_delete=models.CASCADE)
   yorum = models.TextField(max_length=200,verbose_name='Yorum')
   new_date = models.DateTimeField(auto_now_add=True)
   kullanici = models.ForeignKey(User,null=True,on_delete=models.CASCADE)  

   def _str_(self):
       return self.kullanici.username    



