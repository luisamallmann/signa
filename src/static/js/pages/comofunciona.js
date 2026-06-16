// como-funciona.js
// Importa o header e footer, igual ao home.js

const app = document.getElementById('app');

app.innerHTML = `
  ${Header('Como Funciona')}
`;

initNavigation();

document.body.insertAdjacentHTML('beforeend', Footer());