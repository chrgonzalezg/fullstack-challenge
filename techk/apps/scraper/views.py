# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import generics
from .models import Books, Categories
from .serializers import BooksSerializer, CategoriesSerializer

# Create your views here.


class ListBooksView(generics.ListAPIView):

    queryset = Books.objects.all()
    serializer_class = BooksSerializer

class ListCategoriesView(generics.ListAPIView):

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
