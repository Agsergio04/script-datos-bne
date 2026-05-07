#!/usr/bin/env python3
"""
Script de prueba rápida para extraer datos de ediciones de BNE
Sin necesidad de base de datos ni Docker
"""

import sys
import os

# Agregar backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from bne_scraper import BNEScraper
import json

def test_extractor():
    """Prueba el extractor con la URL del Quijote"""
    
    print("=" * 70)
    print("PRUEBA: Extractor de Ediciones BNE")
    print("=" * 70)
    
    # URL del Quijote
    url_quijote = "https://datos.bne.es/edicion/bimo0000659916.html"
    
    # Crear scraper (verify_ssl=False para resolver problemas de certificado en Windows)
    scraper = BNEScraper(verify_ssl=False)
    
    print(f"\n📄 URL a procesar:")
    print(f"   {url_quijote}")
    
    # Extraer datos
    print(f"\n⏳ Extrayendo datos...")
    datos = scraper.extraer_datos_edicion_html(url_quijote)
    
    if datos:
        print(f"\n✅ ÉXITO: Se extrajeron {len(datos)} campos\n")
        
        print("📋 Datos extraídos:")
        print("-" * 70)
        
        for clave, valor in datos.items():
            if isinstance(valor, list):
                if valor:
                    print(f"{clave.upper()}: {len(valor)} elementos")
                    for item in valor:
                        print(f"  - {item}")
            else:
                print(f"{clave.upper()}: {valor}")
        
        print("\n" + "=" * 70)
        print("📊 RESUMEN")
        print("=" * 70)
        print(f"Título:       {datos.get('titulo', 'N/A')}")
        print(f"Autor:        {datos.get('autor', 'N/A')}")
        print(f"Autor firma:  {datos.get('autor_firma', 'N/A')}")
        print(f"Editorial:    {datos.get('editorial', 'N/A')}")
        print(f"Lugar:        {datos.get('lugar_publicacion', 'N/A')}")
        print(f"Fecha:        {datos.get('fecha_publicacion', 'N/A')}")
        print(f"Descripción:  {datos.get('descripcion_fisica', 'N/A')}")
        print(f"Dimensiones:  {datos.get('dimensiones', 'N/A')}")
        print(f"Forma:        {datos.get('forma_contenido', 'N/A')}")
        print(f"Medio:        {datos.get('tipo_medio', 'N/A')}")
        
        # Guardar JSON
        json_file = 'quijote_datos.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Datos guardados en: {json_file}")
        
    else:
        print(f"\n❌ ERROR: No se pudo extraer información")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    try:
        test_extractor()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
