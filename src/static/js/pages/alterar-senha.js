
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

document.getElementById('form-email').addEventListener('submit', async (e) =>{
  e.preventDefault();
  dadodFluxo.email = document.getElementById('input-email').ariaValueMax;
  irParaStep('codigo')
}) 
