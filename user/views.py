from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import *
# Create your views here.
def userRegister(request):
    if request.method == 'POST':
        kullanici = request.POST['kullanici']
        email = request.POST['email']
        resim = request.FILES['resim']
        telefon = request.POST['telefon']
        sifre1 = request.POST['sifre1']
        sifre2 = request.POST['sifre2']

        if kullanici != '' and email != '' and sifre1 != '' and sifre2 != '':
            if sifre1 == sifre2:
                if User.objects.filter(username = kullanici).exists():
                    messages.error(request, 'Bu kullanıcı adı zaten mevcut')
                    return redirect('register')
                elif User.objects.filter(email = email).exists():
                    messages.error(request, 'Bu email kullanımda')
                    return redirect('register')
                elif len(sifre1) < 6:
                    messages.error(request, 'Şifre en az 6 karakter olmalıdır')
                    return redirect('register')
                elif kullanici in sifre1:
                    messages.error(request, 'Kullanıcı adı ile şifre benzer olmamalıdır')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username = kullanici, email = email, password = sifre1)
                    Hesap.objects.create(
                        user = user,
                        resim = resim,
                        tel = telefon
                    )
                    user.save()
                    messages.success(request, 'Kullanıcı oluşturuldu')
                    return redirect('index')
            else:
                messages.error(request, 'Şifreler uyuşmuyor')
                return redirect('register')
        else:
            messages.error(request, 'Tüm alanların doldurulması zorunludur')
            return redirect('register')
    return render(request, 'register.html')

def userLogin(request):
    if request.method == 'POST':
        kullanici = request.POST['kullanici']
        sifre = request.POST['sifre']

        user = authenticate(request, username = kullanici, password = sifre)

        if user is not None:
            login(request, user)
            messages.success(request, 'Giriş yapıldı')
            return redirect('profiles')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı')
            return redirect('login')
    return render(request, 'login.html')

def profiles(request):
    profiller = Profil.objects.filter(olusturan = request.user)
    context = {
        'profiller':profiller
    }
    return render(request, 'browse.html', context)

def olustur(request):
    form = ProfilForm()
    print(Profil.objects.filter(olusturan = request.user).count())
    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES)
        if form.is_valid():
            if Profil.objects.filter(olusturan = request.user).count() < 4:
                profil = form.save(commit = False)
                profil.olusturan = request.user
                profil.save()
                messages.success(request, 'Profil Oluşturuldu')
                return redirect('profiles')
            else:
                messages.error(request, 'En fazla 4 adet profil oluşturulabilir')
                return redirect('profiles')
    context = {
        'form':form
    }
    return render(request, 'olustur.html', context)

def hesap(request):
    profil = request.user.hesap
    context = {
        'profil':profil
    }
    return render(request, 'hesap.html', context)

def sil(request):
    user = request.user
    user.delete()
    messages.success(request, 'Kullanıcı silindi')
    return redirect('index')

def update(request):
    # forms.py'dan yaptığımız zaman
    # form = UserForm(instance = request.user)
    
    # if request.method == 'POST':
    #     form = UserForm(request.POST, instance = request.user)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Bilgiler güncellendi')
    #         return redirect('hesap')

    # Formu kendimiz oluşturduğumuz zaman
    user = request.user
    if request.method == 'POST':
        kullanici = request.POST['kullanici']
        email = request.POST['email']

        print(user.username)
        print(user.email)
        user.username = kullanici
        user.email = email
        user.save()
        messages.success(request, 'Güncellendi')
        return redirect('hesap')
    # context = {
    #     'form':form
    # }
    return render(request, 'update.html')

def userLogout(request):
    logout(request)
    messages.success(request, 'Çıkış yapıldı')
    return redirect('index')