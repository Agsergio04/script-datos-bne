"""Servicio de scraping: instancia compartida del scraper de datos.bne.es.

Aísla la dependencia del scraper (Dependency Inversion): los blueprints
dependen de este módulo, no de cómo se construye el `BNEScraper`.
verify_ssl=False resuelve problemas de certificados en Windows.
"""
from bne_scraper import BNEScraper

scraper = BNEScraper(verify_ssl=False)
