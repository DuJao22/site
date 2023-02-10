from Dados import Pecas ,Usuarios_permitidos
import qrcode
import numpy as np
import os

def gerar_qr(usuario,modelo,peca):
	num = np.random.randint(000,999)
	if usuario in Usuarios_permitidos:
		linha = Usuarios_permitidos[usuario][2]
		if modelo in Pecas[linha]:
			if peca in Pecas[linha][modelo]:
				cod = Pecas[linha][modelo][peca]
				if len(str(cod)) <= 21:
					print(f"provavelmente que o codgo esta incorreto ele tem {len(str(cod))} e para que codigo funcione e necessario que ele tenha no minimo 21 caracteres ")
					return False , texto
				else:
					arquivo = 'qrcode.jpg'
					if os.path.isfile(arquivo):
						os.remove(arquivo)
						print(f"removendo {arquivo}")
					codigo = f"{str(cod)[:21]}{num}23"
					print(f"existe a peca {peca} e o cod e {codigo}")
					qr = qrcode.QRCode()
					qr.add_data(codigo)
					qr.make()
					img = qr.make_image()
					img.save('static/qrcode.jpg')
					return True,img
			else:
				texto = f"Nao existe a peca {peca} no banco de dados"
				return False,texto
		else:
			texto = f"Nao existe o modelo : {modelo}"
			return False,texto
	else:
		texto = f"Nao existe o usuario {usuario} cadastrado no sistema"
		return False,texto
			
#gerar_qr("dujao","ago","roda")
