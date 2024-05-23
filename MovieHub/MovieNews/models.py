from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length = 18)
    user = models.CharField(max_length = 18)
    password = models.CharField(max_length = 18)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


class RssFeed(models.Model):
    channel_name = models.CharField(max_length = 30, primary_key = True)
    description = models.TextField()
    imagine = models.ImageField()
    url = models.URLField()
    users = models.ManyToManyField(User, related_name = 'rss_list', blank = True)

    def __str__(self):
        return self.channel_name


    class Meta:
        verbose_name = "rss feed"
        verbose_name_plural = "rss feed"


class News(models.Model):
    news_title = models.TextField()
    description = models.TextField()
    imagine = models.URLField
    rss_model = models.ForeignKey(RssFeed, on_delete = models.CASCADE, related_name = 'rss')   #vincolo referenziale

    def __str__(self):
        # con rss_model si ottiene la referenza al modello news, da cui è possibile accedere ai suoi campi
        return "news " + self.rss_model.channel_name


    class Meta:
        verbose_name = "news"
        verbose_name_plural = "news"