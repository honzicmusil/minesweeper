# statistiky hráčů
# pořadí nejlepších hráčských výsledků
from datetime import date
from pandas import DataFrame as df
from os import path



statistiky = []
hrac = dict(alias="hogo", skore="154", date="2020-11-25")
statistiky.append(hrac)
hrac = dict(alias="fogo", skore="20", date="2021-01-02")
statistiky.append(hrac)
hrac = dict(alias="hrusoun", skore="254", date="2020-11-25")
statistiky.append(hrac)
hrac = dict(alias="ala", skore="52", date="2020-06-21")
statistiky.append(hrac)
hrac = dict(alias="bena", skore="21", date="2020-09-30")
statistiky.append(hrac)
hrac = dict(alias="ovi", skore="574", date="2020-03-05")
statistiky.append(hrac)

df_statistiky = df(statistiky)
print(df_statistiky)
jason = df_statistiky.to_json()
print(jason)