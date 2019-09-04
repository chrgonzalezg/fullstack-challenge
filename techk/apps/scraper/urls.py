from django.urls import include, path
from rest_framework import routers
from apps.scraper import views

router = routers.DefaultRouter()
router.register(r'categories', views.ListCategoriesView)
router.register(r'books', views.ListBooksView)

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework'))
]

