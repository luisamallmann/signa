
const app = document.getElementById('app');

app.innerHTML = `
  ${Header('Sobre')}
`;

initNavigation();

document.body.insertAdjacentHTML('beforeend', Footer());