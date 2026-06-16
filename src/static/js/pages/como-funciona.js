const app = document.getElementById('app');

app.innerHTML = `
  ${Header('Como Funciona')}
`;

initNavigation();

document.body.insertAdjacentHTML('beforeend', Footer());