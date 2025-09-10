from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db
from models import Reserva

app = Flask(__name__)
CORS(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Jujuba345!@localhost/restaurant_reservation"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/reservas", methods=["POST"])
def criar_reserva():
    dados = request.json
    nova = Reserva(
        nome_cliente=dados.get("nome_cliente"),
        telefone_cliente=dados.get("telefone_cliente"),
        data=dados.get("data"),
        hora=dados.get("hora"),
        numero_pessoas=dados.get("numero_pessoas")
    )
    db.session.add(nova)
    db.session.commit()
    return jsonify({"mensagem": "Reserva criada com sucesso!"}), 201


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

if __name__ == "__main__":
    app.run(debug=True)