//alert("js funcionando") 

function CPF(input) {
    let value = input.value.replace(/\D/g, ''); 
    value = value.slice(0, 11);

    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');

    input.value = value;
}

function TEL(input) {
    let value = input.value.replace(/\D/g, '');
    value = value.slice(0, 11); 

    value = value.replace(/^(\d{2})(\d)/g, '($1) $2');
    value = value.replace(/(\d{5})(\d)/, '$1-$2');

    input.value = value;
}

function EMAIL(input){
    const email = input.value;
    const arroba = email.indexOf('@');
    const ponto = email.lastIndexOf('.');
    
    if(arroba < 1 || ponto < arroba + 2 || ponto === email.length - 1){
        input.setCustomValidity("Digite um e-mail válido.");
    }
    else {
        input.setCustomValidity("");
    }
}

//-----------------------------------------------------------------------------------------------------

//JS DA PAGINA MENU (utilizado todas as pag que tiverem o header!)

// MENU PARA MOBILE RESPONSIVO E SCROLL EFFECT
document.addEventListener('DOMContentLoaded', function() {
    let menuClique = document.getElementById('menuClique');
    let menuHeader = document.getElementById('menuHeader');
    let header = document.getElementById('header');
    const body = document.body; //Deixar o body como constante pois existe outra variavel body no codigo

        menuClique.addEventListener('click', function() {
        this.classList.toggle('active');
            menuHeader.classList.toggle('active');
        
        // BLOQUEIO DO SCROLL
        if (menuHeader.classList.contains('active')) {
            body.style.overflow = 'hidden';
        } else {
            body.style.overflow = '';
        }
    });
    
    // FECHAR MENU AO CLICAR NO HEADER
    let navLinks = document.querySelectorAll('nav ul li a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 900) {
                menuClique.classList.remove('active');
                    menuHeader.classList.remove('active');
                body.style.overflow = '';
            }
        });
    });

    // FECHAR MENU AO CLICAR FORA
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 900 && 
            !e.target.closest('header') && 
            menuHeader.classList.contains('active')) {
            menuClique.classList.remove('active');
            menuHeader.classList.remove('active');
            body.style.overflow = '';
        }
    });
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            menuClique.classList.remove('active');
            menuHeader.classList.remove('active');
            body.style.overflow = '';
        }
    });

    // SCROLL EFFECT (DIMINUIR HEADER AO DESCER A PAGINA)
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            header.style.padding = '0.5rem 1rem';
            header.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
        } else {
            header.style.padding = '1rem';
            header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        }
    });
});

// ACCORDIONS DE INFORMAÇÕES
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