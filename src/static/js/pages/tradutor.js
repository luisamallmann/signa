const app = document.getElementById('app');

app.innerHTML = `

${Header('Tradutor')}

`
initNavigation();

document.body.insertAdjacentHTML('beforeend', Footer())