from datetime import date
import re


def formatar_cpf(cpf: str) -> str:
    digitos = re.sub(r'\D', '', cpf)
    if len(digitos) != 11:
        return cpf

    return f"{digitos[0:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}"


def ocultar_cpf(cpf: str) -> str:
    digitos = re.sub(r'\D', '', cpf)
    if len(digitos) != 11:
        return cpf

    return f"{digitos[0:3]}.***.**{digitos[8]}-{digitos[9:]}"


def formatar_nome(nome: str) -> str:
    minusculas = {"da", "de", "do", "das", "dos", "e"}
    palavras = nome.strip().split()

    resultado = [
        palavra.lower() if palavra.lower() in minusculas else palavra.title()
        for palavra in palavras
    ]

    if resultado:
        resultado[0] = resultado[0].title()

    return " ".join(resultado)


def nome_abreviado(nome: str, max_chars: int = 25) -> str:
    if len(nome) <= max_chars:
        return nome

    partes = nome.split()
    if len(partes) <= 2:
        return nome
    
    meio = [f"{p[0]}." if i not in (0, len(partes) - 1) else p
            for i, p in enumerate(partes)]

    return " ".join(meio)


def calcular_idade(data_nascimento: date) -> int:
    hoje = date.today()
    idade = hoje.year - data_nascimento.year

    aniversario_passou = (hoje.month, hoje.day) >= (data_nascimento.month, data_nascimento.day)

    if not aniversario_passou:
        idade -= 1

    return idade


def formatar_idade(data_nascimento: date) -> str:
    idade = calcular_idade(data_nascimento)
    return f"{idade} ano{'s' if idade != 1 else ''}"


ICONES_STATUS = {
    1: "🕐 Agendada",
    2: "✅ Realizada",
    3: "❌ Cancelada",
}


def formatar_status(status_id: int, descricao: str = None) -> str:
    if status_id in ICONES_STATUS:
        return ICONES_STATUS[status_id]

    return descricao or f"Status {status_id}"