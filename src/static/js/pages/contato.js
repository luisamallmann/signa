// contato.js
// Importa o header e footer, igual ao home.js

const app = document.getElementById('app');

app.innerHTML = `
  ${Header('Contato')}
`;

initNavigation();

document.body.insertAdjacentHTML('beforeend', Footer());