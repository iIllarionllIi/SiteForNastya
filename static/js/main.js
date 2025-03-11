document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mainNav = document.querySelector('.main-nav');
    const headerActions = document.querySelector('.header-actions');
    const body = document.body;

    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', function(e) {
            e.stopPropagation();
            this.classList.toggle('active');
            mainNav.classList.toggle('active');
            headerActions.classList.toggle('active');
            body.classList.toggle('menu-open');
        });
    }

    // Закрытие меню при клике на пункт меню
    const menuLinks = document.querySelectorAll('.nav-link');
    menuLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileMenuButton.classList.remove('active');
            mainNav.classList.remove('active');
            headerActions.classList.remove('active');
            body.classList.remove('menu-open');
        });
    });

    // Закрытие меню при клике вне его
    document.addEventListener('click', function(event) {
        if (mainNav.classList.contains('active') && 
            !event.target.closest('.main-nav') && 
            !event.target.closest('.mobile-menu-button')) {
            mobileMenuButton.classList.remove('active');
            mainNav.classList.remove('active');
            headerActions.classList.remove('active');
            body.classList.remove('menu-open');
        }
    });

    // Предотвращаем закрытие меню при клике внутри него
    mainNav.addEventListener('click', function(e) {
        e.stopPropagation();
    });
});