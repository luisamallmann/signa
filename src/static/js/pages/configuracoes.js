const app = document.getElementById('app');

app.innerHTML = `
  ${Header('Configurações')}
`;

initNavigation();

document.body.insertAdjacentHTML('beforeend', Footer());