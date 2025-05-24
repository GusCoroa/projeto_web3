document.querySelectorAll('.accordion-header').forEach(header => {
  header.addEventListener('click', () => {
    document.querySelectorAll('.accordion-body').forEach(accordionBody => {
      if (accordionBody !== header.nextElementSibling) {
        accordionBody.classList.remove('active');
        accordionBody.previousElementSibling.querySelector('.arrow').style.transform = 'rotate(0deg)';
      }
    });

// SETINHA DO ACCORDION
    const accordionBody = header.nextElementSibling;
    let arrow = header.querySelector('.arrow');
    accordionBody.classList.toggle('active');
    arrow.style.transform = accordionBody.classList.contains('active') ? 'rotate(180deg)' : 'rotate(0deg)';
  });
});

//CARROSSEL

let slideIndex = 0;
const slides = document.querySelectorAll('.slide');
const indicators = document.querySelectorAll('.indicator');

function mostrarSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.remove('ativo');
    indicators[i].classList.remove('active');
  });
  slides[index].classList.add('ativo');
  indicators[index].classList.add('active');
}

function proximoSlide() {
  slideIndex = (slideIndex + 1) % slides.length;
  mostrarSlide(slideIndex);
}

setInterval(proximoSlide, 5000); // Troca a cada 5 segundos

indicators.forEach((indicator, i) => {
  indicator.addEventListener('click', () => {
    slideIndex = i;
    mostrarSlide(slideIndex);
  });
});

mostrarSlide(slideIndex);


// MODAL

document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('modal-1');
  const overlay = document.getElementById('overlay');


  if (!sessionStorage.getItem('modalShown')) {
    setTimeout(function() {
      overlay.style.display = 'block';
      modal.showModal();
      sessionStorage.setItem('modalShown', 'true');
    }, 1000);
  }

 
  function fecharmodal() {
    modal.close();
    overlay.style.display = 'none';
  }


  document.getElementById('close').addEventListener('click', fecharmodal);
});


document.getElementById('abrir-modal').addEventListener('click', function(event) {
  event.preventDefault(); 
  
  const modal = document.getElementById('modal-1');
  const overlay = document.getElementById('overlay');
  
  overlay.style.display = 'block'; 
  modal.showModal(); 
});
