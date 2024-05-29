from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from .models import User, RssFeed
from .scraping import update_news


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
                request.session["username"] = user.user
                return redirect("home")
        # ricarico la pagina con un messaggio di errore
        else:
            return render(request, 'MovieNews/movielogin.html',
                          {'errormex': "Login fallito. Riprova."})

    return render(request, 'MovieNews/movielogin.html')

def movieregister(request):
    error = None

    if "username" in request.session:
        del request.session["username"]

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nome = request.POST.get('nome')

        user_exist = User.objects.filter(user=username).first()
        if not user_exist:
            # raccolti i dati posso creare l'utente e salvarlo in DB
            user = User.objects.create(
                name = nome,
                user = username,
                password = password
            )
            user.save()
            request.session["username"] = user.user
            return redirect("home")
        else:
            error = "Scegli un altro username. Questo è già registrato. "
    return render(request, 'MovieNews/registrazione.html', {'mex': error})



def moviehome(request):
    user_log = None
    url = None
    sub_url = None

    rss_feed = RssFeed.objects.all()

    if "username" in request.session:
        user_log = request.session["username"]
        user = User.objects.get(user = user_log)

        if request.method == "POST":
            url = request.POST.get("url_rss")
            channel = RssFeed.objects.get(url = url)
            if not channel in user.rss_list.all():
                user.rss_list.add(channel)
            else:
                user.rss_list.remove(channel)

            user.save()
        sub_url = list(user.rss_list.all())

    return render(request, 'MovieNews/homePage.html',
                  {'user': user_log, 'rss': rss_feed, 'sub_url': sub_url})



def moviepersonal(request):
    feeds = None

    if "username" not in request.session:
        return HttpResponseNotFound("Non sei autenticato per visionare contenuti privati")
    else:
        username = request.session["username"]
        user = User.objects.get(user = username)
        rss_list = user.rss_list.all()

        if not rss_list.exists():
            return HttpResponseNotFound("Non sei iscritto a nessun canale. Iscriviti per vedere le ultime notizie")
        else:
            update_news(rss_list)
            feeds = [channel.news.all() for channel in rss_list]

        return render(request, 'MovieNews/personalNews.html',
                      {'feeds': feeds, 'username': username})
