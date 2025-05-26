from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True, 
                             help_text="Image représentative de la catégorie")
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom
    
    @property
    def image_url(self):
        """Retourne l'URL de l'image ou une image par défaut"""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None

class SousCategorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='sous_categories')
    image = models.ImageField(upload_to='sous_categories/', blank=True, null=True,
                             help_text="Image représentative de la sous-catégorie")
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Sous-catégorie"
        verbose_name_plural = "Sous-catégories"
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.categorie.nom} - {self.nom}"
    
    @property
    def image_url(self):
        """Retourne l'URL de l'image ou celle de la catégorie parente"""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        elif self.categorie.image and hasattr(self.categorie.image, 'url'):
            return self.categorie.image.url
        return None

class Produit(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='produits/', blank=True, null=True)
    sous_categorie = models.ForeignKey(SousCategorie, on_delete=models.CASCADE, related_name='produits')
    en_stock = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-date_creation']
    
    def __str__(self):
        return self.nom
    
    @property
    def image_url(self):
        """Retourne l'URL de l'image du produit ou une image par défaut"""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None





from django.core.validators import RegexValidator




# # Nouveau modèle pour la configuration du site
# class SiteConfig(models.Model):
#     nom_site = models.CharField(max_length=100, default="Mon Shop")
#     slogan = models.CharField(max_length=200, blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     logo = models.ImageField(upload_to='site/', blank=True, null=True)
#     favicon = models.ImageField(upload_to='site/', blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)
#     telephone = models.CharField(max_length=20, blank=True, null=True)
#     adresse = models.TextField(blank=True, null=True)
#     date_modification = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         verbose_name = "Configuration du site"
#         verbose_name_plural = "Configuration du site"
    
#     def __str__(self):
#         return self.nom_site
    
#     def save(self, *args, **kwargs):
#         # S'assurer qu'il n'y a qu'une seule configuration
#         if not self.pk and SiteConfig.objects.exists():
#             raise ValueError('Il ne peut y avoir qu\'une seule configuration de site')
#         return super().save(*args, **kwargs)




class ConfigurationSite(models.Model):
    # Informations de base (prédéfinies)
    nom_site = models.CharField(max_length=100, default="ShopExcellence", 
                               help_text="Nom de votre boutique")
    slogan = models.CharField(max_length=200, default="Votre boutique de confiance", 
                             help_text="Slogan de votre boutique")
    description = models.TextField(default="Une expérience shopping moderne et intuitive", 
                                  help_text="Description de votre boutique")
    
    # Informations de contact
    telephone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Le numéro de téléphone doit être au format: '+999999999'. Jusqu'à 15 chiffres autorisés."
    )
    
    email = models.EmailField(blank=True, null=True, 
                             help_text="Email de contact principal")
    telephone = models.CharField(validators=[telephone_validator], max_length=17, 
                                blank=True, null=True,
                                help_text="Numéro de téléphone principal")
    telephone_2 = models.CharField(validators=[telephone_validator], max_length=17, 
                                  blank=True, null=True,
                                  help_text="Numéro de téléphone secondaire")
    
    # WhatsApp
    whatsapp = models.CharField(validators=[telephone_validator], max_length=17, 
                               blank=True, null=True,
                               help_text="Numéro WhatsApp (avec indicatif pays)")
    
    # Adresse
    adresse = models.TextField(blank=True, null=True, 
                              help_text="Adresse physique complète")
    ville = models.CharField(max_length=100, blank=True, null=True)
    code_postal = models.CharField(max_length=10, blank=True, null=True)
    pays = models.CharField(max_length=100, blank=True, null=True, default="France")
    
    # Liens Google Maps
    lien_google_maps = models.URLField(blank=True, null=True,
                                      help_text="Lien vers votre localisation Google Maps")
    
    # Réseaux sociaux
    facebook = models.URLField(blank=True, null=True, 
                              help_text="Lien vers votre page Facebook")
    instagram = models.URLField(blank=True, null=True,
                               help_text="Lien vers votre compte Instagram")
    twitter = models.URLField(blank=True, null=True,
                             help_text="Lien vers votre compte Twitter")
    linkedin = models.URLField(blank=True, null=True,
                              help_text="Lien vers votre page LinkedIn")
    youtube = models.URLField(blank=True, null=True,
                             help_text="Lien vers votre chaîne YouTube")
    tiktok = models.URLField(blank=True, null=True,
                            help_text="Lien vers votre compte TikTok")
    
    # Horaires d'ouverture
    horaires_lundi = models.CharField(max_length=100, blank=True, null=True,
                                     help_text="Ex: 9h00 - 18h00 ou Fermé")
    horaires_mardi = models.CharField(max_length=100, blank=True, null=True)
    horaires_mercredi = models.CharField(max_length=100, blank=True, null=True)
    horaires_jeudi = models.CharField(max_length=100, blank=True, null=True)
    horaires_vendredi = models.CharField(max_length=100, blank=True, null=True)
    horaires_samedi = models.CharField(max_length=100, blank=True, null=True)
    horaires_dimanche = models.CharField(max_length=100, blank=True, null=True)
    
    # Informations supplémentaires
    a_propos = models.TextField(blank=True, null=True,
                               help_text="Texte de présentation de votre entreprise")
    
    # Paramètres techniques
    logo = models.ImageField(upload_to='site/', blank=True, null=True,
                            help_text="Logo de votre boutique")
    favicon = models.ImageField(upload_to='site/', blank=True, null=True,
                               help_text="Icône du site (favicon)")
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuration du site"
        verbose_name_plural = "Configuration du site"
    
    def __str__(self):
        return f"Configuration - {self.nom_site}"
    
    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule configuration
        if not self.pk and ConfigurationSite.objects.exists():
            raise ValueError("Une seule configuration est autorisée")
        super().save(*args, **kwargs)
    
    @classmethod
    def get_config(cls):
        """Récupère la configuration du site ou en crée une par défaut"""
        config, created = cls.objects.get_or_create(pk=1)
        return config
    
    @property
    def whatsapp_url(self):
        """Génère l'URL WhatsApp"""
        if self.whatsapp:
            # Nettoyer le numéro (enlever espaces, tirets, etc.)
            numero_clean = ''.join(filter(str.isdigit, self.whatsapp))
            if not numero_clean.startswith('33'):  # Ajouter indicatif France si nécessaire
                numero_clean = '33' + numero_clean.lstrip('0')
            return f"https://wa.me/{numero_clean}"
        return None
    
    @property
    def adresse_complete(self):
        """Retourne l'adresse complète formatée"""
        elements = [self.adresse, self.code_postal, self.ville, self.pays]
        return ', '.join([elem for elem in elements if elem])
    
    @property
    def horaires_semaine(self):
        """Retourne les horaires de la semaine sous forme de dictionnaire"""
        return {
            'Lundi': self.horaires_lundi,
            'Mardi': self.horaires_mardi,
            'Mercredi': self.horaires_mercredi,
            'Jeudi': self.horaires_jeudi,
            'Vendredi': self.horaires_vendredi,
            'Samedi': self.horaires_samedi,
            'Dimanche': self.horaires_dimanche,
        }
    
    @property
    def reseaux_sociaux(self):
        """Retourne les réseaux sociaux configurés"""
        reseaux = {}
        if self.facebook:
            reseaux['Facebook'] = {'url': self.facebook, 'icon': 'bxl-facebook'}
        if self.instagram:
            reseaux['Instagram'] = {'url': self.instagram, 'icon': 'bxl-instagram'}
        if self.twitter:
            reseaux['Twitter'] = {'url': self.twitter, 'icon': 'bxl-twitter'}
        if self.linkedin:
            reseaux['LinkedIn'] = {'url': self.linkedin, 'icon': 'bxl-linkedin'}
        if self.youtube:
            reseaux['YouTube'] = {'url': self.youtube, 'icon': 'bxl-youtube'}
        if self.tiktok:
            reseaux['TikTok'] = {'url': self.tiktok, 'icon': 'bxl-tiktok'}
        return reseaux