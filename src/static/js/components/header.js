const NAV_LINKS = [
  { label: "Home", href: "/" },
  { label: "Tradutor", href: "/tradutor" },
  { label: "Como Funciona", href: "/como-funciona" },
  { label: "Sobre", href: "/sobre" },
  { label: "Contato", href: "/contato" },
]
function Header(pageAtiva = 'Home') {
  const linksHTML = NAV_LINKS.map(link => `
    <a href="${link.href}" class="nav-item ${link.label === pageAtiva ? 'active' : ''}" data-page="${link.label}">
      ${link.label}
      <span class="nav-underline"></span>
    </a>
  `).join("")

  return `
  <div class="nav-overlay" id="nav-overlay"></div>
    <header>
      <a href="/" class="logo">
        <img src="../static/assets/images/logo.png" alt="Signa Logo">
      </a>

      <nav id="nav-menu">
        ${linksHTML}
        <div class="nav-icons-mobile">
          <button class="icon-btn" aria-label="Notificações">${IconBell()}</button>
          <a href="/configuracoes" class="icon-btn" aria-label="Configurações">${IconSettings()}</a>
          <a href="/auth/login" class="icon-btn" aria-label="Perfil">${IconUser()}</a>
        </div>
      </nav>

      <div class="header-icons">
        <button class="icon-btn" aria-label="Notificações">${IconBell()}</button>
        <a href="/configuracoes" class="icon-btn" aria-label="Configurações">${IconSettings()}</a>
        <a href="/auth/login" class="icon-btn" aria-label="Perfil">${IconUser()}</a>
      </div>

      <button class="menu-toggle" id="menu-toggle" aria-label="Menu">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </header>
  `
}

function initNavigation() {
  const overlay = document.getElementById('nav-overlay')
  const links = document.querySelectorAll('.nav-item')
  const toggle = document.getElementById('menu-toggle')
  const nav = document.getElementById('nav-menu')

  links.forEach(link => {
    link.addEventListener('click', () => {
      links.forEach(l => l.classList.remove('active'))
      link.classList.add('active')
      toggle?.classList.remove('aberto')
      nav?.classList.remove('aberta')
      overlay?.classList.remove('ativo')        // ← remove
      document.body.classList.remove('menu-aberto')
    })
  })

  toggle?.addEventListener('click', () => {
    toggle.classList.toggle('aberto')
    nav.classList.toggle('aberta')
    overlay?.classList.toggle('ativo')          // ← toggle
    document.body.classList.toggle('menu-aberto')
  })

  overlay?.addEventListener('click', () => {
    toggle?.classList.remove('aberto')
    nav?.classList.remove('aberta')
    overlay?.classList.remove('ativo')
    document.body.classList.remove('menu-aberto')
  })
}
