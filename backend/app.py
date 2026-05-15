from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
# Habilitar CORS para permitir peticiones desde el frontend local
CORS(app) 

# Configuración paramétrica de la base de datos relacional
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inci.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Entidad de Dominio: Incidencia
class Incidencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False) 
    descripcion = db.Column(db.String(2000), nullable=False) 
    comentarios = db.Column(db.String(1000), nullable=True)  
    estado = db.Column(db.String(50), default="Incidencia registrada") 
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

# Endpoint POST: Registrar incidencia
@app.route('/api/incidencias', methods=['POST'])
def registrar_incidencia():
    data = request.get_json() 
    
    # Truncar cadenas de texto para evitar desbordamientos
    desc = data.get('descripcion', '')[:2000] 
    coment = data.get('comentarios', '')[:1000]
    
    nueva_incidencia = Incidencia(
        titulo=data.get('titulo')[:255],
        descripcion=desc,
        comentarios=coment
    )
    
    db.session.add(nueva_incidencia)
    db.session.commit()
    
    return jsonify({"mensaje": "Incidencia registrada con éxito", "id": nueva_incidencia.id}), 201

# Endpoint GET: Listar incidencias
@app.route('/api/incidencias', methods=['GET'])
def listar_incidencias():
    incidencias = Incidencia.query.all()
    resultado = [
        {
            "id": inc.id, 
            "titulo": inc.titulo, 
            "estado": inc.estado, 
            "fecha": inc.fecha.strftime('%Y-%m-%d')
        } for inc in incidencias
    ]
    return jsonify(resultado), 200

if __name__ == '__main__':
    # El sistema opera en ambientes de servidores estándares
    app.run(debug=True, port=5000)