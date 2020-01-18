from django.urls import path

from . import views
app_name = 'sermonapp'

urlpatterns = [
    # ex: /polls/
    path('', views.view_sermon_list, name='index'),
    # ex: /sermon/5/
    path('<int:sermon_id>/', views.view_sermon, name='details'),
    # ex: /sermon/5/edit/
    path('<int:sermon_id>/edit/', views.edit_sermon, name='editor'),
]
