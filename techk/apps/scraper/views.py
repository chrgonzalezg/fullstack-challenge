# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import generics
from .models import Categories, Books
from .serializers import CategoriesSerializer, BooksSerializer
from rest_framework import viewsets

# Create your views here.


class ListBooksView(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer


class ListCategoriesView(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

