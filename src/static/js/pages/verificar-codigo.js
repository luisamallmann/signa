
const app = document.getElementById('app');

app.innerHTML = `
  ${Header('Configurações')}
`;

initNavigation();

document.body.insertAdjacentHTML('beforeend', Footer());


const digitos = document.querySelectorAll('.codigo-digito');

if (digitos.length > 0) {
  digitos.forEach((input, i) => {
    input.addEventListener('input', () => {
      input.value = input.value.replace(/\D/g, '');
      if (input.value && i < digitos.length - 1) {
        digitos[i + 1].focus();
      }
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace' && !input.value && i > 0) {
        digitos[i - 1].focus();
      }
    });
  });

  digitos[0].focus();
}