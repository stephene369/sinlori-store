#!/bin/bash
echo "🚀 Déploiement E-commerce Django"

# Installation des dépendances
pip install -r requirements.txt

# Migrations
python manage.py makemigrations
python manage.py migrate

# Collecte des fichiers statiques
python manage.py collectstatic --noinput

# Création du superutilisateur (optionnel)
echo "Créer un superutilisateur ? (y/n)"
read create_super
if [ "$create_super" = "y" ]; then
    python manage.py createsuperuser
fi

echo "✅ Déploiement terminé !"
echo "📝 N'oubliez pas de :"
echo "   - Configurer votre numéro WhatsApp dans settings.py"
echo "   - Ajouter vos catégories via /admin/"
echo "   - Tester le site sur votre domaine"
