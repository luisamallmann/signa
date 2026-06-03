const NAV_LINKS = ["Home", "Tradutor", "Como Funciona", "Sobre", "Contato"]

function Header() {
  const linksHTML = NAV_LINKS.map(link => `
    <a href="#" class="nav-item" data-page="${link}">
      ${link}
      <span class="nav-underline"></span>
    </a>
  `).join("")

  return `
    <header>
      <a href="/" class="logo">
        <img src="../../assets/images/logo.png" alt="Signa Logo">
      </a>

      <nav>${linksHTML}</nav>

      <div class="header-icons">
        <button class="icon-btn" aria-label="Notificações">
          ${IconBell()}
        </button>
        <button class="icon-btn" aria-label="Configurações">
          ${IconSettings()}
        </button>
        <button class="icon-btn" aria-label="Perfil">
          ${IconUser()}
        </button>
      </div>
    </header>
  `
}

function initNavigation() {
  const links = document.querySelectorAll('.nav-item')

  links.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault()

      links.forEach(l => l.classList.remove('active'))

      //link ativo só no clicado
      link.classList.add('active')
    })
  })

  //primeiro link ativo por padrão

  links[0].classList.add('active')
}