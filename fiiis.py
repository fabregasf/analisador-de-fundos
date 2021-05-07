import requests as req
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook as planilha
from flask import *
from wtforms import *
from sqlite import Sqlite as meudb
import matplotlib.pyplot as plt
from highcharts import Highchart

# Critérios de avaliação de fiis: valuation, técnica
class Fundos(object):
    
    
    # Gera gráficos com parametros passados do Dataset
    def graficos(lista,indices):
        
        for coluna in indices: 
            print(lista[coluna].values)            


            
        
    # Pega fundos selecionados
    # Gera o relatório no excel
    def val(fundos):
        info_fii={}
        lista_fiis=[]
        
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
                #print(soup)
                
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

                # procura = soup.find_all('table')[2].find_all('tr')[1].find_all('td')[1]
                # procura2 = soup.find_all('table')[1].find_all('tr')[17].find_all('td')[1]
                # Resultado anual contábil do ano anterior
                # info_fii['EBITDA_Ano_anterior']= procura.find('span').get_text()
                # info_fii['capex_hoje']= procura2.find('span').get_text()
                

                lista_fiis.append(info_fii)
                info_fii={}            
                meudb(x.replace(" ",""), "fiis")
                print(len(lista_fiis))

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
            




