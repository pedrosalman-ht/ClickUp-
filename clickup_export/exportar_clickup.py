import requests
import csv
from datetime import datetime

# Configurações de Acesso
API_TOKEN = "pk_112123497_TBUUIJM894TTDQ43WZEZ5RL21QXQEPH5"
TEAM_ID = "90131942220"

headers = {"Authorization": API_TOKEN}

def formatar_data(timestamp):
    if not timestamp: return ""
    try:
        return datetime.fromtimestamp(int(timestamp)/1000).strftime("%d/%m/%Y")
    except:
        return ""

all_tasks = []
page = 0

print("Exportando dados do ClickUp...")

while True:
    url = f"https://api.clickup.com/api/v2/team/{TEAM_ID}/task?page={page}&include_closed=true"
    response = requests.get(url, headers=headers)
    if response.status_code != 200: break

    data = response.json()
    tasks = data.get("tasks", [])
    if not tasks: break

    for task in tasks:
        # Prioridade Traduzida
        prioridade_data = task.get("priority")
        if prioridade_data:
            p_name = str(prioridade_data.get("priority")).lower()
            prioridade_map = {"urgent": "Urgente", "high": "Alta", "normal": "Normal", "low": "Baixa"}
            prioridade = prioridade_map.get(p_name, p_name.capitalize())
        else:
            prioridade = "Sem prioridade"

        # Organizando as colunas (Coluna H agora vai vazia)
        all_tasks.append([
            formatar_data(task.get("date_created")), # A: Data Criação
            task.get("list", {}).get("name", ""),    # B: SETOR
            task.get("name", ""),                    # C: Nome da Tarefa
            ", ".join([str(a.get("username")) for a in task.get("assignees", [])]), # D: Responsável
            task.get("status", {}).get("status", ""), # E: Status
            prioridade,                               # F: Prioridade
            formatar_data(task.get("due_date")),      # G: Data Vencimento
            ""                                        # H: PROBLEMAS (Vazio)
        ])
    page += 1

# Salvando o arquivo CSV
with open("dados_brutos_clickup.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(["Data de Criação","SETOR","Nome da Tarefa","Responsável","Status","Prioridade","Data de Vencimento","PROBLEMAS"])
    writer.writerows(all_tasks)

print(f"Exportação concluída! Coluna 'PROBLEMAS' está limpa para preenchimento.")