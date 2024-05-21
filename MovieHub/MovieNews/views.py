from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .models import User


# Create your views here.


def movielog(request):

    if request.method == 'POST':
        # raccolti i dati POST
        username = request.POST.get('user')
        password = request.POST.get('password')
        # controllo se esiste lo user nel DB
        user = User.objects.filter(user=username).first()
        if user:
            # confronto la password catturata con quella del DB
            if user.password == password:
                # lo porto alla home loggata
                return render(request, 'MovieNews/homePage.html', {'user': user})
        # ricarico la pagina con un messaggio di errore
        else:
            return render(request, 'MovieNews/movielogin.html',
                          {'errormex': "Login fallito. Riprova."})

    return render(request, 'MovieNews/movielogin.html')

def movieregister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nome = request.POST.get('nome')

        # raccolti i dati dal POST posso creare l'utente e salvarlo in DB
        user = User.objects.create(
            name = nome,
            user = username,
            password = password
        )
        user.save()

        return render(request, 'MovieNews/homePage.html', {'user': user})


    return render(request, 'MovieNews/registrazione.html')



def moviehome(request):
    return render(request, 'MovieNews/homePage.html', {'user': None})



def moviepersonal(request):
    return render(request, 'MovieNews/personalNews.html')