const app = document.getElementById('app');

app.innerHTML = `
  ${Header('Perfil')}
`;

initNavigation();

document.body.insertAdjacentHTML('beforeend', Footer());


// Editar perfil: o botão "Salvar alterações" só liga quando o nome mudou
const campoNome = document.getElementById('nome');
const btnSalvar = document.getElementById('btn-salvar');

if (campoNome && btnSalvar) {
  const atualizarBotao = () => {
    const mudou = campoNome.value.trim() !== campoNome.dataset.original.trim();
    btnSalvar.disabled = !mudou || campoNome.value.trim() === '';
  };
  campoNome.addEventListener('input', atualizarBotao);
  atualizarBotao();
}
