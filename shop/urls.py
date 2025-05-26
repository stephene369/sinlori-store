from django.urls import path
from . import views

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
]
