function expandirTexto(button) {
    var texto = button.previousElementSibling;
    texto.classList.toggle("expandidotexto"); 

   
    if (texto.classList.contains("expandidotexto")) {
        button.textContent = "Ver menos";
    } else {
        button.textContent = "Ver mais";
    }
}
