import os
import json
from pathlib import Path

# Dictionary with translations
TRANSLATIONS = {
    "en": {
        "success": "Success!",
        "error": "Error:",
        "warning": "Warning:",
        "project_init": "Project {name} initialized in .mr-blackbox/",
        "project_exists": ".mr-blackbox directory already exists.",
        "not_project": "Not an MR Blackbox project. Run 'mr init' first.",
        "tracing_on": "MR Blackbox is now ON",
        "tracing_off": "MR Blackbox is now OFF",
        "tracing_already_on": "MR Blackbox is already ON",
        "tracing_already_off": "MR Blackbox is already OFF",
        "tracing_project": "Tracing project: {name}",
        "total_cost": "Total AI coding cost",
        "sessions_tracked": "Sessions tracked:",
        "tokens": "Tokens:",
        "cache_efficiency": "Cache Efficiency",
        "cache_read": "Cache Read Tokens",
        "cache_write": "Cache Write Tokens",
        "savings": "Estimated Savings",
        "provider": "Provider",
        "tier": "Tier",
        "ingested_session": "Ingested session:",
        "no_sessions_found": "No {provider} sessions found.",
    },
    "it": {
        "success": "Successo!",
        "error": "Errore:",
        "warning": "Attenzione:",
        "project_init": "Progetto {name} inizializzato in .mr-blackbox/",
        "project_exists": "La directory .mr-blackbox esiste già.",
        "not_project": "Non è un progetto MR Blackbox. Esegui prima 'mr init'.",
        "tracing_on": "MR Blackbox è ora ATTIVO (ON)",
        "tracing_off": "MR Blackbox è ora DISATTIVO (OFF)",
        "tracing_already_on": "MR Blackbox è già ATTIVO",
        "tracing_already_off": "MR Blackbox è già DISATTIVO",
        "tracing_project": "Monitoraggio progetto: {name}",
        "total_cost": "Costo totale AI coding",
        "sessions_tracked": "Sessioni tracciate:",
        "tokens": "Token:",
        "cache_efficiency": "Efficienza Cache",
        "cache_read": "Token letti da Cache",
        "cache_write": "Token scritti in Cache",
        "savings": "Risparmio stimato",
        "provider": "Provider",
        "tier": "Tier",
        "ingested_session": "Sessione importata:",
        "no_sessions_found": "Nessuna sessione {provider} trovata.",
    }
}

class I18n:
    def __init__(self, lang="en"):
        self.lang = lang if lang in TRANSLATIONS else "en"

    def t(self, key, **kwargs):
        text = TRANSLATIONS[self.lang].get(key, key)
        return text.format(**kwargs)

# Global i18n instance
# Language can be set via environment variable MR_LANG
_current_lang = os.getenv("MR_LANG", "en")
i18n = I18n(_current_lang)
