// *.index.html jss edits

// loading effect upon website start/page change
window.addEventListener('load', function() {
    const loader = document.querySelector('.loader-wrapper');
    loader.classList.add('hidden');

    setTimeout(() => {
        loader.remove();
    }, 1000);
});

// particles
document.addEventListener('DOMContentLoaded', function() {
    const particlesContainer = document.querySelector('.particles');
    for (let i = 0; i < 10; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.width = Math.random() * 300 + 1 + 'px';
        particle.style.height = particle.style.width;
        particle.style.animationDuration = Math.random() * 10 + 5 + 's';
        particlesContainer.appendChild(particle);
    }
});

// password strength indicator
document.getElementById('register-password').addEventListener('input', function(e) {
    const strengthBar = document.querySelector('.strength-bar');
    const strength = Math.min(e.target.value.length / 12 * 100, 100);
    strengthBar.style.width = strength + '%';
    strengthBar.style.background = strength < 40 ? '#ff4d4d' :
                                  strength < 70 ? '#4f8aff' :
                                  '#2be2a4';

});
