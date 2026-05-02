# MR Blackbox — AI Coding Cost Observability

<p align="center">
  <img src="https://img.shields.io/badge/Status-Phase_2_Completed-667eeb?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Local--First-Privacy_by_Design-green?style=for-the-badge" alt="Local First">
</p>

**MR Blackbox** è lo strumento locale di "scatola nera" progettato per misurare con precisione quanto costa costruire ogni singolo progetto (app, siti, SaaS) utilizzando agenti coder come **Claude Code**, **Gemini CLI** e **Codex CLI**.

Mentre i provider mostrano i costi a livello di account, MR Blackbox sposta il focus sul **progetto**, tracciando sessioni, token e sprechi direttamente nella tua directory di lavoro.

---

## 🚀 Perché MR Blackbox?

Chi sviluppa oggi con l'AI affronta problemi comuni:
- **Costi invisibili**: Non sai quanto ti è costata davvero quella specifica feature.
- **Dati frammentati**: Claude, Gemini e Codex espongono dati in formati diversi.
- **Mancanza di storico**: I prezzi cambiano, ma il costo della tua sessione passata non dovrebbe.
- **Token sprecati**: Non sai dove il contesto sta diventando troppo pesante o inefficiente.

MR Blackbox risponde a: *Quanto mi è costata davvero questa app?*

---

## ✨ Caratteristiche Principali

- 🕵️ **MR Transparent Tracing**: Attivalo con `mr on` e continua a programmare. Monitora silenziosamente i log dei coder senza interrompere il workflow.
- 📊 **MR Usage Dashboard**: Una dashboard TUI (Terminal UI) completa con breakdown per provider, tier di token e trend giornalieri.
- 💰 **MR Cost Engine**: Calcolo preciso basato su snapshot di pricing locali e tassi di cambio USD/EUR stabili.
- 🧊 **MR Cache Inspector**: Analizza l'efficienza della cache (Context Caching) e visualizza quanto stai risparmiando.
- 🛡️ **Privacy-First**: Tutti i dati, i transcript e i ledger rimangono locali nella cartella `.mr-blackbox/`.

---

## 🛠️ Installazione

```bash
# Clona il repository
git clone https://github.com/youruser/MRBlackbox.git
cd MRBlackbox

# Installa in modalità editabile
pip install -e .
```

---

## 📖 Guida Rapida

### 1. Inizializza il progetto
Crea il ledger locale per il tuo nuovo SaaS:
```bash
mr init --name "My Awesome SaaS" --type "webapp"
```

### 2. Attiva il monitoraggio
Fai partire la "scatola nera" prima di iniziare a programmare con Claude o Gemini:
```bash
mr on
```

### 3. Controlla i costi
In qualsiasi momento, visualizza il riepilogo o la dashboard completa:
```bash
mr costview  # Vista rapida
mr usage     # Dashboard completa
```

### 4. Analizza l'efficienza
Scopri quanto stai risparmiando grazie alla cache:
```bash
mr cache
```

---

## 🤖 Provider Supportati

| Provider | Stato | Livello Dettaglio |
| :--- | :--- | :--- |
| **Claude Code** | Stabile | **Exact** (Token tiers, Cache, Tools) |
| **Gemini CLI** | Beta | **Derived** (Tokens, Context Caching) |
| **Codex CLI** | Sperimentale | **Estimated** (Quota based) |

---

## 🗺️ Roadmap

- [x] **Phase 1**: Supporto Claude Code & Core Engine.
- [x] **Phase 2**: Integrazione Gemini CLI & Cache Inspector.
- [ ] **Phase 3**: Supporto Codex & Marker di affidabilità dei dati.
- [ ] **Phase 4**: MR Waste Score & Intelligence (suggerimenti per spendere meno).

---

## 📄 Licenza

Distribuito sotto Licenza MIT. Vedi `LICENSE` per maggiori informazioni.

---
<p align="center">
  Realizzato con ❤️ per la community di Indie Hackers e Sviluppatori AI.
</p>
