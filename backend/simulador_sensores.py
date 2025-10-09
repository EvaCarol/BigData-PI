import requests
import random
import time

# URL do seu backend Flask (ajuste o IP se necessário)
URL_API = "http://172.26.37.69:5000/api/leituras"

# Função para gerar dados simulados
def gerar_dados_simulados(ciclo):
    if ciclo == 0:  # Excelente
        return {
            "temperatura": round(random.uniform(21.0, 23.0), 1),
            "umidade": round(random.uniform(50.0, 60.0), 1),
            "qualidadeAr": random.randint(200, 350),
            "nivelCO": random.randint(20, 50),
            "statusQualidade": "EXCELENTE"
        }
    elif ciclo == 1:  # Boa
        return {
            "temperatura": round(random.uniform(25.0, 27.0), 1),
            "umidade": round(random.uniform(60.0, 70.0), 1),
            "qualidadeAr": random.randint(400, 550),
            "nivelCO": random.randint(50, 100),
            "statusQualidade": "BOA"
        }
    elif ciclo == 2:  # Moderada
        return {
            "temperatura": round(random.uniform(29.0, 31.0), 1),
            "umidade": round(random.uniform(65.0, 75.0), 1),
            "qualidadeAr": random.randint(600, 750),
            "nivelCO": random.randint(100, 200),
            "statusQualidade": "MODERADA"
        }
    else:  # Ruim
        return {
            "temperatura": round(random.uniform(31.0, 33.0), 1),
            "umidade": round(random.uniform(75.0, 85.0), 1),
            "qualidadeAr": random.randint(800, 1000),
            "nivelCO": random.randint(200, 400),
            "statusQualidade": "RUIM"
        }

# Loop contínuo de simulação
if __name__ == "__main__":
    ciclo = 0
    while True:
        dados = gerar_dados_simulados(ciclo)
        print(f"📡 Enviando dados simulados: {dados}")

        try:
            resposta = requests.post(URL_API, json=dados, timeout=5)
            if resposta.status_code == 201:
                print(f"✅ Servidor respondeu: {resposta.status_code} - {resposta.json()}")
            else:
                print(f"⚠️ Servidor respondeu com erro: {resposta.status_code} - {resposta.text}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao enviar dados: {e}")

        # Alterna o cenário
        ciclo = (ciclo + 1) % 4
        time.sleep(5)

