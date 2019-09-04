from django.urls import include, path
from .views import ListBooksView, ListCategoriesView
from rest_framework import routers
from apps.scraper import views

router = routers.DefaultRouter()
router.register(r'books', views.ListBooksView)
router.register(r'categories', views.ListCategoriesView)

urlpatterns = [
    path('books/', ListBooksView.as_view(), name="books-all"),
    path('categories/', ListCategoriesView.as_view(), name="categories-all")
]

