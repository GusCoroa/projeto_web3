alert("js funcionando")

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