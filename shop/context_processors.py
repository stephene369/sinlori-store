from .models import ConfigurationSite

def site_config(request):
    """Rend la configuration du site disponible dans tous les templates"""
    return {
        'site_config': ConfigurationSite.get_config()
    }