from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ventas(db.Model):
    __tablename__ = 'Ventas'  # Asegúrate de que esto coincida con el nombre en tu base de datos
    id = db.Column(db.String, primary_key=True) #dasdasdadada
    precio_Fn = db.Column(db.Float, nullable=False)
    id_mesa = db.Column(db.String, nullable=False)
    estado = db.Column(db.Boolean, default=True)
    createdAt = db.Column(db.DateTime, default=db.func.current_timestamp())
