from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Categorie, SousCategorie, Produit, ConfigurationSite
from .forms import CategorieForm, SousCategorieForm, ProduitForm, ConfigurationSiteForm


def is_admin(user):
    return user.is_authenticated and user.is_staff

# Vue de connexion admin
# Vue de connexion admin
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Identifiants incorrects ou accès non autorisé')
    
    return render(request, 'admin/login_.html')


# Déconnexion admin
@user_passes_test(is_admin)
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# Dashboard principal
@user_passes_test(is_admin)
def admin_dashboard(request):
    stats = {
        'total_categories': Categorie.objects.count(),
        'total_sous_categories': SousCategorie.objects.count(),
        'total_produits': Produit.objects.count(),
        'produits_en_stock': Produit.objects.filter(en_stock=True).count(),
        'produits_rupture': Produit.objects.filter(en_stock=False).count(),
    }
    
    # Derniers produits ajoutés
    derniers_produits = Produit.objects.order_by('-date_creation')[:5]
    
    # Catégories avec nombre de produits
    categories_stats = Categorie.objects.annotate(
        nb_produits=Count('sous_categories__produits')
    ).order_by('-nb_produits')[:5]
    
    context = {
        'stats': stats,
        'derniers_produits': derniers_produits,
        'categories_stats': categories_stats,
    }
    return render(request, 'admin/dashboard.html', context)


# Gestion des catégories
@user_passes_test(is_admin)
def admin_categories(request):
    categories = Categorie.objects.annotate(
        nb_sous_categories=Count('sous_categories'),
        nb_produits=Count('sous_categories__produits')
    ).order_by('nom')
    
    paginator = Paginator(categories, 10)
    page = request.GET.get('page')
    categories = paginator.get_page(page)
    
    return render(request, 'admin/categories.html', {'categories': categories})



@user_passes_test(is_admin)
def admin_categorie_create(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catégorie créée avec succès!')
            return redirect('admin_categories')
    else:
        form = CategorieForm()
    
    return render(request, 'admin/categorie_form.html', {'form': form, 'action': 'Créer'})

@user_passes_test(is_admin)
def admin_categorie_edit(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catégorie modifiée avec succès!')
            return redirect('admin_categories')
    else:
        form = CategorieForm(instance=categorie)
    
    return render(request, 'admin/categorie_form.html', {
        'form': form, 
        'action': 'Modifier',
        'categorie': categorie
    })

@user_passes_test(is_admin)
def admin_categorie_delete(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    if request.method == 'POST':
        categorie.delete()
        messages.success(request, 'Catégorie supprimée avec succès!')
        return redirect('admin_categories')
    
    return render(request, 'admin/categorie_confirm_delete.html', {'categorie': categorie})

# Gestion des sous-catégories
@user_passes_test(is_admin)
def admin_sous_categories(request):
    sous_categories = SousCategorie.objects.select_related('categorie').annotate(
        nb_produits=Count('produits')
    ).order_by('categorie__nom', 'nom')
    
    paginator = Paginator(sous_categories, 10)
    page = request.GET.get('page')
    sous_categories = paginator.get_page(page)
    
    return render(request, 'admin/sous_categories.html', {'sous_categories': sous_categories})

@user_passes_test(is_admin)
def admin_sous_categorie_create(request):
    if request.method == 'POST':
        form = SousCategorieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sous-catégorie créée avec succès!')
            return redirect('admin_sous_categories')
    else:
        form = SousCategorieForm()
    
    return render(request, 'admin/sous_categorie_form.html', {'form': form, 'action': 'Créer'})

@user_passes_test(is_admin)
def admin_sous_categorie_edit(request, pk):
    sous_categorie = get_object_or_404(SousCategorie, pk=pk)
    
    if request.method == 'POST':
        form = SousCategorieForm(request.POST, instance=sous_categorie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sous-catégorie modifiée avec succès!')
            return redirect('admin_sous_categories')
    else:
        form = SousCategorieForm(instance=sous_categorie)
    
    return render(request, 'admin/sous_categorie_form.html', {
        'form': form, 
        'action': 'Modifier',
        'sous_categorie': sous_categorie
    })

@user_passes_test(is_admin)
def admin_sous_categorie_delete(request, pk):
    sous_categorie = get_object_or_404(SousCategorie, pk=pk)
    if request.method == 'POST':
        sous_categorie.delete()
        messages.success(request, 'Sous-catégorie supprimée avec succès!')
        return redirect('admin_sous_categories')
    
    return render(request, 'admin/sous_categorie_confirm_delete.html', {'sous_categorie': sous_categorie})

# Gestion des produits
@user_passes_test(is_admin)
def admin_produits(request):
    produits = Produit.objects.select_related('sous_categorie__categorie').order_by('-date_creation')
    
    # Filtres
    search = request.GET.get('search')
    categorie_id = request.GET.get('categorie')
    en_stock = request.GET.get('en_stock')
    
    if search:
        produits = produits.filter(
            Q(nom__icontains=search) | 
            Q(description__icontains=search)
        )
    
    if categorie_id:
        produits = produits.filter(sous_categorie__categorie_id=categorie_id)
    
    if en_stock == 'true':
        produits = produits.filter(en_stock=True)
    elif en_stock == 'false':
        produits = produits.filter(en_stock=False)
    
    paginator = Paginator(produits, 12)
    page = request.GET.get('page')
    produits = paginator.get_page(page)
    
    categories = Categorie.objects.all()
    
    context = {
        'produits': produits,
        'categories': categories,
        'search': search,
        'selected_categorie': int(categorie_id) if categorie_id else None,
        'selected_stock': en_stock,
    }
    
    return render(request, 'admin/produits.html', context)

@user_passes_test(is_admin)
def admin_produit_create(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit créé avec succès!')
            return redirect('admin_produits')
    else:
        form = ProduitForm()
    
    return render(request, 'admin/produit_form.html', {'form': form, 'action': 'Créer'})

@user_passes_test(is_admin)
def admin_produit_edit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit modifié avec succès!')
            return redirect('admin_produits')
    else:
        form = ProduitForm(instance=produit)
    
    return render(request, 'admin/produit_form.html', {
        'form': form, 
        'action': 'Modifier',
        'produit': produit
    })

@user_passes_test(is_admin)
def admin_produit_delete(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        produit.delete()
        messages.success(request, 'Produit supprimé avec succès!')
        return redirect('admin_produits')
    
    return render(request, 'admin/produit_confirm_delete.html', {'produit': produit})

# Configuration du site
@user_passes_test(is_admin)
def admin_site_config(request):
    try:
        config = ConfigurationSite.objects.first()
    except ConfigurationSite.DoesNotExist:
        config = None
    
    if request.method == 'POST':
        if config:
            form = ConfigurationSiteForm(request.POST, request.FILES, instance=config)
        else:
            form = ConfigurationSiteForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuration sauvegardée avec succès!')
            return redirect('admin_site_config')
    else:
        form = ConfigurationSiteForm(instance=config)
    
    return render(request, 'admin/site_config.html', {'form': form})

# API pour les sous-catégories (AJAX)
@user_passes_test(is_admin)
def api_sous_categories(request):
    categorie_id = request.GET.get('categorie_id')
    if categorie_id:
        sous_categories = SousCategorie.objects.filter(categorie_id=categorie_id).values('id', 'nom')
        return JsonResponse(list(sous_categories), safe=False)
    return JsonResponse([], safe=False)














