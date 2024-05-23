from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .models import User, RssFeed


# Create your views here.


def movielog(request):

    if "username" in request.session:
        del request.session["username"]

    if request.method == 'POST':
        # raccolti i dati POST
        username = request.POST.get('user')
        password = request.POST.get('password')
        # controllo se esiste lo user nel DB
        user = User.objects.filter(user=username).first()
        if user:
            # confronto la password catturata con quella del DB
            if user.password == password:
                # lo porto alla home loggata, caricando gli RSS Feed
                rss_feed = RssFeed.objects.all()
                request.session["username"] = user.user
                return redirect("home")
        # ricarico la pagina con un messaggio di errore
        else:
            return render(request, 'MovieNews/movielogin.html',
                          {'errormex': "Login fallito. Riprova."})

    return render(request, 'MovieNews/movielogin.html')

def movieregister(request):

    if "username" in request.session:
        del request.session["username"]

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
        request.session["username"] = user.user
        return redirect("home")


    return render(request, 'MovieNews/registrazione.html')



def moviehome(request):
    user_log = None
    sub_message = "Prima effettua l'accesso."

    rss_feed = RssFeed.objects.all()

    if "username" in request.session:
        user_log = request.session["username"]

        if request.method == "POST":
            url = request.POST.get("url_rss")
            channel = RssFeed.objects.get(url = url)
            user = User.objects.filter(user = user_log).first()
            if not user.rss_list.filter(url = url).exists():
                user.rss_list.add(channel)
                sub_message = "Canale aggiunto"
            else:
                sub_message = "Canale gia' presente"

    return render(request, 'MovieNews/homePage.html',
                  {'user': user_log, 'rss': rss_feed, 'mex': sub_message})



def moviepersonal(request):
    return render(request, 'MovieNews/personalNews.html')