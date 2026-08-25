function initNotificacoes() {

  const notificacoes = [
    {
      id: 1,
      titulo: 'Tradução concluída',
      desc: 'Sua última tradução foi processada com sucesso',
      tempo: '5 min atrás',
      lida: false,
      icone: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none">
        <polyline points="20 6 9 17 4 12" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>`
    },
    {
      id: 2,
      titulo: 'Nova atualização',
      desc: 'Melhorias na precisão do reconhecimento de sinais',
      tempo: '1 hora atrás',
      lida: false,
      icone: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="10" stroke="white" stroke-width="2"/>
        <line x1="12" y1="8" x2="12" y2="12" stroke="white" stroke-width="2" stroke-linecap="round"/>
        <line x1="12" y1="16" x2="12.01" y2="16" stroke="white" stroke-width="2" stroke-linecap="round"/>
      </svg>`
    },
    {
      id: 3,
      titulo: 'Bem-vindo ao Signa',
      desc: 'Aproveite todos os recursos da plataforma',
      tempo: '1 dia atrás',
      lida: true,
      icone: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="10" stroke="white" stroke-width="2"/>
        <line x1="12" y1="8" x2="12" y2="12" stroke="white" stroke-width="2" stroke-linecap="round"/>
        <line x1="12" y1="16" x2="12.01" y2="16" stroke="white" stroke-width="2" stroke-linecap="round"/>
      </svg>`
    }
  ];

  const naoLidas = notificacoes.filter(n => !n.lida).length;

  document.body.insertAdjacentHTML('beforeend', `
    <!-- Overlay escuro atrás do painel -->
    <div class="notif-overlay" id="notifOverlay"></div>

    <!-- Painel lateral -->
    <div class="notif-painel" id="notifPainel">

      <div class="notif-cabecalho">
        <div class="notif-cabecalho-texto">
          <h2>Notificações</h2>
          <span>${naoLidas} não ${naoLidas === 1 ? 'lida' : 'lidas'}</span>
        </div>
        <button class="notif-fechar" id="notifFechar">✕</button>
      </div>

      <div class="notif-lista" id="notifLista">
        ${notificacoes.map(n => `
          <div class="notif-card ${n.lida ? '' : 'nao-lida'}" data-id="${n.id}">
            <div class="notif-icone">${n.icone}</div>
            <div class="notif-info">
              <span class="notif-titulo">${n.titulo}</span>
              <span class="notif-desc">${n.desc}</span>
              <span class="notif-tempo">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                  <polyline points="12 6 12 12 16 14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                ${n.tempo}
              </span>
            </div>
          </div>
        `).join('')}
      </div>

      <div class="notif-rodape">
        <button class="notif-btn-marcar" id="notifMarcarTodas">
          Marcar todas como lidas
        </button>
      </div>

    </div>
  `);

  const btnNotif = document.querySelector('.icon-btn[data-notif]');
  if (btnNotif && naoLidas > 0) {
    btnNotif.style.position = 'relative';
    btnNotif.insertAdjacentHTML('beforeend', '<span class="notif-badge"></span>');
  }

  const overlay  = document.getElementById('notifOverlay');
  const painel   = document.getElementById('notifPainel');
  const btnFechar = document.getElementById('notifFechar');
  const btnMarcar = document.getElementById('notifMarcarTodas');

  function abrirPainel() {
    painel.classList.add('ativo');
    overlay.classList.add('ativo');
    document.body.style.overflow = 'hidden'; // impede scroll da página
  }

  function fecharPainel() {
    painel.classList.remove('ativo');
    overlay.classList.remove('ativo');
    document.body.style.overflow = '';
  }

  const iconeNotif = document.querySelector('.icon-btn[data-notif]')
                  || document.querySelector('.header-icons .icon-btn');

  if (iconeNotif) {
    iconeNotif.addEventListener('click', abrirPainel);
  }

  btnFechar.addEventListener('click', fecharPainel);

  overlay.addEventListener('click', fecharPainel);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') fecharPainel();
  });

  btnMarcar.addEventListener('click', () => {
    document.querySelectorAll('.notif-card.nao-lida').forEach(card => {
      card.classList.remove('nao-lida');
    });
    document.querySelector('.notif-cabecalho-texto span').textContent = '0 não lidas';

    const badge = document.querySelector('.notif-badge');
    if (badge) badge.remove();
  });
}