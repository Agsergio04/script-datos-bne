#!/usr/bin/env python3
"""
Script de diagnóstico para analizar la estructura HTML de la página
"""

import requests
from bs4 import BeautifulSoup
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)

url = "https://datos.bne.es/edicion/bimo0000659916.html"

print("=" * 70)
print("DIAGNÓSTICO: Estructura HTML de página de edición BNE")
print("=" * 70)

print(f"\n📄 URL: {url}\n")

# Descargar página
response = requests.get(url, verify=False, timeout=30)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.content, 'html.parser')

# 1. Verificar que se descargó bien
print(f"✓ Página descargada ({len(response.content)} bytes)")

# 2. Buscar títulos
print(f"\n📌 TÍTULOS (h1, h2, h3):")
for tag in ['h1', 'h2', 'h3']:
    elems = soup.find_all(tag)
    for i, elem in enumerate(elems[:3]):
        text = elem.get_text(strip=True)[:80]
        print(f"  <{tag}> {text}")

# 3. Buscar tablas
print(f"\n📊 TABLAS:")
tables = soup.find_all('table')
print(f"  Encontradas: {len(tables)} tablas")

for idx, table in enumerate(tables[:2]):
    print(f"\n  --- Tabla {idx + 1} ---")
    rows = table.find_all('tr')
    for row in rows[:5]:
        cols = row.find_all(['td', 'th'])
        row_text = " | ".join([col.get_text(strip=True)[:30] for col in cols])
        print(f"    {row_text}")

# 4. Buscar listas de definición (dl)
print(f"\n📋 LISTAS DE DEFINICIÓN (dl):")
dls = soup.find_all('dl')
print(f"  Encontradas: {len(dls)} listas")

for idx, dl in enumerate(dls[:2]):
    print(f"\n  --- DL {idx + 1} ---")
    dts = dl.find_all('dt')[:5]
    dds = dl.find_all('dd')[:5]
    
    for dt, dd in zip(dts, dds):
        label = dt.get_text(strip=True)[:30]
        value = dd.get_text(strip=True)[:50]
        print(f"    {label}: {value}")

# 5. Buscar divs con class
print(f"\n📦 DIVS IMPORTANTES:")
important_classes = ['field', 'metadata', 'data', 'content', 'info', 'header', 'details']
for cls in important_classes:
    divs = soup.find_all('div', class_=lambda x: x and cls.lower() in x.lower())
    if divs:
        print(f"  .{cls}: {len(divs)} elementos")
        for div in divs[:2]:
            text = div.get_text(strip=True)[:60]
            print(f"    > {text}")

# 6. Buscar spans
print(f"\n💬 SPANS Y LABELS:")
spans = soup.find_all('span')
print(f"  Total spans: {len(spans)}")
for span in spans[:10]:
    text = span.get_text(strip=True)
    if len(text) > 5 and len(text) < 100:
        classes = span.get('class', [])
        print(f"  {text[:60]}")

# 7. Estructura general
print(f"\n🏗️ ESTRUCTURA GENERAL:")
print(f"  Body clases: {soup.body.get('class', [])}")
main_content = soup.find('main') or soup.find('article') or soup.find(id=lambda x: x and 'content' in x.lower() if x else False)
if main_content:
    print(f"  Main content encontrado: {main_content.name}")

# 8. Guardar HTML para análisis manual
html_file = 'page_structure.html'
with open(html_file, 'w', encoding='utf-8') as f:
    # Guardar con indentación para análisis
    f.write(soup.prettify())
print(f"\n💾 HTML guardado en: {html_file}")

print("\n" + "=" * 70)
print("PRÓXIMOS PASOS:")
print("=" * 70)
print("1. Abre 'page_structure.html' en un editor para analizar la estructura")
print("2. O visita la URL en el navegador y usa F12 Inspector")
print("3. Identifica dónde están los datos (tablas, listas, divs, etc.)")
print("4. Actualiza bne_scraper.py con los selectores correctos")
print("=" * 70)
