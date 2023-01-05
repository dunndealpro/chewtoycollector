from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("chewtoys/", views.chewtoys_index, name="index"),
    path("chewtoys/<int:chewtoy_id>/", views.chewtoys_detail, name="detail"),
    path("chewtoys/create/", views.ChewtoyCreate.as_view(), name="chewtoys_create"),
    path(
        "chewtoys/<int:pk>/update/",
        views.ChewtoyUpdate.as_view(),
        name="chewtoys_update",
    ),
    path(
        "chewtoys/<int:pk>/delete/",
        views.ChewtoyDelete.as_view(),
        name="chewtoys_delete",
    ),
    path(
        "chewtoys/<int:chewtoy_id>/add_cleaning/",
        views.add_cleaning,
        name="add_cleaning",
    ),
    path('chewtoys/<int:chewtoy_id>/assoc_dog/<int:dog_id>/', views.assoc_dog, name='assoc_dog'),
    path('chewtoys/<int:chewtoy_id>/unassoc_dog/<int:dog_id>/', views.unassoc_dog, name='unassoc_dog'),
    path("dogs/", views.DogList.as_view(), name="dogs_index"),
    path("dogs/<int:pk>/", views.DogDetail.as_view(), name="dogs_detail"),
    path("dogs/create/", views.DogCreate.as_view(), name="dogs_create"),
    path("dogs/<int:pk>/update/",views.DogUpdate.as_view(),name="dogs_update"),
    path("dogs/<int:pk>/delete/", views.DogDelete.as_view(), name="dogs_delete"),
    path('chewtoys/<int:chewtoy_id>/add_photo/', views.add_photo, name='add_photo'),
]
