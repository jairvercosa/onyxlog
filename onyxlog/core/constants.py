# -*- coding: ISO-8859-1 -*-
"""
Constantes da aplicação para uso geral
"""

#Parametro do fator 0.66
PAR_POND66 = "PAR_POND66"

#Parametro de tipo de meta padrão
PAR_TPMETA = "PAR_TPMETAPADRAO"

#Parametro que indica se oportunidade está fechada
PAR_TPOPFECHADA = "PAR_TPOPFECHADA"

#Meses
CONST_MESES = (
    ('01','Janeiro'),
    ('02','Fevereiro'),
    ('03','Março'),
    ('04','Abril'),
    ('05','Maio'),
    ('06','Junho'),
    ('07','Julho'),
    ('08','Agosto'),
    ('09','Setembro'),
    ('10','Outubro'),
    ('11','Novembro'),
    ('12','Dezembro'),
)

#Parametro que indica o fator de divisão do gráfico de prospecção do dashboard
PAR_FATORCOMPENS = "PAR_FATORCOMPENS"

#Parametro com id das temperaturas que serão utilizadas no dashboard
PAR_TEMPGRAF = "PAR_TEMPGRAF"

#Retorna a quantidade de dias que devem aparecer no gráfico de linearidade
PAR_DIASLINEARIDADE = "PAR_DIASLINEARIDADE"

#Id da funcao arquiteto
PAR_FUNCARQ = "PAR_FUNCARQ"

#id da funcao GPP
PAR_FUNCGPP = "PAR_FUNCGPP"

#Indica se usa fim de semana como dias uteis
PAR_SABADO = "PAR_SABADO"
PAR_DOMINGO = "PAR_DOMINGO"

#Dias da semana
DAYS_WEEK_BR = (
    (0,'Segunda-Feira'),
    (1,'Terça-Feira'),
    (2,'Quarta-Feira'),
    (3,'Quinta-Feira'),
    (4,'Sexta-Feira'),
    (5,'Sábado'),
    (6,'Domingo'),
)

#Opcoes para filtro de valores via select (combos)
OPT_VALS = [
    {
        "label": "todos",
        "ini":0,
        "end":0,
    },{
        "label": "0 até 50k",
        "ini":0,
        "end":50000,
    },{
        "label": "50k até 100k",
        "ini":50000,
        "end":100000,
    },{
        "label": "100k até 200k",
        "ini":100000,
        "end":200000,
    },{
        "label": "acima de 200k",
        "ini":200000,
        "end":0,
    }
]