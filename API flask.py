from flask import Flask, request, json, Response
from flask_cors import CORS
import bd

app = Flask(__name__)
CORS(app)

viagens = [
    {"id":1, "local": "Destino 1"},
    {"id":2, "local": "Destino 2"},
    {"id":3, "local": "Destino 3"}
]

#Procurar todas as viagens
@app.route('/viagens', methods=['GET'])
def get_viagens():
    viagens = bd.session.query(bd.Viagens).order_by(bd.Viagens.id)
    viagens_json = [viagem.to_json() for viagem in viagens]
    return Response(json.dumps(viagens_json), status=200, mimetype="application/json")

#Procurar uma viagem especifica por ID
@app.route('/viagens/<int:destino_id>', methods=['GET'])
def get_viagem(destino_id):
    for viagem in viagens:
        if viagem['id']==destino_id:
            return viagem
    return {'error':'Local não encontrado'}

#Criando um cadastro de viagem
@app.route('/viagens', methods=['POST'])
def create_viagem():
    body = request.get_json()
    try:
        viagem = bd.Viagens(origem = body['origem'], 
                            destino =  body['destino'], 
                            valor =  body['valor'], 
                            urlfoto =  body['urlFoto'])
        bd.session.add(viagem)
        bd.session.commit()
        
        return Response(json.dumps(viagem.to_json()), status=201, mimetype="application/json")
    except Exception as e:
        print("Erro", e)
        return Response(status=400)
    

#Atualizando uma viagem
@app.route('/viagens/<int:destino_id>', methods=['GET'])
def update_viagem(destino_id):
    for viagem in viagens:
        if viagem['id']==destino_id:
            viagem['local']=request.json['local']
            return viagem
        return{'error':'Local não encontrado'}
    
#Deletando uma viagem
@app.route('/viagens/<int:destino_id>', methods=['DELETE'])
def delete_viagem(destino_id):
    bd.session.query(bd.Viagens).filter_by(id = destino_id).delete()
    bd.session.commit()
    return Response(status=200)
    
#corre o flask
if __name__ =='__main__':
    app.run(debug=True)