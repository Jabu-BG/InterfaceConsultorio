from datetime import date, time, datetime

def data_e_passada(data: date) -> bool:
    return data < date.today()

def data_e_futura(data: date) -> bool:
    return data > date.today()

def data_e_hoje_ou_futura(data: date) -> bool:
    return data >= date.today()

NOMES_DIA_SEMANA = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo",
}
 
ABREV_DIA_SEMANA = {
    0: "Seg", 1: "Ter", 2: "Qua",
    3: "Qui", 4: "Sex", 5: "Sáb", 6: "Dom",
}

def nome_dia_semana(data_ou_numero) -> str:
    if isinstance(data_ou_numero, date):
        numero = data_ou_numero.weekday()
    else:
        numero = data_ou_numero

    return NOMES_DIA_SEMANA.get(numero, "Dia inválido")

def abrev_dia_semana(data_ou_numero) -> str:
    if isinstance(data_ou_numero, date):
        numero = data_ou_numero.weekday()
    else:
        numero = data_ou_numero

    return ABREV_DIA_SEMANA.get(numero, "???")

def formatar_data(data: date) -> str:
    return data.strftime("%d/%m/%y")

def formatar_hora(hora: time) -> str:
    return hora.strftime("%H:%M")

def formatar_data_hora(data: date, hora: time) -> str:
    return f"{formatar_data(data)} às {formatar_hora(hora)}"

def str_para_date(texto: str) -> date | None:
    try:
        return datetime.strptime(texto, "%d/%m/%Y")
    except ValueError:
        return None
    
def str_para_time(texto: str) -> time | None:
    try:
        return datetime.strftime(texto, "%H:%M").time()
    except ValueError:
        return None