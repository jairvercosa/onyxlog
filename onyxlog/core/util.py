# -*- coding: ISO-8859-1 -*-
"""
Funções uteis para toda aplicação
"""

def getParam(param):
    """
    Retorna o valor de um parâmetro
    """
    from onyxlog.core.models.parametro import Parametro
    if not param:
        return None

    parametro = Parametro.objects.filter(nome=param)
    if parametro:
        return parametro[0].valor
    else:
        return None

def getParamByName(param, user_id):
    """
    Retorna o valor de um parâmetro filtrando filiais
    """
    from django.db.models import Q
    from onyxlog.core.models.parametro import Parametro

    if not param:
        return None

    parametro = Parametro.objects.filter(nome=param)

    if parametro:
        return parametro[0].valor
    else:
        return None

def format_number(numero):
    """
    Formata o número para o padrão brasileiro
    """

    try:
        contador = 0
        valor_str = ''
        num = numero.__str__()
        if '.' in num:
            valor, decimal = num.split('.')
        else:
            valor = num
            decimal = '00'

        if len(decimal) < 2:
            decimal = decimal + '0'

        tamanho = len(valor)
        while tamanho > 0:
            valor_str = valor_str + valor[tamanho-1]
            contador += 1
            if contador == 3 and tamanho > 1:
                valor_str = valor_str + ','
                contador = 0
            tamanho -= 1

        tamanho = len(valor_str)
        str_valor = ''
        while tamanho > 0:
            str_valor = str_valor + valor_str[tamanho-1]
            tamanho -= 1

        return "%s.%s" % (str_valor,decimal)
    except:
        return "Erro. Nao foi possivel converter o valor enviado."
