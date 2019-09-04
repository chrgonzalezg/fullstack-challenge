from rest_framework import serializers
from .models import Books, Categories


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ("c_id", "c_name")

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ("b_id", "b_title", "b_thumbnail", "b_price", "b_stock", "b_product_descripcion", "b_upc", "fk_c_id")