#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from entityextractor.core.api import process_entities
import json
import sys
import logging
sys.stdout.reconfigure(encoding='utf-8')

# Thema: Geometrische Optik
text = "Geometrische Optik ist der Zweig der Optik, der Licht als Strahlen betrachtet und Phänomene wie Reflexion, Brechung und Totalreflexion untersucht."

# Vollständige JSON-Ausgabe
result = process_entities(
    text,
    {
        # === LLM PROVIDER SETTINGS ===
        "LLM_BASE_URL": "https://api.openai.com/v1",  # Base-URL für LLM API
        "MODEL": "gpt-4.1-mini",                      # LLM-Modell (empfohlen: gpt-4.1-mini, gpt-4o-mini)
        "OPENAI_API_KEY": None,                       # API-Key setzen oder aus Umgebungsvariable (Standard: None)
        "MAX_TOKENS": 16000,                          # Maximale Tokenanzahl pro Anfrage
        "TEMPERATURE": 0.2,                           # Sampling-Temperatur

        # === LANGUAGE SETTINGS ===
        "LANGUAGE": "de",           # Sprache der Verarbeitung (de oder en)

        # === TEXT PROCESSING SETTINGS ===
        "TEXT_CHUNKING": False,     # Text-Chunking aktivieren (False = ein LLM-Durchgang)
        "TEXT_CHUNK_SIZE": 1000,    # Chunk-Größe in Zeichen
        "TEXT_CHUNK_OVERLAP": 50,   # Überlappung zwischen Chunks in Zeichen

        # === ENTITY EXTRACTION SETTINGS ===
        "MODE": "generate",               # Modus: extract oder generate
        "MAX_ENTITIES": 10,              # Maximale Anzahl extrahierter Entitäten
        "ALLOWED_ENTITY_TYPES": "auto",  # Automatische Filterung erlaubter Entitätstypen
        "ENABLE_ENTITY_INFERENCE": False, # Implizite Entitätserkennung aktivieren

        # === RELATIONSHIP EXTRACTION AND INFERENCE ===
        "RELATION_EXTRACTION": False,         # Relationsextraktion aktivieren
        "ENABLE_RELATIONS_INFERENCE": False,  # Implizite Relationen aktivieren
        "MAX_RELATIONS": 15,                  # Maximale Anzahl Beziehungen pro Prompt

        # === CORE DATA SOURCE SETTINGS ===
        "USE_WIKIPEDIA": True,          # Wikipedia-Verknüpfung aktivieren (immer True)
        "USE_WIKIDATA": False,          # Wikidata-Verknüpfung aktivieren
        "USE_DBPEDIA": False,           # DBpedia-Verknüpfung aktivieren
        "DBPEDIA_USE_DE": False,        # Deutsche DBpedia nutzen (Standard: False = englische DBpedia)
        "ADDITIONAL_DETAILS": False,    # Zusätzliche Details aus allen Wissensquellen abrufen (mehr Infos aber langsamer)

        # === DBpedia Lookup API Fallback ===
        "DBPEDIA_LOOKUP_API": True,       # Fallback via DBpedia Lookup API aktivieren
        "DBPEDIA_SKIP_SPARQL": False,     # SPARQL-Abfragen überspringen und nur Lookup-API verwenden
        "DBPEDIA_LOOKUP_MAX_HITS": 5,     # Maximale Trefferzahl für Lookup-API
        "DBPEDIA_LOOKUP_CLASS": None,     # Optionale DBpedia-Ontology-Klasse für Lookup-API (derzeit ungenutzt)
        "DBPEDIA_LOOKUP_FORMAT": "xml",   # Response-Format: "json", "xml" (empfohlen) oder "beide" (maximale Details)

        # === COMPENDIUM SETTINGS ===
        "ENABLE_COMPENDIUM": True,           # Kompendium-Generierung aktivieren
        "COMPENDIUM_LENGTH": 8000,            # Anzahl der Zeichen für das Kompendium (ca. 4 A4-Seiten)
        "COMPENDIUM_EDUCATIONAL_MODE": True,  # Bildungsmodus für Kompendium aktivieren

        # === KNOWLEDGE GRAPH VISUALIZATION SETTINGS ===
        "ENABLE_GRAPH_VISUALIZATION": False,  # Statische PNG- und interaktive HTML-Ansicht aktivieren (erfordert RELATION_EXTRACTION=True)

        # === KNOWLEDGE GRAPH COMPLETION (KGC) ===
        "ENABLE_KGC": False,   # Knowledge-Graph-Completion aktivieren (Vervollständigung mit impliziten Relationen)
        "KGC_ROUNDS": 3,       # Anzahl der KGC-Runden

        # === STATISCHER GRAPH mit NetworkX-Layouts (PNG) ===
        "GRAPH_LAYOUT_METHOD": "spring",          # Layout: "kamada_kawai" (ohne K-/Iter-Param) oder "spring" (Fruchterman-Reingold)
        "GRAPH_LAYOUT_K": None,                   # (Spring-Layout) Ideale Kantenlänge (None=Standard)
        "GRAPH_LAYOUT_ITERATIONS": 50,            # (Spring-Layout) Anzahl der Iterationen
        "GRAPH_PHYSICS_PREVENT_OVERLAP": True,    # (Spring-Layout) Überlappungsprävention aktivieren
        "GRAPH_PHYSICS_PREVENT_OVERLAP_DISTANCE": 0.1,  # (Spring-Layout) Mindestabstand zwischen Knoten
        "GRAPH_PHYSICS_PREVENT_OVERLAP_ITERATIONS": 50, # (Spring-Layout) Iterationen zur Überlappungsprävention
        "GRAPH_PNG_SCALE": 0.30,                  # Skalierungsfaktor für statisches PNG-Layout (Standard 0.33)

        # === INTERAKTIVER GRAPH mit PyVis (HTML) ===
        "GRAPH_HTML_INITIAL_SCALE": 10,           # Anfangs-Zoom (network.moveTo scale): >1 rauszoomen, <1 reinzoomen

        # === TRAINING DATA COLLECTION SETTINGS ===
        "COLLECT_TRAINING_DATA": False,  # Trainingsdaten für Fine-Tuning sammeln
        "OPENAI_TRAINING_DATA_PATH": "entity_extractor_training_openai.jsonl",  # Pfad für Entitäts-Trainingsdaten
        "OPENAI_RELATIONSHIP_TRAINING_DATA_PATH": "entity_relationship_training_openai.jsonl",  # Pfad für Beziehungs-Trainingsdaten

        # === RATE LIMITER AND TIMEOUT SETTINGS ===
        "TIMEOUT_THIRD_PARTY": 15,       # Timeout für externe Dienste (Wikipedia, Wikidata, DBpedia)
        "RATE_LIMIT_MAX_CALLS": 3,       # Maximale Anzahl Aufrufe pro Zeitraum
        "RATE_LIMIT_PERIOD": 1,          # Zeitraum in Sekunden
        "RATE_LIMIT_BACKOFF_BASE": 1,    # Basiswert für exponentielles Backoff
        "RATE_LIMIT_BACKOFF_MAX": 60,    # Maximale Wartezeit bei Backoff
        "USER_AGENT": "EntityExtractor/1.0", # HTTP User-Agent-Header
        "WIKIPEDIA_MAXLAG": 5,           # Maxlag-Parameter für Wikipedia-API

        # === CACHING SETTINGS ===
        "CACHE_ENABLED": True,   # Caching global aktivieren oder deaktivieren
        "CACHE_DIR": __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__file__)), "cache"),    # Verzeichnis für Cache-Dateien innerhalb des Pakets (bei Bedarf erstellen)
        "CACHE_DBPEDIA_ENABLED": True,              # Caching für DBpedia-SPARQL-Abfragen aktivieren
        "CACHE_WIKIDATA_ENABLED": True,             # (Optional) Caching für Wikidata-API aktivieren
        "CACHE_WIKIPEDIA_ENABLED": True,            # (Optional) Caching für Wikipedia-API-Anfragen aktivieren

        # === LOGGING AND DEBUG SETTINGS ===
        "SHOW_STATUS": True,            # Statusmeldungen anzeigen
        "SUPPRESS_TLS_WARNINGS": True   # TLS-Warnungen unterdrücken
    }
)

# Compendium ausgeben
if "compendium" in result:
    comp = result["compendium"]
    print("=== Compendium ===")
    print(comp.get("text", ""))
    print("\nReferences:")
    for ref in comp.get("references", []):
        print(ref)

logging.info("Gebe Ergebnisse für Geometrische Optik Entitäten aus...")
filtered_entities = []
for ent in result.get("entities", []):
    wiki = ent.get("sources", {}).get("wikipedia", {})
    filtered_entities.append({
        "entity": ent.get("entity"),
        "url": wiki.get("url"),
        "image": wiki.get("image")
    })
print(json.dumps(filtered_entities, indent=2, ensure_ascii=False))
