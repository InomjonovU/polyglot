/**
 * PolyglotLC - Main JavaScript
 * Modern, clean, and performant
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all modules
    initCustomCursor();
    initHeader();
    initMobileMenu();
    initBackToTop();
    initAlerts();
    initAccordion();
    initTabs();
    initModals();
    initForms();
    initAnimations();
    initCounters();
});

/**
 * Custom Cursor
 */
function initCustomCursor() {
    const cursor = document.querySelector('.custom-cursor');
    const follower = document.querySelector('.cursor-follower');
    
    if (!cursor || !follower) return;
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
    
    let mouseX = 0, mouseY = 0;
    let cursorX = 0, cursorY = 0;
    let followerX = 0, followerY = 0;
    
    document.addEventListener('mousemove', function(e) {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });
    
    function animate() {
        // Cursor (instant)
        cursorX = mouseX;
        cursorY = mouseY;
        cursor.style.left = cursorX + 'px';
        cursor.style.top = cursorY + 'px';
        
        // Follower (smooth)
        followerX += (mouseX - followerX) * 0.15;
        followerY += (mouseY - followerY) * 0.15;
        follower.style.left = followerX + 'px';
        follower.style.top = followerY + 'px';
        
        requestAnimationFrame(animate);
    }
    animate();
    
    // Hover effects
    const hoverElements = document.querySelectorAll('a, button, input, textarea, select, [data-cursor-hover]');
    hoverElements.forEach(function(el) {
        el.addEventListener('mouseenter', function() {
            document.body.classList.add('cursor-hover');
        });
        el.addEventListener('mouseleave', function() {
            document.body.classList.remove('cursor-hover');
        });
    });
}

/**
 * Header
 */
function initHeader() {
    const header = document.getElementById('header');
    if (!header) return;
    
    let lastScroll = 0;
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        // Add/remove scrolled class
        if (currentScroll > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    });
}

/**
 * Mobile Menu
 */
function initMobileMenu() {
    const toggle = document.getElementById('navToggle');
    const menu = document.getElementById('mobileMenu');
    
    if (!toggle || !menu) return;
    
    toggle.addEventListener('click', function() {
        toggle.classList.toggle('active');
        menu.classList.toggle('active');
        document.body.classList.toggle('menu-open');
    });
    
    // Close menu when clicking links
    const menuLinks = menu.querySelectorAll('a');
    menuLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            toggle.classList.remove('active');
            menu.classList.remove('active');
            document.body.classList.remove('menu-open');
        });
    });
    
    // Close on escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && menu.classList.contains('active')) {
            toggle.classList.remove('active');
            menu.classList.remove('active');
            document.body.classList.remove('menu-open');
        }
    });
}

/**
 * Back to Top Button
 */
function initBackToTop() {
    const btn = document.getElementById('backToTop');
    if (!btn) return;
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            btn.classList.add('visible');
        } else {
            btn.classList.remove('visible');
        }
    });
    
    btn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/**
 * Alert Messages
 */
function initAlerts() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(function(alert) {
        const closeBtn = alert.querySelector('.alert-close');
        
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                alert.style.animation = 'slideOut 0.3s ease forwards';
                setTimeout(function() {
                    alert.remove();
                }, 300);
            });
        }
        
        // Auto dismiss after 5 seconds
        setTimeout(function() {
            if (alert.parentNode) {
                alert.style.animation = 'slideOut 0.3s ease forwards';
                setTimeout(function() {
                    alert.remove();
                }, 300);
            }
        }, 5000);
    });
}

/**
 * Accordion
 */
function initAccordion() {
    const accordions = document.querySelectorAll('.accordion');
    
    accordions.forEach(function(accordion) {
        const items = accordion.querySelectorAll('.accordion-item');
        
        items.forEach(function(item) {
            const header = item.querySelector('.accordion-header');
            
            header.addEventListener('click', function() {
                const isActive = item.classList.contains('active');
                
                // Close all items
                items.forEach(function(i) {
                    i.classList.remove('active');
                });
                
                // Open clicked item if it wasn't active
                if (!isActive) {
                    item.classList.add('active');
                }
            });
        });
    });
}

/**
 * Tabs
 */
function initTabs() {
    const tabContainers = document.querySelectorAll('[data-tabs]');
    
    tabContainers.forEach(function(container) {
        const buttons = container.querySelectorAll('.tab-btn');
        const contents = container.querySelectorAll('.tab-content');
        
        buttons.forEach(function(btn) {
            btn.addEventListener('click', function() {
                const target = btn.getAttribute('data-tab');
                
                // Update buttons
                buttons.forEach(function(b) {
                    b.classList.remove('active');
                });
                btn.classList.add('active');
                
                // Update content
                contents.forEach(function(content) {
                    content.classList.remove('active');
                    if (content.getAttribute('data-tab-content') === target) {
                        content.classList.add('active');
                    }
                });
            });
        });
    });
}

/**
 * Modals
 */
function initModals() {
    const modalTriggers = document.querySelectorAll('[data-modal]');
    const modals = document.querySelectorAll('.modal');
    
    modalTriggers.forEach(function(trigger) {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            const modalId = trigger.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            if (modal) {
                openModal(modal);
            }
        });
    });
    
    modals.forEach(function(modal) {
        const backdrop = modal.querySelector('.modal-backdrop');
        const closeBtn = modal.querySelector('.modal-close');
        
        if (backdrop) {
            backdrop.addEventListener('click', function() {
                closeModal(modal);
            });
        }
        
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                closeModal(modal);
            });
        }
    });
    
    // Close on escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const activeModal = document.querySelector('.modal.active');
            if (activeModal) {
                closeModal(activeModal);
            }
        }
    });
}

function openModal(modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal(modal) {
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

/**
 * Forms
 */
function initForms() {
    // Form validation styling
    const forms = document.querySelectorAll('form');
    
    forms.forEach(function(form) {
        const inputs = form.querySelectorAll('.form-input, .form-select, .form-textarea');
        
        inputs.forEach(function(input) {
            input.addEventListener('blur', function() {
                if (input.value.trim() !== '') {
                    input.classList.add('has-value');
                } else {
                    input.classList.remove('has-value');
                }
            });
            
            // Check on load
            if (input.value.trim() !== '') {
                input.classList.add('has-value');
            }
        });
    });
    
    // File input preview
    const fileInputs = document.querySelectorAll('.form-file input[type="file"]');
    
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const label = input.parentElement.querySelector('.form-file-label');
            if (input.files.length > 0) {
                label.innerHTML = '<i class="fas fa-check"></i> ' + input.files[0].name;
            }
        });
    });
}

/**
 * Animations (AOS)
 */
function initAnimations() {
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-out-cubic',
            once: true,
            offset: 50,
            disable: 'mobile'
        });
    }
}

/**
 * Counter Animation
 */
function initCounters() {
    const counters = document.querySelectorAll('[data-counter]');
    
    if (counters.length === 0) return;
    
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.5
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    counters.forEach(function(counter) {
        observer.observe(counter);
    });
}

function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-counter'));
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    
    function update() {
        current += step;
        if (current < target) {
            element.textContent = Math.floor(current);
            requestAnimationFrame(update);
        } else {
            element.textContent = target;
        }
    }
    
    update();
}

/**
 * Smooth Scroll for anchor links
 */
document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href === '#') return;
        
        const target = document.querySelector(href);
        if (target) {
            e.preventDefault();
            const headerHeight = document.getElementById('header')?.offsetHeight || 80;
            const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

/**
 * Lazy Loading Images
 */
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                imageObserver.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(function(img) {
        imageObserver.observe(img);
    });
}

/**
 * Gallery Lightbox (Simple)
 */
function initGalleryLightbox() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    galleryItems.forEach(function(item) {
        item.addEventListener('click', function() {
            const img = item.querySelector('img');
            if (!img) return;
            
            const lightbox = document.createElement('div');
            lightbox.className = 'lightbox';
            lightbox.innerHTML = `
                <div class="lightbox-backdrop"></div>
                <div class="lightbox-content">
                    <img src="${img.src}" alt="${img.alt || ''}">
                    <button class="lightbox-close"><i class="fas fa-times"></i></button>
                </div>
            `;
            
            document.body.appendChild(lightbox);
            document.body.style.overflow = 'hidden';
            
            setTimeout(function() {
                lightbox.classList.add('active');
            }, 10);
            
            const close = function() {
                lightbox.classList.remove('active');
                setTimeout(function() {
                    lightbox.remove();
                    document.body.style.overflow = '';
                }, 300);
            };
            
            lightbox.querySelector('.lightbox-backdrop').addEventListener('click', close);
            lightbox.querySelector('.lightbox-close').addEventListener('click', close);
        });
    });
}

// Initialize lightbox if gallery exists
if (document.querySelector('.gallery-item')) {
    initGalleryLightbox();
}

/**
 * Price Formatter
 */
function formatPrice(price) {
    return new Intl.NumberFormat('uz-UZ').format(price) + ' so\'m';
}

/**
 * Search Functionality
 */
const searchInput = document.querySelector('.search-input');
if (searchInput) {
    let debounceTimer;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(function() {
            // Perform search or filter
            console.log('Search:', searchInput.value);
        }, 300);
    });
}

/**
 * Course Filter
 */
const filterForm = document.querySelector('.filter-form');
if (filterForm) {
    const filterInputs = filterForm.querySelectorAll('.filter-input, .filter-select');
    
    filterInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            // Auto submit on change (optional)
            // filterForm.submit();
        });
    });
}

// Add slideOut animation
const styleSheet = document.createElement('style');
styleSheet.textContent = `
    @keyframes slideOut {
        from { opacity: 1; transform: translateX(0); }
        to { opacity: 0; transform: translateX(100%); }
    }
    
    .lightbox {
        position: fixed;
        inset: 0;
        z-index: 10000;
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .lightbox.active {
        opacity: 1;
    }
    
    .lightbox-backdrop {
        position: absolute;
        inset: 0;
        background: rgba(0, 0, 0, 0.9);
    }
    
    .lightbox-content {
        position: relative;
        max-width: 90vw;
        max-height: 90vh;
    }
    
    .lightbox-content img {
        max-width: 100%;
        max-height: 90vh;
        object-fit: contain;
        border-radius: 8px;
    }
    
    .lightbox-close {
        position: absolute;
        top: -40px;
        right: 0;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        background: none;
        border: none;
        transition: transform 0.2s ease;
    }
    
    .lightbox-close:hover {
        transform: scale(1.2);
    }
`;
document.head.appendChild(styleSheet);
