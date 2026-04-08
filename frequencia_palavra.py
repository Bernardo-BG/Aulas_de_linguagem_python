"""
Trabalho Prático 1.8 — Validação de Dados de Formulário com Regex e Decoradores
Autor: Bernardo
Tema: Sistema de validação modular para formulários web simulados
"""

import re
from functools import wraps


# =============================================================================
# MÓDULO 1 — FUNÇÕES DE VALIDAÇÃO COM EXPRESSÕES REGULARES
# =============================================================================

def validar_email(email: str) -> bool:
    """
    Valida o formato de um endereço de e-mail.
    Padrão aceito: nome@domínio.extensão
    Exemplo válido: bernardo@gmail.com
    """
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return bool(re.match(padrao, email))


def validar_telefone(telefone: str) -> bool:
    """
    Valida o formato de número de telefone angolano/brasileiro.
    Padrão aceito: (XX) XXXXX XXXX
    Exemplo válido: (94) 98765 4321
    """
    padrao = r'^\(\d{2}\) \d{5} \d{4}$'
    return bool(re.match(padrao, telefone))


def validar_data(data: str) -> bool:
    """
    Valida o formato de data no padrão DD-MM-AAAA.
    Também verifica faixas lógicas de dia (01-31) e mês (01-12).
    Exemplo válido: 07-04-2026
    """
    padrao = r'^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-\d{4}$'
    return bool(re.match(padrao, data))


def validar_nif(nif: str) -> bool:
    """
    Valida o formato do NIF (Número de Identificação Fiscal).
    Padrão aceito: exatamente 9 dígitos numéricos.
    Exemplo válido: 123456789
    """
    padrao = r'^\d{9}$'
    return bool(re.match(padrao, nif))


# Dicionário central de validações disponíveis (facilita modularidade)
VALIDACOES_DISPONIVEIS = {
    "email":    validar_email,
    "telefone": validar_telefone,
    "data":     validar_data,
    "nif":      validar_nif,
}


# =============================================================================
# MÓDULO 2 — DECORADOR DE VALIDAÇÃO
# =============================================================================

def validar_formulario(validacoes: dict):
    """
    Decorador de fábrica que recebe um dicionário de validações.

    Parâmetro:
        validacoes (dict): mapeia nome do campo → função de validação.
            Ex.: {"email": validar_email, "nif": validar_nif}

    Comportamento:
        - Itera sobre cada campo especificado em `validacoes`.
        - Aplica a função de validação correspondente ao valor recebido em kwargs.
        - Se houver falhas, levanta ValueError com relatório detalhado.
        - Se tudo for válido, executa a função decorada normalmente.
    """
    def decorador(func):
        @wraps(func)
        def wrapper(**kwargs):
            erros = {}

            for campo, funcao_validadora in validacoes.items():
                valor = kwargs.get(campo)

                # Campo ausente no envio
                if valor is None:
                    erros[campo] = f"Campo '{campo}' é obrigatório mas não foi informado."
                    continue

                # Campo presente mas com formato inválido
                if not funcao_validadora(valor):
                    erros[campo] = (
                        f"Valor inválido para '{campo}': '{valor}'. "
                        f"Verifique o formato esperado."
                    )

            # Bloqueia execução se houver erros
            if erros:
                mensagens = "\n".join(
                    f"  [{i+1}] {msg}" for i, msg in enumerate(erros.values())
                )
                raise ValueError(
                    f"\n{'='*55}\n"
                    f"  FORMULÁRIO REJEITADO — {len(erros)} erro(s) encontrado(s):\n"
                    f"{'='*55}\n"
                    f"{mensagens}\n"
                    f"{'='*55}"
                )

            # Todos os campos validados com sucesso
            return func(**kwargs)

        return wrapper
    return decorador


# =============================================================================
# MÓDULO 3 — FUNÇÃO DE PROCESSAMENTO DO FORMULÁRIO
# =============================================================================

@validar_formulario({
    "email":    validar_email,
    "telefone": validar_telefone,
    "data":     validar_data,
    "nif":      validar_nif,
})
def processar_cadastro(**dados_formulario):
    """
    Simula o processamento de um formulário de cadastro.
    Só é executada após todas as validações passarem com sucesso.
    """
    print("\n" + "=" * 55)
    print("  CADASTRO REALIZADO COM SUCESSO!")
    print("=" * 55)
    print("  Dados recebidos:")
    for campo, valor in dados_formulario.items():
        print(f"    {campo:<12}: {valor}")
    print("=" * 55 + "\n")
    return {"status": "sucesso", "dados": dados_formulario}


# =============================================================================
# MÓDULO 4 — TESTES
# =============================================================================

def executar_testes():
    print("\n" + "#" * 55)
    print("  TESTES DO SISTEMA DE VALIDAÇÃO")
    print("#" * 55)

    # --- CASO 1: Dados completamente válidos ---
    print("\n[TESTE 1] Dados válidos:")
    try:
        processar_cadastro(
            email="bernardo@gmail.com",
            telefone="(94) 98765 4321",
            data="07-04-2026",
            nif="123456789"
        )
    except ValueError as e:
        print(e)

    # --- CASO 2: Email inválido ---
    print("[TESTE 2] Email com formato inválido:")
    try:
        processar_cadastro(
            email="bernardo@",
            telefone="(94) 98765 4321",
            data="07-04-2026",
            nif="123456789"
        )
    except ValueError as e:
        print(e)

    # --- CASO 3: Múltiplos erros ---
    print("[TESTE 3] Vários campos inválidos:")
    try:
        processar_cadastro(
            email="nao-e-email",
            telefone="912345678",
            data="2026/04/07",
            nif="12345"
        )
    except ValueError as e:
        print(e)

    # --- CASO 4: Campo ausente ---
    print("[TESTE 4] Campo 'nif' ausente:")
    try:
        processar_cadastro(
            email="bernardo@outlook.com",
            telefone="(94) 98765 4321",
            data="01-01-2000"
        )
    except ValueError as e:
        print(e)

    # --- CASO 5: NIF com letras ---
    print("[TESTE 5] NIF com letras:")
    try:
        processar_cadastro(
            email="teste@dominio.co",
            telefone="(11) 91234 5678",
            data="15-06-1995",
            nif="12345678A"
        )
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    executar_testes()