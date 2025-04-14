document.addEventListener('DOMContentLoaded', function() {
    const track = document.querySelector('.slider-track');
    const slides = document.querySelectorAll('.slide');
    const dotsContainer = document.querySelector('.slider-dots');
    
    let currentSlide = 0;
    let slideInterval;
    
 
    slides.forEach((_, index) => {
        const dot = document.createElement('div');
        dot.classList.add('dot');
        if (index === 0) dot.classList.add('active');
        dot.addEventListener('click', () => {
            clearInterval(slideInterval);
            currentSlide = index;
            updateSlider();
            startSlideShow();
        });
        dotsContainer.appendChild(dot);
    });
    
    const dots = document.querySelectorAll('.dot');
    
    function updateSlider() {
     
        track.style.transform = `translateX(-${currentSlide * 100}%)`;
        
       
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentSlide);
        });
    }
    
    function moveSlide(direction) {
        currentSlide = (currentSlide + direction + slides.length) % slides.length;
        updateSlider();
    }
    
    function startSlideShow() {
        slideInterval = setInterval(() => {
            moveSlide(1);
        }, 5000);
    }
    
    track.addEventListener('mouseenter', () => {
        clearInterval(slideInterval);
    });
    
    track.addEventListener('mouseleave', () => {
        startSlideShow();
    });
    
    startSlideShow();
}); 