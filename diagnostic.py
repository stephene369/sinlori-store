import os
import django
from django.conf import settings

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.db import connection
from shop.models import Categorie, SousCategorie, Produit

def diagnostic():
    print("🔍 DIAGNOSTIC DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    # Vérifier la connexion
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"✅ Tables existantes: {[table[0] for table in tables]}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    # Vérifier les modèles
    try:
        print(f"📊 Catégories: {Categorie.objects.count()}")
        print(f"📊 Sous-catégories: {SousCategorie.objects.count()}")
        print(f"📊 Produits: {Produit.objects.count()}")
    except Exception as e:
        print(f"❌ Erreur modèles: {e}")

if __name__ == "__main__":
    diagnostic()