/**
 * Sahil Talape - Premium Glassmorphism Portfolio Main JavaScript
 * Handles: Theme Toggle, Mobile Menu, Scroll Reveal, Intersection Active Nav, Testimonials Carousel, Contact Form POST
 */

document.addEventListener('DOMContentLoaded', () => {

  // --- Theme Toggle System ---
  const themeToggle = document.getElementById('theme-toggle');
  const sunIcon = document.getElementById('sun-icon');
  const moonIcon = document.getElementById('moon-icon');
  const navbar = document.getElementById('navbar');
  const mobileMenu = document.getElementById('mobile-menu');

  // Check saved theme or default to Dark mode
  const currentTheme = localStorage.getItem('theme') || 'dark';
  applyTheme(currentTheme);

  themeToggle.addEventListener('click', () => {
    const activeTheme = document.documentElement.classList.contains('light') ? 'dark' : 'light';
    applyTheme(activeTheme);
  });

  function applyTheme(theme) {
    if (theme === 'light') {
      document.documentElement.classList.remove('dark');
      document.documentElement.classList.add('light');
      // Show moon icon, hide sun icon (means clicking will switch back to dark)
      sunIcon.classList.add('hidden');
      moonIcon.classList.remove('hidden');
      localStorage.setItem('theme', 'light');
      
      // Update nav styles
      navbar.classList.remove('glass-nav-dark');
      navbar.classList.add('glass-nav-light');
      mobileMenu.classList.remove('glass-nav-dark');
      mobileMenu.classList.add('glass-nav-light');
    } else {
      document.documentElement.classList.remove('light');
      document.documentElement.classList.add('dark');
      // Show sun icon, hide moon icon
      sunIcon.classList.remove('hidden');
      moonIcon.classList.add('hidden');
      localStorage.setItem('theme', 'dark');

      // Update nav styles
      navbar.classList.remove('glass-nav-light');
      navbar.classList.add('glass-nav-dark');
      mobileMenu.classList.remove('glass-nav-light');
      mobileMenu.classList.add('glass-nav-dark');
    }
    // Perform quick layout adjustments for cards if needed
    updateCardGlows(theme);
  }

  function updateCardGlows(theme) {
    const glassCards = document.querySelectorAll('.glass-card-dark, .glass-card-light');
    glassCards.forEach(card => {
      if (theme === 'light') {
        card.classList.remove('glass-card-dark');
        card.classList.add('glass-card-light');
      } else {
        card.classList.remove('glass-card-light');
        card.classList.add('glass-card-dark');
      }
    });
  }


  // --- Mobile Drawer Menu ---
  const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
  let isMenuOpen = false;

  mobileMenuToggle.addEventListener('click', () => {
    isMenuOpen = !isMenuOpen;
    if (isMenuOpen) {
      mobileMenu.classList.remove('hidden');
      setTimeout(() => {
        mobileMenu.classList.remove('scale-95', 'opacity-0');
        mobileMenu.classList.add('scale-100', 'opacity-100');
      }, 10);
    } else {
      closeMenu();
    }
  });

  // Close menu on selecting any link
  const mobileLinks = document.querySelectorAll('.mobile-nav-link');
  mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
      closeMenu();
    });
  });

  function closeMenu() {
    isMenuOpen = false;
    mobileMenu.classList.remove('scale-100', 'opacity-100');
    mobileMenu.classList.add('scale-95', 'opacity-0');
    setTimeout(() => {
      mobileMenu.classList.add('hidden');
    }, 300);
  }


  // --- Intersection Observer for Scroll Reveal ---
  const revealElements = document.querySelectorAll('.reveal');
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        // If it's the skills section, animate the progress bars
        if (entry.target.id === 'skills' || entry.target.querySelector('.skill-bar')) {
          animateSkills();
        }
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px'
  });

  revealElements.forEach(el => revealObserver.observe(el));


  // --- Skills Progress Bars Animation ---
  function animateSkills() {
    const progressBars = document.querySelectorAll('.skill-bar');
    progressBars.forEach(bar => {
      const width = bar.getAttribute('data-width');
      bar.style.transition = 'width 1.5s cubic-bezier(0.1, 0.8, 0.2, 1)';
      bar.style.width = width;
    });
  }


  // --- Active Nav Section Highlighting ---
  const sections = document.querySelectorAll('section');
  const navLinks = document.querySelectorAll('.nav-link');

  window.addEventListener('scroll', () => {
    let currentSectionId = '';
    sections.forEach(sec => {
      const secTop = sec.offsetTop;
      const secHeight = sec.clientHeight;
      if (pageYOffset >= (secTop - 120)) {
        currentSectionId = sec.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('text-violet-400', 'after:w-full');
      link.classList.add('text-slate-300');
      if (link.getAttribute('href').slice(1) === currentSectionId) {
        link.classList.remove('text-slate-300');
        link.classList.add('text-violet-400', 'after:w-full');
      }
    });
  });


  // --- Typing Text Animation in Hero ---
  const roles = ["Full Stack Developer", "FastAPI Engineer", "UI/UX Craftsman", "Python Developer"];
  const typingText = document.getElementById('typing-text');
  let roleIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let typingSpeed = 100;

  function typeEffect() {
    const currentRole = roles[roleIndex];
    if (isDeleting) {
      typingText.textContent = currentRole.substring(0, charIndex - 1);
      charIndex--;
      typingSpeed = 50;
    } else {
      typingText.textContent = currentRole.substring(0, charIndex + 1);
      charIndex++;
      typingSpeed = 100;
    }

    if (!isDeleting && charIndex === currentRole.length) {
      isDeleting = true;
      typingSpeed = 1500; // Pause at end of word
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      roleIndex = (roleIndex + 1) % roles.length;
      typingSpeed = 500; // Pause before starting new word
    }

    setTimeout(typeEffect, typingSpeed);
  }
  
  // Start typing
  setTimeout(typeEffect, 1000);


  // --- Testimonials Slider / Carousel ---
  const track = document.getElementById('testimonial-track');
  const slides = Array.from(track.children);
  const nextButton = document.getElementById('slider-next');
  const prevButton = document.getElementById('slider-prev');
  const dots = document.querySelectorAll('.slider-dot');
  let currentSlideIndex = 0;

  function updateSlider() {
    track.style.transform = `translateX(-${currentSlideIndex * 100}%)`;
    
    // Update dots
    dots.forEach((dot, index) => {
      dot.classList.remove('bg-violet-600', 'w-4');
      dot.classList.add('bg-violet-600/30', 'w-2');
      if (index === currentSlideIndex) {
        dot.classList.remove('bg-violet-600/30', 'w-2');
        dot.classList.add('bg-violet-600', 'w-4');
      }
    });
  }

  nextButton.addEventListener('click', () => {
    currentSlideIndex = (currentSlideIndex + 1) % slides.length;
    updateSlider();
  });

  prevButton.addEventListener('click', () => {
    currentSlideIndex = (currentSlideIndex - 1 + slides.length) % slides.length;
    updateSlider();
  });

  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      currentSlideIndex = index;
      updateSlider();
    });
  });

  // Auto-sliding every 6 seconds
  let slideInterval = setInterval(() => {
    currentSlideIndex = (currentSlideIndex + 1) % slides.length;
    updateSlider();
  }, 6000);

  // Pause autoslide on user interaction
  const sliderContainer = document.getElementById('testimonials');
  sliderContainer.addEventListener('mouseenter', () => clearInterval(slideInterval));
  sliderContainer.addEventListener('mouseleave', () => {
    slideInterval = setInterval(() => {
      currentSlideIndex = (currentSlideIndex + 1) % slides.length;
      updateSlider();
    }, 6000);
  });


  // --- Contact Form Handling & FastAPI Integration ---
  const contactForm = document.getElementById('contact-form');
  const formLoader = document.getElementById('form-loader');
  
  // Custom Glass Toast Alert
  const toastWrapper = document.getElementById('toast-wrapper');
  const toastIcon = document.getElementById('toast-icon');
  const toastTitle = document.getElementById('toast-title');
  const toastDesc = document.getElementById('toast-desc');

  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('form-name').value.trim();
    const email = document.getElementById('form-email').value.trim();
    const message = document.getElementById('form-message').value.trim();

    // Visual loading state
    formLoader.classList.remove('opacity-0', 'pointer-events-none');
    formLoader.classList.add('opacity-100');

    try {
      const endpoint = window.location.protocol === 'file:' 
        ? 'http://localhost:8000/api/contact' 
        : '/api/contact';

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email, message })
      });

      const result = await response.json();

      if (response.ok) {
        showToast(true, 'Transmission Succeeded', result.message || 'Your message has been successfully saved to our localized database.');
        contactForm.reset();
      } else {
        const errorDetail = result.detail ? (Array.isArray(result.detail) ? result.detail[0].msg : result.detail) : 'An error occurred during submission.';
        showToast(false, 'Submission Refused', errorDetail);
      }

    } catch (error) {
      showToast(false, 'Local API Unreachable', 'Backend server placeholder is currently sleeping. Run "run.bat" to boot FastAPI locally!');
    } finally {
      // Hide loading state
      formLoader.classList.remove('opacity-100');
      formLoader.classList.add('opacity-0', 'pointer-events-none');
    }
  });

  function showToast(isSuccess, title, desc) {
    // Configure colors based on state
    if (isSuccess) {
      toastIcon.textContent = '✓';
      toastIcon.className = 'w-8 h-8 rounded-lg bg-emerald-600/20 flex items-center justify-center text-emerald-400 font-bold border border-emerald-500/20';
      toastWrapper.querySelector('div').className = 'glass-card-dark rounded-xl p-4 border border-emerald-500/30 shadow-2xl flex items-start gap-3';
    } else {
      toastIcon.textContent = '✕';
      toastIcon.className = 'w-8 h-8 rounded-lg bg-rose-600/20 flex items-center justify-center text-rose-400 font-bold border border-rose-500/20';
      toastWrapper.querySelector('div').className = 'glass-card-dark rounded-xl p-4 border border-rose-500/30 shadow-2xl flex items-start gap-3';
    }

    toastTitle.textContent = title;
    toastDesc.textContent = desc;

    // Slide in
    toastWrapper.classList.remove('translate-y-24', 'opacity-0', 'pointer-events-none');
    toastWrapper.classList.add('translate-y-0', 'opacity-100');

    // Auto slide out after 5 seconds
    setTimeout(() => {
      toastWrapper.classList.remove('translate-y-0', 'opacity-100');
      toastWrapper.classList.add('translate-y-24', 'opacity-0', 'pointer-events-none');
    }, 5000);
  }

});
