from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import *
from django.db.models import Q
from .models import *



# Create your views here.

def begen(request):
    if 'begen' in request.POST:    
        postId = request.POST['postId']
        print(postId)
        post = Post.objects.get(id = postId)
        if 'begen' in request.POST:
            if Post.objects.filter(like__in = [request.user] , id = postId).exists():
                post.like.remove(request.user)
                post.save()
            else:
                post.like.add(request.user)
                post.save() 

def yildiz(request):
    posts = Post.objects.all()
    for i in posts:
        begeni = i.like.all().count()
        yildiz = 0
        if begeni == 2:
            yildiz = 1
        elif begeni == 4:
            yildiz = 2
        elif begeni == 6:
            yildiz = 3 
        elif begeni == 8:
            yildiz = 4 
        elif begeni == 10:
            yildiz = 5
        i.yildiz = yildiz
        i.save()

def index(request):
    posts = Post.objects.all().order_by('?')
    kategoriler = Kategori.objects.all()

    if request.method == 'POST':
        begen(request)
        return redirect('anasayfa')
    
    yildiz(request)


    
    context={
            'kategoriler' :kategoriler,
            'posts' : posts 
        }

    return render(request , 'anasayfa.html' , context)

def filter(request):
    kategoriler = Kategori.objects.all()
    
    posts = ''
    try:
        minprice = request.GET['min_price']
        maxprice = request.GET['max_price']
        kategori = request.GET['kategori']
        location = request.GET['location']
        posts = Post.objects.filter(
            Q(fiyat__range = (minprice,maxprice)) &
            Q(location__contains = location ) &
            Q(kategori__isim__contains = kategori ) 
        )     
        uzunluk = len(posts)
        print(posts)
        
        if request.method == 'POST':
            begen(request)
            return redirect(f'/filter/?min_price={minprice}&max_price={maxprice}&kategori={kategori}&location={location}')
    except:
        return redirect('/')
    
    yildiz(request)

    context={
        'kategoriler' :kategoriler,
        'posts' : posts,
        'uzunluk' : uzunluk
    }
    return render(request , 'filter.html' , context)

def kategori(request,slug):
    kategoriler = Kategori.objects.all()
    kategori = Kategori.objects.get(slug = slug)
    
    posts= Post.objects.filter(kategori__slug=slug)

    if request.method == 'POST':
        begen(request)
        return redirect('kategori', slug = kategori.slug)
    yildiz(request)
    context={
            'posts' :posts,
            'kategoriler' : kategoriler
        }
    return render(request , 'kategori.html',context)

def loginregister(request):

    
    if 'üye' in request.POST:
        email = request.POST["email"]
        username = request.POST["username"]
        sifre1 = request.POST["sifre1"]
        sifre2 = request.POST["sifre2"]

        
        if sifre1 ==  sifre2 :
            if User.objects.filter(username = username).exists():
                messages.error(request,'Kullanıcı adı kullanılıyor')
                return redirect("loginregister")
            elif User.objects.filter(email = email).exists():
                messages.error(request,'Email kullanılıyor')
                return redirect("loginregister")
            elif len(sifre1) < 6 :
                messages.error(request , 'Şifre en az 6 karakter olmalıdır')
                return redirect("loginregister")
            else:
                user = User.objects.create_user(username = username , email = email , password = sifre1 )
                Profil.objects.create(
                kullanici = user ,
            )
                user.save()
                messages.success(request,'Kayıt başarı ile gerçekleşti')
                return redirect('anasayfa')
        else :
            messages.error(request,'Şifreler uyuşmuyor')
            return redirect("loginregister")

    if 'giris' in request.POST:
            username1 = request.POST['username1']
            sifre3 = request.POST['sifre3']

            user = authenticate (request , username = username1 , password = sifre3)
            if user is not None :
                login(request , user)
                messages.success(request , 'Giriş')
                return redirect('anasayfa')
                    
            else:
                messages.error(request, "Parola ya da kullanıcı adı yanlış")
                return redirect ("loginregister")

    kategoriler = Kategori.objects.all()
    context = {
        'kategoriler' :kategoriler
    }

    return render(request , 'loginregister.html' ,context)

def logout_request (request):
    logout(request)
    return redirect ('anasayfa')

def favori(request):
    begeni = Post.objects.filter(like__in = [request.user])
    uzunluk = len(begeni)
    print(uzunluk)
    if request.method == 'POST':
        begen(request)
        return redirect('favori')
    begen(request)
    context={
        'begeni' : begeni,
        'uzunluk' :uzunluk
    }
    return render(request, 'favori.html',context)

def profil(request):
    user = request.user
    posts = Post.objects.filter(evsahibi = user)
    context = {
        'posts':posts,
    }
    return render(request,'profil.html', context)

def userProfil(request , pk):
    user = User.objects.get(id = pk)
    paylas = Post.objects.filter(evsahibi = user)

    for i in paylas:
        print(i)
    context={
        'user' : user,
        'paylas':paylas,
    }
    return render(request,'userProfil.html',context)

def detay(request , postId):

    postDetay = Post.objects.get(slug = postId)
    if 'comment' in request.POST:
        yorum = request.POST['yorum']
        yorums=Yorum.objects.create(
            kullanici = request.user,
            yorum = yorum,
            post = postDetay,
        )
        yorums.save()
        messages.success(request,'Yorum yapıldı')
        return redirect('detay' , postId = postDetay.slug)
    yorumlar = Yorum.objects.filter(post = postDetay)
    if 'sil' in request.POST:
        yorumId = request.POST['userYorum']
        yorums = Yorum.objects.get(id = yorumId)
        yorums.delete()

    yildiz(request)
    
    context = {
        'postDetay' : postDetay,
        'yorumlar':yorumlar,

    }
    return render(request , 'detail.html' ,context)

def HesapSil(request,id):
    profile = User.objects.get(id = id)
    profile.delete()
    messages.success(request,'Profil silindi') 
    return render(request,'loginregister.html')

def host(request):
    return render(request , "host.html")

def postForm(request):
    kategoriler = Kategori.objects.all()

    if request.method == 'POST':
        
        evName = request.POST['evName']
        kategoriId = request.POST['kategori']
        uzaklık = request.POST['uzaklık']
        price = request.POST['price']
        info = request.POST['info']
        country = request.POST['country']
        pic1 = request.FILES['pic1']
        pic2 = request.FILES['pic2']
        pic3 = request.FILES['pic3']
        pic4 = request.FILES['pic4']
        pic5 = request.FILES['pic5']
        kategori = Kategori.objects.get(id =kategoriId)
        post = Post.objects.create( isim = evName , 
                                evsahibi = request.user,
                                kategori=kategori,
                                uzaklik = uzaklık,
                                location = country,
                                fiyat = price,
                                bilgi = info,
                                resim1 = pic1,
                                resim2 = pic2,
                                resim3 = pic3,
                                resim4 = pic4,
                                resim5 = pic5
                                           )
        
        post.save()
        messages.success(request,'Eviniz paylaşıldı')
        return redirect('anasayfa')
    context={
            'kategoriler' :kategoriler,
        }
    return render(request,'postForm.html',context)


def hesap(request):
    return render(request , 'hesap/hesap.html')

def hesapKisisel(request):
    user = request.user.profil
    form = HesapForm(instance=user)
    if request.method == 'POST':
        form = HesapForm(request.POST,request.FILES,instance = user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profil bilgileri güncellendi')
            return redirect('hesap')
    context = {
        'form':form
    }
    return render(request ,'hesap/kisisel-bilgiler.html',context)

def guvenlik(request):
    user = request.user
    if request.method == 'POST':
        eski = request.POST['eski']
        yeni1 = request.POST['yeni1']
        yeni2 = request.POST['yeni2']

        yeni = authenticate(request,username=user,password=eski)

        if yeni is not None:
            if yeni1 == yeni2:
                user.set_password(yeni1)
                user.save()
                messages.success(request,'Şifrenis değiştirildi')
                return redirect('anasayfa')
            else:
                messages.error(request,'Şifreler uyuşmuyor')
        else:
            messages.error(request,'Mevcut şifreniz hatalı')  
    return render(request ,'hesap/güvenlik.html')

def payment(request):
    return render(request,'hesap/ödeme.html')

def vergiler(request):
    return render(request,'hesap/vergiler.html')

def bildirim(request):
    return render(request,'hesap/bildirimler.html')

def gizlilik(request):
    return render(request,'hesap/gizlilik.html')

def tercihler(request):
    return render(request,'hesap/tercihler.html')

def seyehat(request):
    return render(request,'hesap/seyehat.html')

def sahiplik(request):
    return render(request,'hesap/ev-sahipliği.html')

def misafir(request):
    return render(request,'hesap/misafir.html')

def contactHost(request):
    return render(request,'contact_host.html')

def onayodeme(request):
    return render(request, 'onayodeme.html')
