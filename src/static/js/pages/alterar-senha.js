
const app = document.getElementById('app');

app.innerHTML = `
  ${Header('')}
`;

initNavigation();

document.body.insertAdjacentHTML('beforeend', Footer());

function irParaStep(nome){
  document.querySelectorAll('.step').forEach(s=> s.hidden = true);
  document.getElementById(`step-${nome}`).hidden = false;
}

const slots = document.querySelectorAll('.slot');

slots.forEach((slot, index) => {

  // Quando digitar
  slot.addEventListener('input', () => {

    // Remove tudo que não for número
    slot.value = slot.value.replace(/[^0-9]/g, '');

    // Garante que tenha apenas um caractere
    slot.value = slot.value.slice(0, 1);

    // Se digitou um número, vai para o próximo
    if (slot.value !== '' && index < slots.length - 1) {
      slots[index + 1].focus();
    }

  });


  // Teclas pressionadas
  slot.addEventListener('keydown', (event) => {

    // Permite:
    // números
    // Backspace
    // Delete
    // Tab
    // setas
    // Ctrl/Cmd + C, V, X, A

    const teclasPermitidas = [
      'Backspace',
      'Delete',
      'Tab',
      'ArrowLeft',
      'ArrowRight',
      'ArrowUp',
      'ArrowDown'
    ];

    const numero = /^[0-9]$/.test(event.key);

    const atalho =
      event.ctrlKey ||
      event.metaKey;

    if (
      !numero &&
      !teclasPermitidas.includes(event.key) &&
      !atalho
    ) {
      event.preventDefault();
    }


    // Backspace em campo vazio
    // volta para o campo anterior
    if (
      event.key === 'Backspace' &&
      slot.value === '' &&
      index > 0
    ) {
      slots[index - 1].focus();
    }

  });


  // Quando colar
  slot.addEventListener('paste', (event) => {

    event.preventDefault();

    // Pega o texto copiado
    const codigo = event.clipboardData
      .getData('text')
      .replace(/[^0-9]/g, '')
      .slice(0, slots.length);


    // Distribui os números
    codigo.split('').forEach((numero, i) => {
      slots[i].value = numero;
    });


    // Coloca o cursor no próximo campo
    const proximo = codigo.length;

    if (proximo < slots.length) {
      slots[proximo].focus();
    } else {
      slots[slots.length - 1].focus();
    }

  });

});

const contador = document.getElementById('contador');

let tempoRestante = 3 * 60; // 10 minutos em segundos

const intervalo = setInterval(() => {

    const minutos = Math.floor(tempoRestante / 60);
    const segundos = tempoRestante % 60;

    // Formata para 00:00
    contador.textContent =
        `${String(minutos).padStart(2, '0')}:${String(segundos).padStart(2, '0')}`;

    tempoRestante--;

    // Quando chegar a zero
    if (tempoRestante < 0) {

        clearInterval(intervalo);

        contador.textContent = 'Expirado';

        // Muda o texto inteiro
        contador.parentElement.innerHTML =
            'O código <span class="rosa">expirou</span>.';

    }

}, 1000);
