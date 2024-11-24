from django.urls import path, include

# ========== Authentification ===================
from SunApp.views import check_notifications, log_in, mark_notifications_as_read, notifications_view, register, log_out, profile

# ========== Les Pages Users =======================
from SunApp.views import home, boutique, super_marcher, superette, particulier, station_service, user_map_view, facture_users

# ========== Les Pages Notifications =======================
from SunApp.views import notifications

# ========= Les Pages Admins =======================
from SunApp.views import SuperAdmin

# ========== Les Formulaires =================
from SunApp.views import create_product, facture
# ========== Details =========================
from SunApp.views import product_detail, facture_detail
from . import views



urlpatterns = [
    # ========== Authentification ==================
    path('', log_in, name = 'login'),
    path('register', register, name = 'register'),
    path('logout', log_out, name = 'logout'),
    path('profil', profile, name = 'profil'),
    path('user-map', user_map_view, name='user_map'),
    
    
    # ========== Pages Users ======================
    path('home', home, name = 'home'),
    path('boutique', boutique, name = 'boutique'),
    path('super_marcher', super_marcher, name = 'super_marcher'),
    path('superette', superette, name = 'superette'),
    path('particulier', particulier, name = 'particulier'),
    path('station_service', station_service, name = 'station_service'),
    path('facture_users', facture_users, name = 'facture_users'),
    
    # ========== Pages de Notifications ======================
    path('notifications', notifications, name='notifications'),
    path('notifications/', notifications_view, name='notifications'),
    path('mark-notifications-as-read/', mark_notifications_as_read, name='mark_notifications_as_read'),
    path('check_notifications/', check_notifications, name='check_notifications'),
    
    # ========== Pages Admins ======================
    path('SuperAdmin', SuperAdmin, name= 'SuperAdmin'),
    
    # ========== Les Formulaires ================
    path('product', create_product, name = 'product'),
    path('facture', facture, name='facture'),
    
    # ========== Details ================
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('profiles/<int:user_id>/', views.user_detail, name='user_detail'),
    path('facture_detail/<int:id>/', facture_detail, name='facture_detail'),
]