from django.shortcuts import render

# Create your views here.


def movielog(request):
    return render(request, 'MovieNews/movielogin.html')



def movieregister(request):
    return render(request, 'MovieNews/registrazione.html')



def moviehome(request):
    return render(request, 'MovieNews/homePage.html')



def moviepersonal(request):
    return render(request, 'MovieNews/personalNews.html')