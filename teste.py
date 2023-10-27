import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QTextEdit, QVBoxLayout, QWidget
import requests
import json

class BotWhatsApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Bot WhatsApp")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.cnpj_input = QLineEdit()
        self.layout.addWidget(self.cnpj_input)

        self.consultar_button = QPushButton("Consultar CNPJ")
        self.consultar_button.clicked.connect(self.consultar_cnpj)
        self.layout.addWidget(self.consultar_button)

        self.mensagem_input = QLineEdit()
        self.layout.addWidget(self.mensagem_input)

        self.enviar_button = QPushButton("Enviar Mensagem")
        self.enviar_button.clicked.connect(self.enviar_mensagem)
        self.layout.addWidget(self.enviar_button)

        self.mensagens_output = QTextEdit()
        self.layout.addWidget(self.mensagens_output)

        self.central_widget.setLayout(self.layout)

        self.saudacao()

    def saudacao(self):
        self.mensagens_output.append("Olá! Sou seu bot. Digite o CNPJ abaixo para consultar.")

    def consultar_cnpj(self):
        cnpj = self.cnpj_input.text()
        try:
            if not cnpj.isdigit() or len(cnpj) != 14:
                self.mensagens_output.append("Erro: Dados errados. Digite apenas números.")
                return

            url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
            querystring = {"token": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX", "cnpj": cnpj, "plugin": "RF"}
            response = requests.get(url, params=querystring)
            response.raise_for_status()

            resp = json.loads(response.text)

            nome = resp.get("nome", "")
            logradouro = resp.get("logradouro", "")

            if nome and logradouro:
                resultado = f"Resultado da Consulta: \nNome: {nome}, \nLogradouro: {logradouro}"
                self.mensagens_output.append(resultado)
            else:
                self.mensagens_output.append("Erro: Dados não encontrados.")

        except requests.exceptions.RequestException as e:
            self.mensagens_output.append(f"Erro de Solicitação: {e}")
        except json.JSONDecodeError as e:
            self.mensagens_output.append(f"Erro de Decodificação JSON: {e}")
        except KeyError as e:
            self.mensagens_output.append(f"Erro de Chave Ausente: {e}")

    def enviar_mensagem(self):
        mensagem = self.mensagem_input.text()
        if mensagem:
            self.mensagens_output.append(f"Você enviou a mensagem: {mensagem}")
        else:
            self.mensagens_output.append("Erro: Digite uma mensagem para enviar.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BotWhatsApp()
    window.show()
    sys.exit(app.exec_())
