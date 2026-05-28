from datetime import datetime
from extensions import db

class Autor(db.Model):
    __tablename__ = 'autor'

    id_autor = db.Column(db.BigInteger, primary_key=True)
    nombre_completo = db.Column(db.String(255), nullable=False)
    nombre_firma = db.Column(db.String(255))
    pseudonimos = db.Column(db.Text)
    fecha_nacimiento = db.Column(db.String(100))
    anio_nacimiento = db.Column(db.Integer)
    lugar_nacimiento = db.Column(db.String(255))
    fecha_muerte = db.Column(db.String(100))
    anio_muerte = db.Column(db.Integer)
    lugar_muerte = db.Column(db.String(255))
    nacionalidad = db.Column(db.String(100))
    ocupacion = db.Column(db.String(255))
    genero = db.Column(db.String(50))
    lengua = db.Column(db.String(100))
    biografia = db.Column(db.Text)
    bne_identificador = db.Column(db.String(100), unique=True)
    url_datos_bne = db.Column(db.Text)
    viaf_id = db.Column(db.String(100))
    otros_identificadores = db.Column(db.Text)
    imagen_url = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id_autor,
            'nombre_completo': self.nombre_completo,
            'nombre_firma': self.nombre_firma,
            'pseudonimos': self.pseudonimos,
            'fecha_nacimiento': self.fecha_nacimiento,
            'anio_nacimiento': self.anio_nacimiento,
            'lugar_nacimiento': self.lugar_nacimiento,
            'fecha_muerte': self.fecha_muerte,
            'anio_muerte': self.anio_muerte,
            'lugar_muerte': self.lugar_muerte,
            'nacionalidad': self.nacionalidad,
            'ocupacion': self.ocupacion,
            'genero': self.genero,
            'lengua': self.lengua,
            'biografia': self.biografia,
            'bne_identificador': self.bne_identificador,
            'url_datos_bne': self.url_datos_bne,
            'viaf_id': self.viaf_id,
            'otros_identificadores': self.otros_identificadores,
            'imagen_url': self.imagen_url,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'actualizado_en': self.actualizado_en.isoformat() if self.actualizado_en else None
        }

