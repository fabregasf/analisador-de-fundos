from flask import *
from flask import request
from wtforms import *
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from fiiis import Fundos as fundos
import requests
import json
from selenium import webdriver as driver
import time

DEBUG = False
SECRET_KEY = '87469976308fd14a2d0148247d441f2756b6176a'
app = Flask(__name__)
# Carregando bootstrap
Bootstrap(app)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = SECRET_KEY

class Main(FlaskForm):   

    series = None 
    fundos = fundos()

    @app.route('/resultado', methods=['GET','POST'])
    def resultado():
        titulo = "Retorno da pesquisa"
       
        valuation = request.form.getlist("fundo_select")
        nomefundo = request.form.get("fii")
        fundoss = any
        fundoss = nomefundo.split(',')  
            
        series = fundos.val(fundoss)            
        
        
        with open('fundos.json', 'w') as outfile:
            json.dump(series.to_json(orient="records"), outfile)
            
        indices = json.dumps(valuation)
        with open('indicadores.json', 'w') as outfile:
            json.dump(indices, outfile)
            
        
        return render_template('resultado.html', title=titulo, fundos=fundoss,valuation_sel=json.dumps(valuation))     

    

    @app.route("/", methods=['GET','POST'])
    def index():
            form = Main()
             # Lista com os tipos de indicadores de valuation
            itens_valuation = ['dividend_yield','pvp','EBITDA','Caixa livre']    

            return render_template('index.html', form=form, fundos=itens_valuation)
    
    # Rota virtual pra envio de dados no formato json    
    @app.route('/pipe', methods=['POST'])
    def pipe():
        payload = {}
        headers = {}
        
        with open('fundos.json') as json_file:
            data = json.load(json_file)

        return {"res":data}


if __name__ == "__main__":    
    app.run(host='127.0.0.1', port=5000,debug=True)
        

         
       
    
       
