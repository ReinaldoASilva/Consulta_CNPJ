import requests
import json
import tkinter as tk
from tkinter import messagebox



def consulta_cnpj():
    cnpj = entry_cnpj.get()
    try:
        # Verifica se o CNPJ contém apenas números e tem 14 dígitos
        if not cnpj.isdigit() or len(cnpj) != 14:
            messagebox.showerror("Erro", "Dados errados. Digite apenas números.")
            return

        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
        querystring = {"token":"XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX","cnpj": cnpj, "plugin":"RF"}
        response = requests.get(url, params=querystring)
        response.raise_for_status()

        resp = json.loads(response.text)

        nome = resp.get("nome", "")
        logradouro = resp.get("logradouro", "")

        messagebox.showinfo("Resultado da Consulta", f"Nome: {nome}\nLogradouro: {logradouro}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro de Solicitação", f"Erro de solicitação: {e}")
    except json.JSONDecodeError as e:
        messagebox.showerror("Erro de Decodificação JSON", f"Erro de decodificação JSON: {e}")
    except KeyError as e:
        messagebox.showerror("Erro de Chave Ausente", f"Erro de chave ausente: {e}")

# Cria a janela
root = tk.Tk()
root.title("Consulta de CNPJ")

# Cria rótulo e entrada para o CNPJ
label_cnpj = tk.Label(root, text="Digite o CNPJ:")
label_cnpj.pack()
entry_cnpj = tk.Entry(root)
entry_cnpj.pack()

# Cria botão para consulta
button_consultar = tk.Button(root, text="Consultar CNPJ", command=consulta_cnpj)
button_consultar.pack()

# Inicia a interface gráfica
root.mainloop()