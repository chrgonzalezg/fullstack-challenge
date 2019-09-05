# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Categories, Books
from .serializers import CategoriesSerializer, BooksSerializer
from rest_framework import viewsets
from bs4 import BeautifulSoup
import requests
import re
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse

# Create your views here.


class ListBooksView(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer


class ListCategoriesView(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


def fetchCategory(request):
    soup = BeautifulSoup(requests.get('http://books.toscrape.com/index.html').text, 'html.parser')
    status = 'ok'
    for a in soup.select("li a"):
        if 'catalogue/category/books/' in a.get('href'):
            c_id_fetch, c_name_fetch = re.findall('\d+', a['href'])[0], a.contents[0].strip()
            try:
                Categories.objects.create(c_id=c_id_fetch , c_name=c_name_fetch)
            except IntegrityError as e:
                status = 'category id ' + c_id_fetch + ' already exists'
    return JsonResponse({'status': status}, status=400)

