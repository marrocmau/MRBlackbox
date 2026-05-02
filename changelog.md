# Changelog — MR Blackbox

Tutte le modifiche rilevanti al progetto MR Blackbox saranno documentate in questo file.

## [0.1.0] - 2026-05-02
### Phase 1: MVP (Claude Code Support) - COMPLETATA ✅

#### Aggiunto
- **Core Engine**: Implementato `CostEngine` con supporto per token tiering (input, output, cache read/write).
- **Claude Adapter**: Sviluppato parser per i transcript di Claude Code (`.jsonl`) e rilevamento progetti.
- **CLI Commands**:
  - `mr init`: Inizializzazione del progetto locale in `.mr-blackbox/`.
  - `mr on`/`mr off`: Sistema di Transparent Tracing con background worker.
  - `mr status`: Visualizzazione dello stato del progetto e del worker.
  - `mr ingest`: Importazione manuale/automatica delle sessioni nel ledger.
  - `mr costview`: Dashboard sintetica dei costi.
  - `mr usage`: Dashboard avanzata con grafici ASCII e breakdown per tier.
- **Storage**: Sistema di persistenza basato su JSON (`ledger.json`, `project.json`) con supporto alla serializzazione datetime.
- **Worker**: Background process con polling fallback per il monitoraggio della history di Claude.

#### Corretto
- Fix per errore di serializzazione JSON dei metadati delle sessioni.
- Fix per `KeyError` nel calcolo dei totali del ledger.
- Aggiunto controllo di esistenza per `Optional` import in Typer.

## [0.2.0] - 2026-05-02
### Phase 2: Gemini CLI & Cache Efficiency - COMPLETATA ✅

#### Aggiunto
- **Gemini Adapter**: Supporto per l'ingest di sessioni Gemini CLI tramite file summary JSON.
- **Cost Engine**: Inseriti i prezzi per `gemini-1.5-pro` e `gemini-1.5-flash`, inclusa la gestione dei token in cache (Context Caching).
- **MR Cache Inspector**: Nuovo comando `mr cache` per analizzare l'efficienza della cache e il risparmio economico stimato.
- **Multi-Provider Support**: La dashboard `MR Usage` ora mostra il breakdown dei costi per provider (Claude vs Gemini).
- **Infrastruttura**: Supporto migliorato per la gestione di modelli diversi durante l'ingest.

#### Corretto
- Migliorata la robustezza del ledger nell'aggiornamento dei totali.

## [0.3.0] - 2026-05-02
### Phase 3: Codex & Reliability - COMPLETATA ✅

#### Aggiunto
- **Codex Adapter**: Supporto sperimentale per Codex CLI in modalità `estimated`.
- **Reliability Markers**: Introdotto il sistema di tracciamento dell'affidabilità (`exact`, `derived`, `estimated`) in tutti i modelli di costo e sessione.
- **Transparenza Dashboard**: La dashboard `MR Usage` ora mostra chiaramente il livello di affidabilità per ogni provider.
- **Codex Pricing**: Aggiunti prezzi stimati per i modelli Codex nel `CostEngine`.

#### Corretto
- Aggiornato il `CostEngine` per supportare diverse modalità di calcolo dinamiche.

## [1.0.0] - 2026-05-02
### Phase 4: Intelligence & Optimization - COMPLETATA ✅

#### Aggiunto
- **i18n Support**: Sistema di internazionalizzazione completo (Inglese/Italiano) per tutti i comandi e le dashboard, gestibile tramite variabile d'ambiente `MR_LANG`.
- **MR Waste Score**: Algoritmo per il calcolo dell'efficienza nell'uso dei token, basato sul riutilizzo della cache e sul mix di modelli.
- **MR Cost Replay**: Sistema di analisi proattiva che suggerisce percorsi di sviluppo alternativi (es. Gemini Flash per scansioni repo) per ridurre i costi fino al 50-60%.
- **Reporting System**: Comando `mr report` per generare report completi in formato Markdown, pronti per la condivisione o per l'archiviazione del progetto.
- **Intelligence Engine**: Nuovo modulo core dedicato all'analisi strategica dei dati del ledger.

#### Documentazione & Sicurezza
- **README**: Documentazione integrale in lingua inglese per un target internazionale.
- **Privacy (.gitignore)**: Configurazione rigorosa per escludere dati sensibili (.mr-blackbox/), specifiche di prodotto e piani di sviluppo dal repository pubblico.

#### Corretto
- Migliorata la formattazione dei pannelli CLI per una migliore leggibilità su terminali di diverse dimensioni.

---

## [Stabile] - Versione 1.0.0 rilasciata 🚀
Tutte le fasi della roadmap originale sono state completate con successo.
