from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ========== CONEXÃO COM MONGO ATLAS ==========
# ATENÇÃO: A senha do MongoDB está hardcoded na string de conexão.
# É recomendado usar variáveis de ambiente para a senha.
MONGO_URI = "mongodb+srv://evellyncarolyne12:@receitas.2dwrpuz.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["iot_database"]  # nome do banco
colecao_leituras = db["leituras"]

# ========== LIMITES (thresholds) ==========
thresholds = {
    "temp_max": 28.0,
    "umid_min": 40.0,
    "luz_min": 300
}

# ================= ROTAS =================

@app.route('/')
def home():
    return jsonify({
        "status": "API IoT Online (MongoDB conectado!)",
        "endpoints": {
            "POST /api/leituras": "Recebe dados dos sensores e salva no banco",
            "GET /api/leituras": "Retorna últimas leituras do MongoDB",
            "GET /api/thresholds": "Retorna limites atuais",
            "PUT /api/thresholds": "Atualiza limites"
        }
    })


# POST: Recebe dados e salva no banco
@app.route('/api/leituras', methods=['POST'])
def receber_leitura():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Nenhum dado enviado"}), 400
        
        # Adiciona timestamp
        dados["timestamp"] = datetime.now().isoformat()
        colecao_leituras.insert_one(dados)
        print(f"✅ Leitura salva no MongoDB: {dados}")
        return jsonify({
            "status": "sucesso",
            "mensagem": "Leitura salva com sucesso"
        }), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


# GET: Retorna últimas leituras
@app.route('/api/leituras', methods=['GET'])
def obter_leituras():
    try:
        limite = request.args.get('limite', default=5, type=int)
        docs = list(colecao_leituras.find().sort("_id", -1).limit(limite))
        for doc in docs:
            doc["_id"] = str(doc["_id"])  # Converter ObjectId para string
        return jsonify({
            "total": len(docs),
            "leituras": docs
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


# GET: Retorna thresholds
@app.route('/api/thresholds', methods=['GET'])
def obter_thresholds():
    return jsonify(thresholds), 200


# PUT: Atualiza thresholds
@app.route('/api/thresholds', methods=['PUT'])
def atualizar_thresholds():
    try:
        novos_limites = request.get_json()
        if not novos_limites:
            return jsonify({"erro": "Nenhum dado enviado"}), 400

        # Atualiza apenas chaves existentes
        for chave in thresholds:
            if chave in novos_limites:
                thresholds[chave] = novos_limites[chave]

        print(f"🔧 Thresholds atualizados: {thresholds}")
        return jsonify({
            "status": "sucesso",
            "mensagem": "Thresholds atualizados",
            "thresholds": thresholds
        }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


# ================= EXECUÇÃO =================
if __name__ == '__main__':
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 5001))
    print("🚀 Iniciando API IoT com MongoDB Atlas...")
    print(f"📍 Acesse: http://{host}:{port}")
    app.run(host=host, port=port, debug=True)
