// Build My Skillset - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeScrollEffects();
    initializeFormValidation();
    initializeTooltips();
    initializeCounters();
    initializeImageLazyLoading();
    initializeSearchFilters();
    initializeThemeToggle();
});

// Scroll Effects
function initializeScrollEffects() {
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Parallax effect for hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        });
    }

    // Animate elements on scroll
    const animateElements = document.querySelectorAll('.card, .feature-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    animateElements.forEach(el => observer.observe(el));
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                
                // Add custom validation styling
                const invalidFields = form.querySelectorAll(':invalid');
                invalidFields.forEach(field => {
                    field.classList.add('is-invalid');
                    
                    // Remove invalid class on input
                    field.addEventListener('input', function() {
                        if (field.checkValidity()) {
                            field.classList.remove('is-invalid');
                            field.classList.add('is-valid');
                        }
                    });
                });
            }
            
            form.classList.add('was-validated');
        });
    });

    // Real-time email validation
    const emailFields = document.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        field.addEventListener('blur', function() {
            validateEmail(field);
        });
    });

    // Password confirmation validation
    const passwordFields = document.querySelectorAll('input[name="password"]');
    const confirmPasswordFields = document.querySelectorAll('input[name="confirm_password"]');
    
    if (passwordFields.length && confirmPasswordFields.length) {
        confirmPasswordFields.forEach(confirmField => {
            confirmField.addEventListener('input', function() {
                const passwordField = document.querySelector('input[name="password"]');
                if (passwordField && confirmField.value !== passwordField.value) {
                    confirmField.setCustomValidity('Passwords do not match');
                } else {
                    confirmField.setCustomValidity('');
                }
            });
        });
    }
}

// Email validation helper
function validateEmail(field) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const isValid = emailRegex.test(field.value);
    
    if (field.value && !isValid) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
    } else if (field.value && isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    }
    
    return isValid;
}

// Tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Counter Animation
function initializeCounters() {
    const counters = document.querySelectorAll('.stat-item h3');
    
    const animateCounter = (counter) => {
        const target = parseInt(counter.textContent.replace(/\D/g, ''));
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            // Format the number
            const formatted = Math.floor(current);
            const originalText = counter.textContent;
            const suffix = originalText.replace(/\d/g, '');
            counter.textContent = formatted + suffix;
        }, 16);
    };
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    });
    
    counters.forEach(counter => counterObserver.observe(counter));
}

// Lazy Loading for Images
function initializeImageLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('loading');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => {
        img.classList.add('loading');
        imageObserver.observe(img);
    });
}

// Search and Filter Functionality
function initializeSearchFilters() {
    // Course level filter
    const levelButtons = document.querySelectorAll('.btn-group a');
    levelButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Update active state
            levelButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Search functionality
    const searchInputs = document.querySelectorAll('input[type="search"]');
    searchInputs.forEach(input => {
        let searchTimeout;
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(this.value);
            }, 300);
        });
    });
}

// Search implementation
function performSearch(query) {
    const cards = document.querySelectorAll('.course-card, .internship-card, .project-card');
    
    cards.forEach(card => {
        const title = card.querySelector('.card-title');
        const description = card.querySelector('.card-text');
        
        if (title && description) {
            const content = (title.textContent + ' ' + description.textContent).toLowerCase();
            const shouldShow = content.includes(query.toLowerCase()) || query === '';
            
            card.closest('.col-lg-4, .col-lg-6, .col-md-6').style.display = shouldShow ? 'block' : 'none';
        }
    });
}

// Theme Toggle (Light/Dark mode preparation)
function initializeThemeToggle() {
    const themeToggle = document.querySelector('#theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });
    }
    
    // Load saved theme
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }
}

// Utility Functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function smoothScrollTo(element) {
    element.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// File Upload Handling
function handleFileUpload(input) {
    const file = input.files[0];
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    
    if (file) {
        if (file.size > maxSize) {
            showNotification('File size must be less than 16MB', 'danger');
            input.value = '';
            return false;
        }
        
        if (!allowedTypes.includes(file.type)) {
            showNotification('Please upload a PDF or DOC file', 'danger');
            input.value = '';
            return false;
        }
        
        showNotification('File uploaded successfully!', 'success');
        return true;
    }
}

// Initialize file upload handlers
document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            handleFileUpload(this);
        });
    });
});

// Rating System
function initializeRatingSystem() {
    const ratingInputs = document.querySelectorAll('.rating-input');
    
    ratingInputs.forEach(ratingDiv => {
        const stars = ratingDiv.querySelectorAll('.star');
        const input = ratingDiv.querySelector('input[type="hidden"]');
        
        stars.forEach((star, index) => {
            star.addEventListener('click', function() {
                const rating = index + 1;
                input.value = rating;
                
                // Update visual state
                stars.forEach((s, i) => {
                    if (i < rating) {
                        s.classList.add('filled');
                    } else {
                        s.classList.remove('filled');
                    }
                });
            });
            
            star.addEventListener('mouseenter', function() {
                const rating = index + 1;
                stars.forEach((s, i) => {
                    if (i < rating) {
                        s.classList.add('hover');
                    } else {
                        s.classList.remove('hover');
                    }
                });
            });
        });
        
        ratingDiv.addEventListener('mouseleave', function() {
            stars.forEach(star => star.classList.remove('hover'));
        });
    });
}

// Copy to Clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showNotification('Copied to clipboard!', 'success');
    }).catch(function() {
        showNotification('Failed to copy to clipboard', 'danger');
    });
}

// Loading States
function showLoading(element) {
    element.classList.add('loading');
    element.disabled = true;
}

function hideLoading(element) {
    element.classList.remove('loading');
    element.disabled = false;
}

// AJAX Form Submission (for future enhancements)
function submitFormAjax(form, callback) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    
    showLoading(submitButton);
    
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        hideLoading(submitButton);
        if (callback) callback(data);
    })
    .catch(error => {
        hideLoading(submitButton);
        showNotification('An error occurred. Please try again.', 'danger');
        console.error('Error:', error);
    });
}

// Keyboard Navigation Support
document.addEventListener('keydown', function(e) {
    // Escape key to close modals
    if (e.key === 'Escape') {
        const openModal = document.querySelector('.modal.show');
        if (openModal) {
            const modal = bootstrap.Modal.getInstance(openModal);
            if (modal) modal.hide();
        }
    }
    
    // Enter key on buttons
    if (e.key === 'Enter' && e.target.classList.contains('btn')) {
        e.target.click();
    }
});

// Performance Monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
        }, 0);
    });
}

// Error Handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // Could send error to analytics service here
});

// Service Worker Registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('SW registered: ', registration);
            })
            .catch(function(registrationError) {
                console.log('SW registration failed: ', registrationError);
            });
    });
}
