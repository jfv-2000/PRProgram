const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.navlinks');
    const navLinks = document.querySelectorAll('.navlinks li');

    burger.addEventListener('click', () => {
        //toggle
        nav.classList.toggle('nav-active');
        //animation links
        navLinks.forEach((link) => {
            link.style.animation = 'navLinkFade 0.5s ease forwards';
        });
    });
}
navSlide();
