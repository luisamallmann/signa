function Footer() {
    return `
    <footer><footer class="footer">
        <div class="footer-content">

            <div class="footer-brand">
                <a href="/" class="logo">
                    <img src="../static/assets/images/logo.png" alt="Signa" />
                </a>
                <p class="footer-desc">Quebrando barreiras de comunicação através da tecnologia e inovação.</p>
            </div>

            <div class="footer-col">
                <h4>Navegação</h4>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/src/pages/tradutor/">Tradutor</a></li>
                    <li><a href="/src/pages/como-funciona/">Como Funciona</a></li>
                    <li><a href="/src/pages/sobre/">Sobre</a></li>
                    <li><a href="/src/pages/contato/">Contato</a></li>
                </ul>
            </div>

            <div class="footer-col">
                <h4>Recursos</h4>
                <ul>
                    <li><a href="#">Documentação</a></li>
                    <li><a href="#">API</a></li>
                    <li><a href="#">Suporte</a></li>
                    <li><a href="#">Blog</a></li>
                </ul>
            </div>

            <div class="footer-col">
                <h4>Conecte-se</h4>
                <div class="footer-socials">
                    <a href="#" class="social-btn" aria-label="Email">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">
                            <path
                                d="M16.666 3.33325H3.33268C2.41221 3.33325 1.66602 4.07944 1.66602 4.99992V14.9999C1.66602 15.9204 2.41221 16.6666 3.33268 16.6666H16.666C17.5865 16.6666 18.3327 15.9204 18.3327 14.9999V4.99992C18.3327 4.07944 17.5865 3.33325 16.666 3.33325Z"
                                stroke="white" stroke-width="1.66667" stroke-linecap="round" stroke-linejoin="round" />
                            <path
                                d="M18.3327 5.83325L10.8577 10.5833C10.6004 10.7444 10.3029 10.8299 9.99935 10.8299C9.69575 10.8299 9.39829 10.7444 9.14102 10.5833L1.66602 5.83325"
                                stroke="white" stroke-width="1.66667" stroke-linecap="round" stroke-linejoin="round" />
                        </svg>
                    </a>
                    <a href="#" class="social-btn" aria-label="Instagram">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">
                            <g clip-path="url(#clip0_2008_1345)">
                                <path
                                    d="M14.166 1.66675H5.83268C3.5315 1.66675 1.66602 3.53223 1.66602 5.83341V14.1667C1.66602 16.4679 3.5315 18.3334 5.83268 18.3334H14.166C16.4672 18.3334 18.3327 16.4679 18.3327 14.1667V5.83341C18.3327 3.53223 16.4672 1.66675 14.166 1.66675Z"
                                    stroke="white" stroke-width="1.66667" stroke-linecap="round"
                                    stroke-linejoin="round" />
                                <path
                                    d="M13.3337 9.47501C13.4366 10.1685 13.3181 10.8769 12.9952 11.4992C12.6723 12.1215 12.1614 12.6262 11.5351 12.9414C10.9088 13.2566 10.1991 13.3663 9.5069 13.255C8.81468 13.1436 8.17521 12.8167 7.67944 12.321C7.18367 11.8252 6.85685 11.1857 6.74546 10.4935C6.63408 9.8013 6.74379 9.09159 7.05901 8.46532C7.37423 7.83905 7.8789 7.32812 8.50123 7.00521C9.12356 6.68229 9.83187 6.56383 10.5254 6.66667C11.2328 6.77158 11.8878 7.10123 12.3935 7.60693C12.8992 8.11263 13.2288 8.76757 13.3337 9.47501Z"
                                    stroke="white" stroke-width="1.66667" stroke-linecap="round"
                                    stroke-linejoin="round" />
                                <path d="M14.584 5.41675H14.5923" stroke="white" stroke-width="1.66667"
                                    stroke-linecap="round" stroke-linejoin="round" />
                            </g>
                            <defs>
                                <clipPath id="clip0_2008_1345">
                                    <rect width="20" height="20" fill="white" />
                                </clipPath>
                            </defs>
                        </svg>
                    </a>
                    <a href="#" class="social-btn" aria-label="LinkedIn">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">
                            <path
                                d="M13.334 6.66675C14.6601 6.66675 15.9318 7.19353 16.8695 8.13121C17.8072 9.0689 18.334 10.3407 18.334 11.6667V17.5001H15.0007V11.6667C15.0007 11.2247 14.8251 10.8008 14.5125 10.4882C14.1999 10.1757 13.776 10.0001 13.334 10.0001C12.892 10.0001 12.468 10.1757 12.1555 10.4882C11.8429 10.8008 11.6673 11.2247 11.6673 11.6667V17.5001H8.33398V11.6667C8.33398 10.3407 8.86077 9.0689 9.79845 8.13121C10.7361 7.19353 12.0079 6.66675 13.334 6.66675Z"
                                stroke="white" stroke-width="1.66667" stroke-linecap="round" stroke-linejoin="round" />
                            <path d="M4.99935 7.5H1.66602V17.5H4.99935V7.5Z" stroke="white" stroke-width="1.66667"
                                stroke-linecap="round" stroke-linejoin="round" />
                            <path
                                d="M3.33268 5.00008C4.25316 5.00008 4.99935 4.25389 4.99935 3.33341C4.99935 2.41294 4.25316 1.66675 3.33268 1.66675C2.41221 1.66675 1.66602 2.41294 1.66602 3.33341C1.66602 4.25389 2.41221 5.00008 3.33268 5.00008Z"
                                stroke="white" stroke-width="1.66667" stroke-linecap="round" stroke-linejoin="round" />
                        </svg>
                    </a>
                </div>
            </div>

        </div>

        <div class="footer-bottom">
            <span>© 2026 Signa. Todos os direitos reservados.</span>
        </div>
    </footer>
  `
}