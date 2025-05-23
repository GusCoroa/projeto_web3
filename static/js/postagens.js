function expandirTexto(button) {
    var texto = button.previousElementSibling;
    texto.classList.toggle("expandidotexto"); 

   
    if (texto.classList.contains("expandidotexto")) {
        button.textContent = "Ver menos";
    } else {
        button.textContent = "Ver mais";
    }
}

const slidesContainer = document.querySelector('.slides');
const slides = Array.from(document.querySelectorAll('.slide'));
const prevBtn = document.querySelector('.prev');
const nextBtn = document.querySelector('.next');
let currentIndex = 0;

function updateCarousel() {
  const offset = -currentIndex * 100;
  slidesContainer.style.transform = `translateX(${offset}%)`;
}

prevBtn.addEventListener('click', () => {
  currentIndex = (currentIndex - 1 + slides.length) % slides.length;
  updateCarousel();
});

nextBtn.addEventListener('click', () => {
  currentIndex = (currentIndex + 1) % slides.length;
  updateCarousel();
});

// inicia no slide 0
updateCarousel();

  