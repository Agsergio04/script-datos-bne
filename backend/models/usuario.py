from datetime import datetime
from extensions import db

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    id_usuario = db.Column(db.BigInteger, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(255), unique=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id_usuario,
            'nombre': self.nombre,
            'email': self.email,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'actualizado_en': self.actualizado_en.isoformat() if self.actualizado_en else None
        }


