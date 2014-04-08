import calendar
import datetime
import re

#import twitter
from articles.models import Article
from django.shortcuts import render

def home(request):
    # TODO: Pasar esto a un template tag
    # Datos para la pagina principal
    # Traigo de twitter los posts de lanuxlug
    user = 'lanuxlug'
    messages_to_display = 5
    #try:
    #    api = twitter.Api()
    #    statuses = api.GetUserTimeline(screen_name=user, count=messages_to_display, include_entities=True)
    #except Exception, e:
    #    statuses = []
    #    messages = []
    statuses = []
    messages = []

    for status in statuses:
        # Replaces the @username mentions with a URL
        replaced_mentions = re.sub(r'(@[^ $]+)', r'<a href="http://twitter.com/\1">\1</a>',status.text);
        # Replaces the #tag's with a URL
        replaced_hashtags = re.sub(r'(#[^ $]+)', r'<a href="http://twitter.com/#!/search?q=%23\1">\1</a>',replaced_mentions);
        # Replaces the published times with a URL
        replaced_times = (replaced_hashtags + " "+
                          "<span class='tiny-font'><a href='http://twitter.com/#!/"+
                          user+"/status/"+str(status.id)+"'>"+str(status.relative_created_at+
                          "</a></span>"))
        messages.append(replaced_times)

    # Traigo del ultimo post
    article = Article.objects.filter(status_id=2)[0]
    return render(request, 'home.html', {'featured_article': article,
        'messages':messages})


def lista(request):
    meses_anio = calendar.month_name
    meses_anio_abbr = calendar.month_abbr

    starting_year = 2003
    starting_month = 9

    current_date = datetime.datetime.now()
    finishing_year = current_date.year
    finishing_month = current_date.month

    meses = []
    for year in range(starting_year, finishing_year+1):
        st_month_iter = starting_month if year==starting_year else 1
        en_month_iter = finishing_month+1 if year==finishing_year else 13
        for month in range(st_month_iter, en_month_iter):
            meses.append((year,meses_anio[month], meses_anio_abbr[month]))
    meses.reverse()
    return render(request, 'lista.html', {'meses':meses})

