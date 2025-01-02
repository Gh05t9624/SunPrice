from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CustomUserViewSet, ProductViewSet, FactureViewSet
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'products', ProductViewSet)
router.register(r'factures', FactureViewSet, basename='facture')

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # ========== Authentification ==================
    path('', views.log_in, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.log_out, name='logout'),
    path('profil', views.profile, name='profil'),
    
    # ========== Pages Users ======================
    path('home', views.home, name='home'),
    path('boutique', views.boutique, name='boutique'),
    path('super_marcher', views.super_marcher, name='super_marcher'),
    path('superette', views.superette, name='superette'),
    path('particulier', views.particulier, name='particulier'),
    path('imobilier', views.imobilier, name='imobilier'),
    path('facture_users', views.facture_users, name='facture_users'),
    
    # ========== Pages de Notifications ======================
    path('notifications', views.notifications, name='notifications'),
    path('notifications_view', views.notifications_view, name='notifications_view'),
    path('mark-notifications-as-read', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    path('check_notifications', views.check_notifications, name='check_notifications'),
    
    # ========== Pages Admins ======================
    path('SuperAdmin', views.SuperAdmin, name='SuperAdmin'),
    
    # ========== Les Formulaires ================
    path('product', views.create_product, name='product'),
    path('facture', views.facture, name='facture'),
    
    # ========== Details ================
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('profiles/<int:user_id>', views.user_detail, name='user_detail'),
    path('toggle_follow/<int:user_id>', views.toggle_follow, name='toggle_follow'),
    path('followed-users/', views.followed_users, name='followed_users'),
    path('facture_detail/<int:id>/', views.facture_detail, name='facture_detail'),
    
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]