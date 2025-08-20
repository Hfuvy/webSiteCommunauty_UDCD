// static/js/main.js
// Animation des compteurs
document.addEventListener('DOMContentLoaded', function() {
    // Animation des compteurs de statistiques
    const counterElements = document.querySelectorAll('.counter-value');
    if (counterElements.length > 0) {
        counterElements.forEach(element => {
            const targetValue = element.textContent;
            element.textContent = "0";
            
            const increment = targetValue.includes('K') ? 
                parseInt(targetValue) / 50 : 
                targetValue.includes('%') ? 
                parseInt(targetValue) : 
                parseInt(targetValue);
            
            const startTime = performance.now();
            const animationDuration = 2000; // ms
            
            function updateCounter(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / animationDuration, 1);
                
                let currentValue;
                if (targetValue.includes('K')) {
                    currentValue = Math.floor(progress * increment);
                    element.textContent = currentValue + 'K+';
                } else if (targetValue.includes('%')) {
                    currentValue = Math.floor(progress * increment);
                    element.textContent = currentValue + '%';
                } else {
                    currentValue = Math.floor(progress * increment);
                    element.textContent = currentValue + '+';
                }
                
                if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                } else {
                    // Rétablir la valeur finale
                    element.textContent = targetValue;
                }
            }
            
            requestAnimationFrame(updateCounter);
        });
    }
    
    // Gestion des messages flash
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Animation des éléments au défilement
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = 1;
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.course-card').forEach(card => {
        card.style.opacity = 0;
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
    
    // Tooltips Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});