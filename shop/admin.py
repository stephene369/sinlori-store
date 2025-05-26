from django.contrib import admin
from .models import Categorie, SousCategorie, Produit

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'description', 'image', 'date_creation']
    list_filter = ['date_creation']
    search_fields = ['nom', 'description']
    readonly_fields = ['date_creation']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'description')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        }),
    )

@admin.register(SousCategorie)
class SousCategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'categorie', 'description', 'image', 'date_creation']
    list_filter = ['categorie', 'date_creation']
    search_fields = ['nom', 'description', 'categorie__nom']
    readonly_fields = ['date_creation']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'categorie', 'description')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['nom', 'sous_categorie', 'prix', 'en_stock', 'image', 'date_creation']
    list_filter = ['sous_categorie', 'en_stock', 'date_creation']
    search_fields = ['nom', 'description']
    readonly_fields = ['date_creation']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'sous_categorie', 'description')
        }),
        ('Prix et stock', {
            'fields': ('prix', 'en_stock')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        }),
    )








from .models import ConfigurationSite

@admin.register(ConfigurationSite)
class ConfigurationSiteAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Empêcher la création de plusieurs configurations
        return not ConfigurationSite.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Empêcher la suppression de la configuration
        return False
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('nom_site', 'slogan', 'description'),
            'description': 'Informations principales de votre boutique'
        }),
        ('Contact', {
            'fields': ('email', 'telephone', 'telephone_2', 'whatsapp'),
            'description': 'Moyens de contact avec vos clients'
        }),
        ('Adresse', {
            'fields': ('adresse', 'ville', 'code_postal', 'pays', 'lien_google_maps'),
            'description': 'Localisation de votre boutique'
        }),
        ('Réseaux sociaux', {
            'fields': ('facebook', 'instagram', 'twitter', 'linkedin', 'youtube', 'tiktok'),
            'description': 'Liens vers vos réseaux sociaux',
            'classes': ('collapse',)
        }),
        ('Horaires d\'ouverture', {
            'fields': ('horaires_lundi', 'horaires_mardi', 'horaires_mercredi', 
                      'horaires_jeudi', 'horaires_vendredi', 'horaires_samedi', 'horaires_dimanche'),
            'description': 'Horaires d\'ouverture de votre boutique',
            'classes': ('collapse',)
        }),
        ('À propos', {
            'fields': ('a_propos',),
            'description': 'Présentation de votre entreprise'
        }),
        ('Images', {
            'fields': ('logo', 'favicon'),
            'description': 'Logo et favicon de votre site',
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ['date_creation', 'date_modification']
    
    def get_object(self, request, object_id, from_field=None):
        # Toujours retourner la configuration unique
        return ConfigurationSite.get_config()
    
    def changelist_view(self, request, extra_context=None):
        # Rediriger vers la page de modification
        config = ConfigurationSite.get_config()
        return self.change_view(request, str(config.pk), '', extra_context)