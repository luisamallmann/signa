// Usado em alterar-senha.html e alterar-email.html

const app = document.getElementById('app');
app.innerHTML = `${Header('')}`;
initNavigation();
document.body.insertAdjacentHTML('beforeend', Footer());

// ---------- caixinhas do código (6 dígitos) ----------
const slots = document.querySelectorAll('.slot');

slots.forEach((slot, index) => {
  slot.addEventListener('input', () => {
    slot.value = slot.value.replace(/[^0-9]/g, '').slice(0, 1);
    if (slot.value !== '' && index < slots.length - 1) slots[index + 1].focus();
  });

  slot.addEventListener('keydown', (event) => {
    const permitidas = ['Backspace', 'Delete', 'Tab', 'ArrowLeft', 'ArrowRight', 'Enter'];
    const numero = /^[0-9]$/.test(event.key);
    if (!numero && !permitidas.includes(event.key) && !event.ctrlKey && !event.metaKey) {
      event.preventDefault();
    }
    if (event.key === 'Backspace' && slot.value === '' && index > 0) slots[index - 1].focus();
  });

  // colar o código inteiro de uma vez
  slot.addEventListener('paste', (event) => {
    event.preventDefault();
    const codigo = event.clipboardData.getData('text').replace(/[^0-9]/g, '').slice(0, slots.length);
    codigo.split('').forEach((n, i) => { slots[i].value = n; });
    slots[Math.min(codigo.length, slots.length - 1)].focus();
  });
});

// foca a primeira caixinha quando a etapa do código está aberta
const etapaCodigo = document.getElementById('step-codigo');
if (etapaCodigo && !etapaCodigo.hidden && slots.length) slots[0].focus();

// ---------- contagem regressiva (tempo vem do servidor) ----------
const contador = document.getElementById('contador');

if (contador && etapaCodigo && !etapaCodigo.hidden) {
  let restante = parseInt(contador.dataset.segundos || '0', 10);

  const mostrar = () => {
    if (restante <= 0) {
      clearInterval(intervalo);
      contador.parentElement.innerHTML = 'O código <span class="rosa">expirou</span>. Clique em Reenviar código.';
      return;
    }
    const m = Math.floor(restante / 60);
    const s = restante % 60;
    contador.textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    restante--;
  };

  const intervalo = setInterval(mostrar, 1000);
  mostrar();
}
