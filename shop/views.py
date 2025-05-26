from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Categorie, SousCategorie, Produit, ConfigurationSite

def get_categories_for_menu():
    """Fonction helper pour récupérer les catégories pour le menu"""
    return Categorie.objects.all()[:6]

def accueil(request):
    categories = Categorie.objects.all()
    config = ConfigurationSite.get_config()
    
    context = {
        'categories': categories,
        'site_config': config,
    }
    return render(request, 'accueil.html', context)

def sous_categories(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    sous_categories = categorie.sous_categories.all()
    
    context = {
        'categorie': categorie,
        'sous_categories': sous_categories,
    }
    return render(request, 'sous_categories.html', context)

def produits(request, sous_categorie_id):
    sous_categorie = get_object_or_404(SousCategorie, id=sous_categorie_id)
    produits = sous_categorie.produits.all()
    
    context = {
        'sous_categorie': sous_categorie,
        'produits': produits,
    }
    return render(request, 'produits.html', context)

def ajouter_panier(request):
    """
    Ajouter un produit au panier (stocké en session)
    """
    if request.method == 'POST':
        produit_id = request.POST.get('produit_id')
        quantite = int(request.POST.get('quantite', 1))
        










        try:
            produit = get_object_or_404(Produit, id=produit_id)











            
            # Vérifier si le produit est en stock
            if not produit.en_stock:
                messages.error(request, 'Ce produit n\'est plus en stock.')
                return redirect('produits', sous_categorie_id=produit.sous_categorie.id)
            
            # Récupérer ou initialiser le panier en session
            panier = request.session.get('panier', {})
            
            # Ajouter ou mettre à jour le produit dans le panier
            if str(produit_id) in panier:
                panier[str(produit_id)]['quantite'] += quantite
            else:
                panier[str(produit_id)] = {
                    'quantite': quantite,
                    'prix': float(produit.prix)
                }
            
            # Sauvegarder le panier en session
            request.session['panier'] = panier
            request.session.modified = True
            
            messages.success(request, f'{produit.nom} ajouté au panier avec succès!')
            return redirect('panier')
            
        except Produit.DoesNotExist:
            messages.error(request, 'Produit introuvable.')
            return redirect('accueil')
    
    return redirect('accueil')

def panier(request):

    """
    Vue du panier - Version simplifiée pour démonstration
    Vous devrez adapter cette logique selon votre système de panier
    """
    
    # Récupérer les items du panier depuis la session
    panier_session = request.session.get('panier', {})
    panier_items = []
    total_panier = 0
    










    # Convertir les données de session en objets utilisables
    for produit_id, item_data in panier_session.items():
        try:
            produit = Produit.objects.get(id=produit_id)
            quantite = item_data.get('quantite', 1)
            total_item = float(produit.prix) * quantite
            
            # Créer un objet-like pour le template
            item = {
                'produit_id': produit.id,
                'nom': produit.nom,
                'prix': produit.prix,
                'quantite': quantite,
                'total': total_item,
                'image': produit.image,
            }
            
            panier_items.append(item)
            total_panier += total_item
            
        except Produit.DoesNotExist:
            # Supprimer les produits qui n'existent plus
            continue
    
    # Générer l'URL WhatsApp si configuré et panier non vide
    config = ConfigurationSite.get_config()
    whatsapp_url = None
    
    if config.whatsapp and panier_items:
        # Créer le message WhatsApp avec les produits
        message = f"Bonjour ! Je souhaite commander :\n\n"
        for item in panier_items:


            message += f"- {item['nom']} x{item['quantite']} = {item['total']:.2f}€\n"
        message += f"\nTotal: {total_panier:.2f}€"
        
        # Encoder le message pour l'URL
        import urllib.parse
        message_encoded = urllib.parse.quote(message)
        numero_clean = ''.join(filter(str.isdigit, config.whatsapp))
        if not numero_clean.startswith('33'):
            numero_clean = '33' + numero_clean.lstrip('0')
        whatsapp_url = f"https://wa.me/{numero_clean}?text={message_encoded}"
    
    context = {
        'panier_items': panier_items,
        'total_panier': total_panier,
        'whatsapp_url': whatsapp_url,
        'categories': get_categories_for_menu(),
    }
    return render(request, 'panier.html', context)

def supprimer_panier(request, produit_id):
    """
    Supprimer un produit du panier
    """
    panier = request.session.get('panier', {})
    
    if str(produit_id) in panier:

        produit = get_object_or_404(Produit, id=produit_id)
        del panier[str(produit_id)]
        request.session['panier'] = panier
        request.session.modified = True

        messages.success(request, f'{produit.nom} supprimé du panier!')
    else:
        messages.error(request, 'Produit introuvable dans le panier.')
    
    return redirect('panier')

def vider_panier(request):
    """
    Vider complètement le panier
    """
    request.session['panier'] = {}
    request.session.modified = True
    messages.success(request, 'Panier vidé avec succès!')
    return redirect('panier')

def modifier_quantite_panier(request):
    """
    Modifier la quantité d'un produit dans le panier
    """
    if request.method == 'POST':
        produit_id = request.POST.get('produit_id')
        nouvelle_quantite = int(request.POST.get('quantite', 1))
        
        if nouvelle_quantite <= 0:
            return supprimer_panier(request, produit_id)
        
        panier = request.session.get('panier', {})
        
        if str(produit_id) in panier:
            panier[str(produit_id)]['quantite'] = nouvelle_quantite
            request.session['panier'] = panier
            request.session.modified = True
            messages.success(request, 'Quantité mise à jour!')
        
    return redirect('panier')

def contact(request):
    config = ConfigurationSite.get_config()
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone', '')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')
        
        # Créer le message email
        email_message = f"""
        Nouveau message de contact depuis le site {config.nom_site}
        
        Nom: {nom}
        Email: {email}
        Téléphone: {telephone}
        Sujet: {sujet}
        
        Message:
        {message}
        """
        
        try:
            # Envoyer l'email si configuré
            if config.email and hasattr(settings, 'EMAIL_HOST'):
                send_mail(
                    subject=f"[{config.nom_site}] {sujet}",
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[config.email],
                    fail_silently=False,
                )
            
            messages.success(request, 'Votre message a été envoyé avec succès! Nous vous répondrons dans les plus brefs délais.')
            return redirect('contact')
            
        except Exception as e:
            messages.error(request, 'Une erreur est survenue lors de l\'envoi du message. Veuillez réessayer.')
    
    return render(request, 'contact.html')

def a_propos(request):
    return render(request, 'a_propos.html')

from django.shortcuts import render
from django.http import HttpResponseServerError, HttpResponseNotFound, HttpResponseForbidden

def handler404(request, exception):
    """Vue personnalisée pour les erreurs 404"""
    return HttpResponseNotFound(render(request, '404.html'))

def handler500(request):
    """Vue personnalisée pour les erreurs 500"""
    return HttpResponseServerError(render(request, '500.html'))

def handler403(request, exception):
    """Vue personnalisée pour les erreurs 403"""
    return HttpResponseForbidden(render(request, '403.html'))
