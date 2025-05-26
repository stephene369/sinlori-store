from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('categories/<int:categorie_id>/', views.sous_categories, name='sous_categories'),
    path('produits/<int:sous_categorie_id>/', views.produits, name='produits'),
    path('panier/', views.panier, name='panier'),
    path('ajouter-panier/', views.ajouter_panier, name='ajouter_panier'),
    path('supprimer-panier/<int:produit_id>/', views.supprimer_panier, name='supprimer_panier'),
    path('vider-panier/', views.vider_panier, name='vider_panier'),
    path('modifier-quantite-panier/', views.modifier_quantite_panier, name='modifier_quantite_panier'),
    path('contact/', views.contact, name='contact'),
    path('a-propos/', views.a_propos, name='a_propos'),
    
    
    
        # URLs d'administration
    path('admin-custom/', admin_views.admin_login, name='admin_login'),
    path('admin-custom/logout/', admin_views.admin_logout, name='admin_logout'),
    path('admin-custom/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    
    # Gestion des catégories
    path('admin-custom/categories/', admin_views.admin_categories, name='admin_categories'),
    path('admin-custom/categories/create/', admin_views.admin_categorie_create, name='admin_categorie_create'),
    path('admin-custom/categories/<int:pk>/edit/', admin_views.admin_categorie_edit, name='admin_categorie_edit'),
    path('admin-custom/categories/<int:pk>/delete/', admin_views.admin_categorie_delete, name='admin_categorie_delete'),
    
    # Gestion des sous-catégories
    path('admin-custom/sous-categories/', admin_views.admin_sous_categories, name='admin_sous_categories'),
    path('admin-custom/sous-categories/create/', admin_views.admin_sous_categorie_create, name='admin_sous_categorie_create'),
    path('admin-custom/sous-categories/<int:pk>/edit/', admin_views.admin_sous_categorie_edit, name='admin_sous_categorie_edit'),
    path('admin-custom/sous-categories/<int:pk>/delete/', admin_views.admin_sous_categorie_delete, name='admin_sous_categorie_delete'),
    
    # Gestion des produits
    path('admin-custom/produits/', admin_views.admin_produits, name='admin_produits'),
    path('admin-custom/produits/create/', admin_views.admin_produit_create, name='admin_produit_create'),
    path('admin-custom/produits/<int:pk>/edit/', admin_views.admin_produit_edit, name='admin_produit_edit'),
    path('admin-custom/produits/<int:pk>/delete/', admin_views.admin_produit_delete, name='admin_produit_delete'),
    
    # Configuration du site
    path('admin-custom/config/', admin_views.admin_site_config, name='admin_site_config'),
    
    # API
    path('admin-custom/api/sous-categories/', admin_views.api_sous_categories, name='api_sous_categories'),
]
