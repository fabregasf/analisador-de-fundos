import requests as req
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook as planilha
from flask import *
from wtforms import *
from sqlite import Sqlite as meudb
import matplotlib.pyplot as plt

# Critérios de avaliação de fiis: valuation, técnica
class Fundos(object):  
    # Atribuindo na classe como Nada
    lista_fiis=None;

    # Array de atributos da classe, inicializando
    def __init__(self):
        # Inicializando como array
        self.lista_fiis=[]


    # Pega fundos selecionados
    # Gera o relatório no excel
    def val(self, fundos):
        info_fii={}

        try:  
            for x in fundos:

                url = "%s%s"%("https://www.fundsexplorer.com.br/funds/",x.replace(" ",""))
                url2 = "%s%s"%("https://fiis.com.br/",x.replace(" ",""))
                url3 = "%s%s"%("https://statusinvest.com.br/fundos-imobiliarios/",x.replace(" ",""))
                #print("Debug:"+url)
                user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'            
                headers = {'User-Agent': user_agent}

                resp = req.get(url)
                response = resp.text
                soup=BeautifulSoup(response,'html.parser')
                
                # filtros
                tag2 = soup.select('span[class="indicator-value"]')    
                nomefundo = soup.find("title")
                        
                info_fii['Tick']=nomefundo.get_text()
                info_fii['liquidez_diaria']=tag2[0].get_text()
                info_fii['ultimo_rendimento']=tag2[1].get_text()
                info_fii['dividend_yield']=tag2[2].get_text()
                info_fii['patrimonio_liquido']=tag2[3].get_text()
                info_fii['valor_patrimonial']=tag2[4].get_text()
                info_fii['rentabilidade']=tag2[5].get_text()
                info_fii['pvp']=tag2[6].get_text()
                
                resp = req.get(url2)
                response = resp.text
                soup=BeautifulSoup(response,'html.parser')

                procura = soup.find_all('td')
                
                # Buscando ultimo resultado do fii
                info_fii['DataBaseAtual']=procura[0].get_text()
                info_fii['DataPagamento']=procura[1].get_text()
                info_fii['CotacaoBase']=procura[2].get_text()
                info_fii['DyMes']=procura[3].get_text()
                info_fii['rendimento_atual']=procura[4].get_text()                             

                resp = req.get(url3)
                response = resp.text
                soup=BeautifulSoup(response,'html.parser')
                # filtros
                caixa_empresa = soup.find(id="contabil-section")
                child = caixa_empresa.findChildren("tr")[12]
                child2 = caixa_empresa.findChildren("tr")[17]
                child3 = caixa_empresa.findChildren("tr")[107]
                
                info_fii['caixalivre_hoje']=child.find_all("span")[1].get_text()
                info_fii['caixalivre_12meses']=child.find_all("span")[7].get_text()
                info_fii['capex']=child2.find_all("span")[1].get_text()
                info_fii['lucroliquido']=child3.find_all("span")[1].get_text()
                child = caixa_empresa.findChildren("tr")[44]
                info_fii['caixa_receber_atual']=child.find_all("span")[1].get_text()
                info_fii['caixa_receber_12meses']=child.find_all("span")[7].get_text()
                
                self.lista_fiis.append(info_fii)
                info_fii={}            
                # meudb(x.replace(" ",""), "fiis")
                # print(len(self.lista_fiis))

        except HTTPError as e:
            print(e.status, e.reason)
        except URLError as e:
            print(e.reason)
        finally:
            # Gera planilha com valores
            tabela_fiis=pd.DataFrame(data=lista_fiis)
            print(tabela_fiis.columns)
            tabela_fiis.to_excel('Tabela_fiis.xlsx', 'Valuation', index=True, header=True, encoding='utf-8')
            return tabela_fiis
            




