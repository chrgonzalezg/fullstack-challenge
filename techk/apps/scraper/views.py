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
from django.utils.html import escape
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.

URL_TO_SCRAP = 'http://books.toscrape.com/'
soup = BeautifulSoup(requests.get(URL_TO_SCRAP).text, 'html.parser')

class ListBooksView(viewsets.ModelViewSet):
    __basic_fields = ("b_id", "b_title", "b_thumbnail", "b_price", "b_stock", "b_product_descripcion", "b_upc", "categories")
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = __basic_fields
    search_fields = __basic_fields


class ListCategoriesView(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


def fetchCategory(request):    
    categoriesAdded = 0
    for a in soup.select("li a"):
        if 'catalogue/category/books/' in a.get('href'):
            c_id_fetch, c_name_fetch = re.findall('\d+', a['href'])[0], a.contents[0].strip()
            try:
                Categories.objects.create(c_id=c_id_fetch , c_name=c_name_fetch)
                categoriesAdded += 1
            except IntegrityError as e:
                continue            
    return JsonResponse({'status': str(categoriesAdded)+" categories has added"}, status=200)



def fetchBooks(request):
    
    totalPages = int((re.findall('\d+', soup.find("li", { "class" : "current" }).text ))[1])

    booksAdded = 0
    for i in range(1, totalPages+1):
        soup_books = BeautifulSoup(requests.get(URL_TO_SCRAP+"catalogue/category/books_1/page-"+str(i)+".html").text, 'html.parser')
        #soup_books = BeautifulSoup(requests.get(URL_TO_SCRAP+"catalogue/category/books_1/page-1.html").text, 'html.parser')        
        booksOfPages = [i.text for i in soup_books.findAll('article', {'class': 'product_pod'})]        
        for booksOfPages in soup_books.select("article div a"):
            urlBook = URL_TO_SCRAP+"catalogue/"+booksOfPages['href'][6:]
            soupBook = BeautifulSoup(requests.get(urlBook).text, 'html.parser')
            desc = soupBook.find('p', {'class' : False})
            data_dict = {                
                "b_id": int(re.search(r'(\d+)\D+$', urlBook).group(1)),
                "b_title": soupBook.find('h1').text,
                "b_thumbnail": URL_TO_SCRAP+soupBook.find('img')['src'][6:],
                "b_price": float(soupBook.find("p", { "class" : "price_color" }).text[2:]),
                "b_stock": int(re.findall('\d+', soupBook.find('p',{'class':'instock availability'}).text)[0]),
                "b_product_descripcion": desc.text if desc else "" ,
                "b_upc": soupBook.find('td').text,
                "categories": Categories.objects.get(c_id = re.findall('\d+', soupBook.find_all('a')[3]["href"])[0]),
            }
            try:
                Books(**data_dict).save()
                booksAdded += 1
            except IntegrityError as e:
                continue            
    return JsonResponse({'status': str(booksAdded)+" books has added"}, status=200)
