from flask import Flask, request, json, Response
from flask_cors import CORS
import bdViagens
import bdUsuarios

app = Flask(__name__)
CORS(app)

@app.route('/viagem', methods=['GET'])
def get_viagem_by_destino():
    viagem = request.args.get('destino')
    viagens = bdViagens.session.query(bdViagens.Viagens).where(bdViagens.Viagens.destino.like(f"%{viagem}%"))
    viagens_json = [viagem.to_json() for viagem in viagens]
    return Response(json.dumps(viagens_json), status=200, mimetype="application/json")
    

#Procurar todas as viagens
@app.route('/viagens', methods=['GET'])
def get_viagens():
    viagens = bdViagens.session.query(bdViagens.Viagens).order_by(bdViagens.Viagens.id)
    viagens_json = [viagem.to_json() for viagem in viagens]
    return Response(json.dumps(viagens_json), status=200, mimetype="application/json")


#Criando um cadastro de viagem
@app.route('/viagens', methods=['POST'])
def create_viagem():
    body = request.get_json()
    try:
        viagem = bdViagens.Viagens(origem = body['origem'], 
                            destino =  body['destino'], 
                            valor =  body['valor'], 
                            urlfoto =  body['urlFoto'])
        bdViagens.session.add(viagem)
        bdViagens.session.commit()
        
        return Response(json.dumps(viagem.to_json()), status=201, mimetype="application/json")
    except Exception as e:
        print("Erro", e)
        return Response(status=400)
    

#Atualizando uma viagem
@app.route('/viagens/<int:destino_id>', methods=['PUT'])
def update_viagem(destino_id):
    body = request.get_json()
    try:
        viagem = bdViagens.session.query(bdViagens.Viagens).filter_by(id = destino_id).first()
        viagem.origem = body['origem']
        viagem.destino = body['destino']
        viagem.valor = body['valor']
        viagem.urlfoto = body['urlFoto']

        bdViagens.session.add(viagem)
        bdViagens.session.commit()

        return Response(json.dumps(viagem.to_json()), status=200, mimetype="application/json")
    except Exception as e:
        print("Erro", e)
        return Response(status=400)   

    
#Deletando uma viagem
@app.route('/viagens/<int:destino_id>', methods=['DELETE'])
def delete_viagem(destino_id):
    bdViagens.session.query(bdViagens.Viagens).filter_by(id = destino_id).delete()
    bdViagens.session.commit()
    return Response(status=200)
    

#Cadastro de usuario
@app.route('/usuarios', methods=['POST'])
def create_usuario():
    body = request.get_json()
    try:
        bdUsuarios.adicionar_usuario(body['nome'], body['sobrenome'], body['email'], body['senha'])
        return Response(status=201, mimetype="application/json")
    except Exception as e:
        retorno = {
            "mensagem": str(e)
        }
        return Response(json.dumps(retorno), status=400, mimetype="application/json")


#Procurar todos os usuarios
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = bdUsuarios.session.query(bdUsuarios.User).order_by(bdUsuarios.User.id)
    usuarios_json = [usuario.to_json() for usuario in usuarios]
    return Response(json.dumps(usuarios_json), status=200, mimetype="application/json")


#login
@app.route("/login", methods=['POST'])
def login():
    body = request.get_json()
    try:
        usuario = bdUsuarios.session.query(bdUsuarios.User).filter_by(email = body['email'], senha = body['senha']).first()
        if (usuario == None):
            retorno = {
                "mensagem": "Usuario ou senha inválidos."
            }

            return Response(json.dumps(retorno), status=400, mimetype="application/json")
        
        return Response(status=200, mimetype="application/json")
    except Exception as e:
        print("Erro", e)
        return Response(status=400)


#roda o flask
if __name__ == '__main__':
    app.run(debug=True)