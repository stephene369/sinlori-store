// Menu mobile toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
            
            // Animation de l'icône
            const icon = mobileMenuBtn.querySelector('i');
            if (mobileMenu.classList.contains('hidden')) {
                icon.className = 'bx bx-menu text-2xl';
            } else {
                icon.className = 'bx bx-x text-2xl';
            }
        });
    }
    
    // Smooth scroll pour les ancres
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Animation des cartes au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observer toutes les cartes
    document.querySelectorAll('.group').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
    
    // Notification toast pour les messages
    const messages = document.querySelectorAll('[class*="bg-green-100"]');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Fonction pour ajouter au panier avec animation
function addToCartAnimation(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="bx bx-loader-alt animate-spin mr-2"></i>Ajout...';
    button.disabled = true;
    
    setTimeout(() => {
        button.innerHTML = '<i class="bx bx-check mr-2"></i>Ajouté !';
        button.classList.remove('from-primary', 'to-secondary');
        button.classList.add('bg-green-500');
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
            button.classList.add('from-primary', 'to-secondary');
            button.classList.remove('bg-green-500');
        }, 1500);
    }, 800);
}

// Recherche en temps réel (optionnel)
function setupSearch() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const products = document.querySelectorAll('.product-card');
            
            products.forEach(product => {
                const title = product.querySelector('h3').textContent.toLowerCase();
                if (title.includes(query)) {
                    product.style.display = 'block';
                } else {
                    product.style.display = 'none';
                }
            });
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.slide');
    let currentSlide = 0;

    function showNextSlide() {
        // Masquer le slide actuel
        slides[currentSlide].classList.remove('active');
        
        // Passer au slide suivant
        currentSlide = (currentSlide + 1) % slides.length;
        
        // Afficher le nouveau slide
        slides[currentSlide].classList.add('active');
    }

    // Changer d'image toutes les 3 secondes
    setInterval(showNextSlide, 3000);
});
