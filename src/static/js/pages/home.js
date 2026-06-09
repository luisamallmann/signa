const app = document.getElementById('app');

// importando os componentes

app.innerHTML = `

  ${Header('Home')}

  `
initNavigation();

document.body.insertAdjacentHTML('beforeend', Footer())