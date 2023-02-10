from flask import Flask,render_template,request
from Dados import Pecas,Usuarios_permitidos as usp
import os

from Funcao import gerar_qr


app = Flask(__name__)

IMG_FOLDER = os.path.join('static')

app.config['UPLOAD_FOLDER'] = IMG_FOLDER

mail = None

@app.route("/")
@app.route("/homepage")
def homepage():
    return render_template("pagina_inicial.html")
    
@app.route("/result", methods=["POST","GET"])
def result():
	global mail
	output = request.form.to_dict()
	email = output["email"]
	mail = email
	senha = output["password"]
	if email in usp:
		password = usp[email][0]
		nome = usp[email][1]
		print(password,senha)
		if int(senha) == int(password):
			foto = os.path.join(app.config['UPLOAD_FOLDER'], 'images (51).jpeg')
			return render_template("terceira_pagina.html",name=nome,apresenta=foto)
		else:
			mensagem = f"Usuario : {email} Correto  Senha : {senha}	Esta invalida"
			return render_template("pagina_erro.html",mensagem = mensagem)
	else:
		mensagem = f"Usuario : {email} e Senha : {senha}	Não esta cadastrado no banco de dados"
		return render_template("pagina_erro.html",mensagem = mensagem)	
					
@app.route("/segundapag")
def segundapag():
	Flask_Logo = os.path.join(app.config['UPLOAD_FOLDER'], 'images (51).jpeg')
	return render_template("segunda_pagina.html",name="layon",senha=123,foto=Flask_Logo)


@app.route("/gerarqr",methods=["POST","GET"])
def gerarqr():
	output = request.form.to_dict()
	modelo = output["modelo"]
	peca = output["peca"]
	print(output)
	if gerar_qr(mail,modelo,peca)[0]:
		mensagem = "Codigo criado com sucesso"
		qr = os.path.join(app.config['UPLOAD_FOLDER'], "qrcode.jpg")
	else:
		mensagem = gerar_qr(mail,modelo,peca)[1]
		qr = os.path.join(app.config['UPLOAD_FOLDER'], 'images (52).jpeg')
		
	Flask_Logo = os.path.join(app.config['UPLOAD_FOLDER'], 'images (51).jpeg')
	return render_template("terceira_pagina.html",qrcode=qr,apresenta=Flask_Logo,mensagem=mensagem)
	
	
@app.route("/teste")
def teste():
	return render_template("teste.html",pecas = Pecas["linha3"])	

@app.route(f"/linha1")    
def mostra():
    return render_template("teste.html",pecas = Pecas)
				
if __name__ == "__main__":
    app.run(debug=True,port=5157)
