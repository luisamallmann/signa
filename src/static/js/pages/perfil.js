const app = document.getElementById('app');

app.innerHTML = `
  ${Header('Perfil')}
`;

initNavigation();

document.body.insertAdjacentHTML('beforeend', Footer());
