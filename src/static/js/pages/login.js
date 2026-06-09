const app = document.getElementById('app');

// importando os componentes

app.innerHTML = `

  ${Header('Login')}

  `
initNavigation();

document.body.insertAdjacentHTML('beforeend', Footer())