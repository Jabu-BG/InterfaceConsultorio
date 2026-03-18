import re

def limpar_cpf(cpf: str) -> str:
    return re.sub(r'\D', '', cpf)

def cpf_valido(cpf: str) -> bool:
    cpf = limpar_cpf(cpf)

    if len(cpf) != 11:
        return False
    
    if cpf == cpf[0] * 11:
        return False
    
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = 0 if (soma * 10 % 11) >= 10 else (soma * 10 % 11)
    if d1 != int(cpf[9]):
        return False
    
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = 0 if (soma * 10 % 11) >= 10 else (soma * 10 % 11)
    return d2 == int(cpf[10])

def formatar_crm(crm: str) -> str:
    return crm.strip().upper()

def crm_valido(crm: str) -> bool:
    return bool(re.match(r'^CRM/[A-Z]{2}\s\d{4,6}$', formatar_crm(crm)))

def formatar_telefone(telefone: str) -> str:
    digitos = re.sub(r'\D', '', telefone)

    if len(digitos) == 11:
        return f"({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}"
    elif len(digitos) == 10:
        return f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"
    
    return telefone

def telefone_valido(telefone: str) -> bool:
    if not telefone:
        return True
    
    digitos = re.sub(r'\D', '', telefone)
    return len(digitos) in (10, 11)
