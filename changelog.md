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

---

## [In Corso] - Phase 4: Intelligence & Optimization 🚀

- [ ] **MR Waste Score**: Algoritmo per il calcolo dello spreco di token.
- [ ] **MR Cost Replay**: Suggerimenti di routing alternativo per risparmio.
- [ ] **MR Report**: Generazione di report Markdown e HTML finali.
