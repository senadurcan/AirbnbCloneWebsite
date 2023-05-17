from django.contrib import admin
from .models import *

class KategoriAdmin(admin.ModelAdmin):
    list_display = ( 'isim' ,'slug',)
    readonly_fields = ('slug',)

class PostAdmin(admin.ModelAdmin):
    list_display = ( 'isim' ,'slug',)
    readonly_fields = ('slug',)

class ProfilAdmin(admin.ModelAdmin):
    list_display = ( 'kullanici' ,'slug',)
    readonly_fields = ('slug',)


# Register your models here.

admin.site.register(Kategori , KategoriAdmin)
admin.site.register(Post , PostAdmin)
admin.site.register(Profil ,ProfilAdmin ),
admin.site.register(Yorum)
