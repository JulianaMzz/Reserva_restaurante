from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db
from models import Reserva
from datetime import datetime

app = Flask(__name__)
CORS(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Jujuba345!@localhost/restaurant_reservation"


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/restaurant_reservation'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/reservas", methods=["POST"])
def criar_reserva():
    try:
        dados = request.json

        # Converter data e hora
        data = datetime.strptime(dados.get("data"), "%Y-%m-%d").date()
        hora = datetime.strptime(dados.get("hora"), "%H:%M:%S").time()

        nova = Reserva(
            nome_cliente=dados.get("nome_cliente"),
            telefone_cliente=dados.get("telefone_cliente"),
            data=data,
            hora=hora,
            numero_pessoas=dados.get("numero_pessoas"),
            status=dados.get("status", "confirmada")
        )
        db.session.add(nova)
        db.session.commit()
        return jsonify({"mensagem": "Reserva criada com sucesso!"}), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/reservas", methods=["GET"])
def listar_reservas():
    reservas = Reserva.query.all()
    return jsonify([{
        "id": r.id,
        "nome_cliente": r.nome_cliente,
        "telefone_cliente": r.telefone_cliente,
        "data": str(r.data),
        "hora": str(r.hora),
        "numero_pessoas": r.numero_pessoas,
        "status": r.status
    } for r in reservas])


@app.route("/reservas/<int:id>", methods=["PUT"])
def atualizar_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    dados = request.json

    try:
        if "data" in dados:
            reserva.data = datetime.strptime(dados["data"], "%Y-%m-%d").date()
        if "hora" in dados:
            reserva.hora = datetime.strptime(dados["hora"], "%H:%M:%S").time()

        reserva.nome_cliente = dados.get("nome_cliente", reserva.nome_cliente)
        reserva.telefone_cliente = dados.get("telefone_cliente", reserva.telefone_cliente)
        reserva.numero_pessoas = dados.get("numero_pessoas", reserva.numero_pessoas)
        reserva.status = dados.get("status", reserva.status)

        db.session.commit()
        return jsonify({"mensagem": "Reserva atualizada com sucesso"})

    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route("/reservas/<int:id>", methods=["DELETE"])
def cancelar_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    reserva.status = "cancelada"
    db.session.commit()
    return jsonify({"mensagem": "Reserva cancelada com sucesso"})


if __name__ == "__main__":
    app.run(debug=True)