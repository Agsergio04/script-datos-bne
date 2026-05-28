from datetime import datetime
from extensions import db

class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    
    id_proyecto = db.Column(db.BigInteger, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    cita = db.Column(db.Text)
    usuario_id = db.Column(db.BigInteger, db.ForeignKey('usuario.id_usuario'))
    laboratorio_id = db.Column(db.BigInteger, db.ForeignKey('laboratorio.id_laboratorio'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id_proyecto,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'cita': self.cita,
            'usuario_id': self.usuario_id,
            'laboratorio_id': self.laboratorio_id,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'actualizado_en': self.actualizado_en.isoformat() if self.actualizado_en else None
        }


# ============================================================
# RUTAS - SALUD Y ESTADO
# ============================================================
