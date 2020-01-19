from django.urls import path

from . import views
app_name = 'sermonapp'

urlpatterns = [
    path('', views.view_sermon_list, name='index'),
    path('<int:sermon_id>/', views.view_sermon, name='details'),
    path('upload/', views.upload_sermon, name='upload_sermon'),
    path('<int:sermon_id>/edit/', views.edit_sermon, name='editor'),
]
