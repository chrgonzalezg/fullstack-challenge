# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Categories(models.Model):
    c_id = models.IntegerField(primary_key=True)
    c_name = models.CharField(max_length=45)
    

class Books(models.Model):    
    b_id = models.IntegerField(primary_key=True)    
    b_title = models.CharField(max_length=125)
    b_thumbnail = models.CharField(max_length=125)
    b_price = models.FloatField()
    b_stock = models.IntegerField()
    b_product_descripcion = models.TextField()
    b_upc = models.CharField(max_length=16)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)