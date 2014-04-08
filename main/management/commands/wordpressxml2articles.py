# -*- coding: utf-8 -*-
from xml.dom import minidom
from optparse import make_option

from django.db import connection
from django.conf import settings
from django.core.management.base import BaseCommand


MESES = {'Jan':1,
        'Feb':2,
        'Mar':3,
        'Apr':4,
        'May':5,
        'Jun':6,
        'Jul':7,
        'Aug':8,
        'Sep':9,
        'Oct':10,
        'Nov':11,
        'Dec':12
        }

AUTHORS = {
        'ska':1,
        'admin':2,
        'chr':5,
        'dererk':6,
        'diegows':4,
        'karucha':3,
        'shanshi':7,
        'exos':8}

class Command(BaseCommand):
    """
        Convierte wordpressxml a articulos de django-article
    """
    help = "Convierte wordpressxml a articulos de django-article"
    args = 'xmlfile'
    option_list = BaseCommand.option_list + (
        make_option('--file',
            type='string', dest='filename',
            help='Filename a convertir'),
    )

    def handle(self, *args, **options):
        filename = options.get('filename')

        dom = minidom.parse(filename)

        blog = [] # list that will contain all posts

        categories_set = set()
        authors_set = set()

        for node in dom.getElementsByTagName('item'):
            status = node.getElementsByTagName('wp:status')[0].firstChild.data
            if status != "publish":
                continue
            post = dict()
            post["title"] = node.getElementsByTagName('title')[0].firstChild.data
            post["date"] = node.getElementsByTagName('pubDate')[0].firstChild.data
            post["author"] = node.getElementsByTagName(
                            'dc:creator')[0].firstChild.data
            post["id"] = node.getElementsByTagName('wp:post_id')[0].firstChild.data

            if node.getElementsByTagName('content:encoded')[0].firstChild != None:
                post["text"] = node.getElementsByTagName(
                                'content:encoded')[0].firstChild.data
            else:
                post["text"] = ""

            # wp:attachment_url could be use to download attachments

            # Get the categories
            tempCategories = []
            post['author_id'] = AUTHORS[post['author']]
            print post['author_id']
            for subnode in node.getElementsByTagName('category'):
                tempCategories.append(subnode.getAttribute('nicename'))
                categories_set.update(tempCategories)
            categories = [x for x in tempCategories if x != '']
            post['tags'] = " ".join([x for x in tempCategories if x != ''])
            post["categories"] = categories
            # Add post to the list of all posts
            blog.append(post)

        from articles.models import Article, Tag
        import datetime
        errors = []
        for entry in blog:
            article = Article()
            article.title = entry['title']
            article.content = entry['text']
            dia = entry['date'][4:7]
            mes = MESES[entry['date'][8:11]]
            anio = entry['date'][12:16]
            print entry['date']
            print anio
            pub_date = datetime.datetime(int(anio), mes, int(dia))
            article.publish_date = pub_date
            article.author_id = entry['author_id']
            article.author_id = entry['author_id']
            article.status_id = 2
            try:
                article.save()
            except:
                errors.append(entry['title'])
            else:
                new_tags = []
                for tag in entry['categories']:
                    ntag = Tag.objects.get_or_create(name=tag)
                    new_tags.append(ntag[0])
                    article.tags.add(*new_tags)
        print(len(errors))
        print errors
