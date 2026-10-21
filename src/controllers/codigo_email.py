"""
Códigos de verificação de 6 dígitos (alterar senha / alterar email).

Os códigos ficam guardados na memória do servidor (não no navegador),
valem 10 minutos e aceitam no máximo 5 tentativas.

ENVIO POR EMAIL: para mandar o código de verdade, defina duas variáveis de
ambiente antes de rodar o app.py (Gmail com "senha de app"):
    set SIGNA_EMAIL=seuemail@gmail.com
    set SIGNA_EMAIL_SENHA=abcd efgh ijkl mnop
Sem elas, o código aparece no TERMINAL do Flask (bom para testar e para a feira).
"""
import os
import random
import smtplib
import time
from email.message import EmailMessage

VALIDADE_SEG = 10 * 60
MAX_TENTATIVAS = 5

_codigos = {}  # (proposito, email) -> {"codigo", "expira", "tentativas"}


def gerar_e_enviar(proposito, email):
    codigo = f"{random.SystemRandom().randint(0, 999999):06d}"
    _codigos[(proposito, email)] = {
        "codigo": codigo,
        "expira": time.time() + VALIDADE_SEG,
        "tentativas": 0,
    }
    _enviar(email, codigo, proposito)


def segundos_restantes(proposito, email):
    dados = _codigos.get((proposito, email))
    if not dados:
        return 0
    return max(0, int(dados["expira"] - time.time()))


def verificar(proposito, email, digitado):
    """Retorna None se o código estiver certo, ou a mensagem de erro."""
    dados = _codigos.get((proposito, email))
    if not dados or time.time() > dados["expira"]:
        return "O código expirou. Clique em Reenviar código."
    if dados["tentativas"] >= MAX_TENTATIVAS:
        return "Muitas tentativas. Clique em Reenviar código."
    if digitado != dados["codigo"]:
        dados["tentativas"] += 1
        return "Código incorreto. Confira e tente de novo."
    del _codigos[(proposito, email)]
    return None


def _enviar(email, codigo, proposito):
    assunto = "Seu código SIGNA"
    acao = "alterar sua senha" if proposito == "senha" else "confirmar seu novo email"
    texto = (f"Olá!\n\nSeu código para {acao} no SIGNA é: {codigo}\n\n"
             f"Ele expira em 10 minutos. Se não foi você, ignore este email.")

    usuario = os.environ.get("SIGNA_EMAIL")
    senha = os.environ.get("SIGNA_EMAIL_SENHA")
    if usuario and senha:
        try:
            msg = EmailMessage()
            msg["Subject"] = assunto
            msg["From"] = usuario
            msg["To"] = email
            msg.set_content(texto)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as smtp:
                smtp.login(usuario, senha)
                smtp.send_message(msg)
            return
        except Exception as e:
            print(f"[SIGNA] Não consegui enviar o email ({e}). Usando o terminal.")

    print("\n" + "=" * 50)
    print(f"[SIGNA] Código para {email}: {codigo}")
    print("=" * 50 + "\n", flush=True)
