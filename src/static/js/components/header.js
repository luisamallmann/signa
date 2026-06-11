const NAV_LINKS = [
  { label: "Home",          href: "/" },
  { label: "Tradutor",      href: "/tradutor" },
  { label: "Como Funciona", href: "/como-funciona" },
  { label: "Sobre",         href: "/sobre" },
  { label: "Contato",       href: "/contato" },
]
function Header(pageAtiva = 'Home') {
  const linksHTML = NAV_LINKS.map(link => `
    <a href="${link.href}" class="nav-item ${link.label === pageAtiva ? 'active' : ''}" data-page="${link.label}">
      ${link.label}
      <span class="nav-underline"></span>
    </a>
  `).join("")

  return `
    <header>
      <a href="/" class="logo">
        <img src="../static/assets/images/logo.png" alt="Signa Logo">
      </a>

      <nav>${linksHTML}</nav>

      <div class="header-icons">
        <button class="icon-btn" aria-label="Notificações">
          ${IconBell()}
        </button>
        <a href="../configuracoes" class="icon-btn" aria-label="Configurações">
          ${IconSettings()}
        </a>
        <a href="/auth/login" class="icon-btn" aria-label="Perfil">
          ${IconUser()}
        </a>
      </div>
    </header>
  `
}

function initNavigation() {
  const links = document.querySelectorAll('.nav-item')

  links.forEach(link => {
    link.addEventListener('click', (e) => {
      //e.preventDefault()

      links.forEach(l => l.classList.remove('active'))

      //link ativo só no clicado
      link.classList.add('active')
    })
  })
}
