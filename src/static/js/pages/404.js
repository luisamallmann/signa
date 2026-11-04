const app = document.getElementById('app');

app.innerHTML = `
  ${Header('')}
`;

initNavigation();

document.body.insertAdjacentHTML('beforeend', Footer());
