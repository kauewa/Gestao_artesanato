from datetime import datetime



def dia_hoje(formato='%d/%m/%Y'):
    hoje = datetime.today()
    hoje = hoje.strftime(formato)
    return hoje

def esta_no_mes_atual(data):
    data_formatada = datetime.strptime(data, '%d/%m/%Y')
    data_atual = datetime.now()

    return data_formatada.month == data_atual.month and data_formatada.year == data_atual.year

        

            