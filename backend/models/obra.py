from datetime import datetime
from extensions import db

class Obra(db.Model):
    __tablename__ = 'obra'
    
    id_obra = db.Column(db.BigInteger, primary_key=True)
    titulo = db.Column(db.String(500), nullable=False)
    tipo_publicacion = db.Column(db.String(100))
    autor_firma = db.Column(db.String(255))
    nombre_autor = db.Column(db.String(255))
    id_autor = db.Column(db.BigInteger, db.ForeignKey('autor.id_autor'), nullable=True)
    anio = db.Column(db.Integer)
    enlace = db.Column(db.Text, unique=True)
    fecha = db.Column(db.Date)
    dia = db.Column(db.Integer)
    mes = db.Column(db.Integer)
    num_periodico = db.Column(db.String(100))
    variante_titulo = db.Column(db.String(255))
    pseudonimos_autor = db.Column(db.String(255))
    tema_principal = db.Column(db.String(255))
    paginas = db.Column(db.String(500))
    como_citar = db.Column(db.Text)
    imprenta = db.Column(db.String(255))
    lugar_impresion = db.Column(db.String(255))
    imagen_url = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id_obra,
            'titulo': self.titulo,
            'tipo_publicacion': self.tipo_publicacion,
            'autor_firma': self.autor_firma,
            'nombre_autor': self.nombre_autor,
            'id_autor': self.id_autor,
            'anio': self.anio,
            'enlace': self.enlace,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'dia': self.dia,
            'mes': self.mes,
            'num_periodico': self.num_periodico,
            'variante_titulo': self.variante_titulo,
            'pseudonimos_autor': self.pseudonimos_autor,
            'tema_principal': self.tema_principal,
            'paginas': self.paginas,
            'como_citar': self.como_citar,
            'imprenta': self.imprenta,
            'lugar_impresion': self.lugar_impresion,
            'imagen_url': self.imagen_url,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'actualizado_en': self.actualizado_en.isoformat() if self.actualizado_en else None
        }
    
    def to_dict_detallado(self):
        """Devuelve información completa incluyendo datos especializados"""
        resultado = self.to_dict()
        
        # Obtener datos especializados según tipo
        from sqlalchemy import text
        
        tipo = self.tipo_publicacion.lower() if self.tipo_publicacion else ''
        
        # Buscar en tabla especializada correspondiente
        if 'teatro' in tipo or 'dramático' in tipo.lower():
            teatro = db.session.execute(
                text("SELECT fuente_procedencia, resumen, modalidad_teatro, otros_motivos FROM teatro WHERE id_obra = :id"),
                {'id': self.id_obra}
            ).fetchone()
            if teatro:
                resultado['especializado'] = {
                    'tipo_especifico': 'Teatro',
                    'fuente_procedencia': teatro[0],
                    'resumen': teatro[1],
                    'modalidad': teatro[2],
                    'otros_motivos': teatro[3]
                }
        
        elif 'novela' in tipo or 'prosa' in tipo.lower():
            novela = db.session.execute(
                text("SELECT fragmento_donde_aparece, modalidad_novela, tipo_de_ubicacion, aspectos_formales, observaciones FROM novela WHERE id_obra = :id"),
                {'id': self.id_obra}
            ).fetchone()
            if novela:
                resultado['especializado'] = {
                    'tipo_especifico': 'Novela',
                    'fragmento': novela[0],
                    'modalidad': novela[1],
                    'tipo_ubicacion': novela[2],
                    'aspectos_formales': novela[3],
                    'observaciones': novela[4]
                }
        
        elif 'periódico' in tipo or 'prensa' in tipo.lower():
            periodico = db.session.execute(
                text("SELECT modalidad_periodico, num_periodico, fragmento_donde_aparece FROM periodico WHERE id_obra = :id"),
                {'id': self.id_obra}
            ).fetchone()
            if periodico:
                resultado['especializado'] = {
                    'tipo_especifico': 'Periódico',
                    'modalidad': periodico[0],
                    'numero': periodico[1],
                    'fragmento': periodico[2]
                }
        
        elif 'poesía' in tipo or 'poema' in tipo.lower() or 'verso' in tipo.lower():
            poesia = db.session.execute(
                text("SELECT aspectos_formales, resumen, fuente_procedencia, modalidad_poesia FROM poesia WHERE id_obra = :id"),
                {'id': self.id_obra}
            ).fetchone()
            if poesia:
                resultado['especializado'] = {
                    'tipo_especifico': 'Poesía',
                    'aspectos_formales': poesia[0],
                    'resumen': poesia[1],
                    'fuente_procedencia': poesia[2],
                    'modalidad': poesia[3]
                }
        
        elif 'música' in tipo or 'música impresa' in tipo.lower():
            musica = db.session.execute(
                text("SELECT resumen, aspectos_formales, observaciones, modalidad_musica_impresa FROM musica_impresa WHERE id_obra = :id"),
                {'id': self.id_obra}
            ).fetchone()
            if musica:
                resultado['especializado'] = {
                    'tipo_especifico': 'Música Impresa',
                    'resumen': musica[0],
                    'aspectos_formales': musica[1],
                    'observaciones': musica[2],
                    'modalidad': musica[3]
                }
        
        return resultado


