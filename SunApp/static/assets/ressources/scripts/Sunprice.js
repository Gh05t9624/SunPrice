document.addEventListener('DOMContentLoaded', function() {
    const menuBtn = document.querySelector('.menu-btn');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.overlay');
    const sidebarClose = document.querySelector('.sidebar-close');
    
    let isMenuOpen = false;

    // Sidebar toggle
    menuBtn.addEventListener('click', () => {
        isMenuOpen = !isMenuOpen;
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    });

    // Close sidebar when clicking overlay
    overlay.addEventListener('click', () => {
        isMenuOpen = false;
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    });

    // Close sidebar with close button
    sidebarClose.addEventListener('click', () => {
        isMenuOpen = false;
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // ... keep existing code (menu functionality)

    // Slider functionality
    const slider = document.querySelector('.slider');
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.querySelector('.slider-btn.prev');
    const nextBtn = document.querySelector('.slider-btn.next');
    
    let currentSlide = 0;
    const totalSlides = slides.length;
    
    function goToSlide(index) {
        if (index < 0) {
            currentSlide = totalSlides - 1;
        } else if (index >= totalSlides) {
            currentSlide = 0;
        } else {
            currentSlide = index;
        }
        
        slider.style.transform = `translateX(-${currentSlide * 33.333}%)`;
    }
    
    function nextSlide() {
        goToSlide(currentSlide + 1);
    }
    
    function prevSlide() {
        goToSlide(currentSlide - 1);
    }
    
    // Auto-advance slides
    let slideInterval = setInterval(nextSlide, 5000);
    
    // Reset interval when manually changing slides
    function resetInterval() {
        clearInterval(slideInterval);
        slideInterval = setInterval(nextSlide, 5000);
    }
    
    prevBtn.addEventListener('click', () => {
        prevSlide();
        resetInterval();
    });
    
    nextBtn.addEventListener('click', () => {
        nextSlide();
        resetInterval();
    });
});

// Qunatité
document.addEventListener('DOMContentLoaded', function() {
    // Gestion des miniatures
    const mainImage = document.querySelector('.product-main-image');
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            // Mise à jour de l'image principale
            mainImage.src = this.src;
            
            // Mise à jour de la classe active
            thumbnails.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });
    // Gestion de la quantité
    const minusBtn = document.querySelector('.quantity-btn.minus');
    const plusBtn = document.querySelector('.quantity-btn.plus');
    const quantityInput = document.querySelector('.quantity-input');
    minusBtn.addEventListener('click', () => {
        const currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
        }
    });
    plusBtn.addEventListener('click', () => {
        const currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
    });
    // Gestion du panier
    const addToCartBtn = document.querySelector('.add-to-cart-btn');
    addToCartBtn.addEventListener('click', () => {
        const quantity = parseInt(quantityInput.value);
        alert(`${quantity} produit(s) ajouté(s) au panier`);
    });
});


// ============== Bouton Links ==========
const navlinks = document.querySelectorAll('.nav-link');
const mobilenavlinks = document.querySelectorAll('.mobile-nav-link');

// ===== Remove Bouton Links PC =====
const changeActiveLink = () => {
    navlinks.forEach(link => {
        link.classList.remove('active-link');
    })
}

navlinks.forEach(link => {
    link.addEventListener('click', () => {
        changeActiveLink();
        link.classList.add('active-link');
    })
})

// ===== Remove Bouton Links Mobile =====
const changerActiveLink = () => {
    mobilenavlinks.forEach(link => {
        link.classList.remove('active-link');
    })
}

mobilenavlinks.forEach(link => {
    link.addEventListener('click', () => {
        changerActiveLink();
        link.classList.add('active-link');
    })
})

// Drop Down
let profilDropdownList = document.querySelector(".profil-dropdown-list");

const toggle = ()  => profilDropdownList.classList.toggle("active");