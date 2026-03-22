from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('spotify/', views.spotify_page, name='spotify'),
    path('categories/', views.categories_page, name='categories'),
    path('search/', views.search_view, name='search'),
    path('reviews/', views.reviews_page, name='reviews'),
    path('podcast/<int:pk>/', views.podcast_detail, name='podcast_detail'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    # # TEMPORARY setup URL — delete after creating superuser
    # path('setup-nkfacts-admin-2026/', views.create_superuser_view, name='create_superuser'),

]
