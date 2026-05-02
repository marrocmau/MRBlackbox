# MR Blackbox — AI Coding Cost Observability

<p align="center">
  <img src="https://img.shields.io/badge/Status-Phase_2_Completed-667eeb?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Local--First-Privacy_by_Design-green?style=for-the-badge" alt="Local First">
  <img src="https://img.shields.io/badge/Language-EN%20%7C%20IT-blue?style=for-the-badge" alt="Multi-language">
</p>

**MR Blackbox** is a local "black box" tool designed to accurately measure how much it costs to build every single project (apps, websites, SaaS) using AI agentic coders like **Claude Code**, **Gemini CLI**, and **Codex CLI**.

While providers show costs at an account level, MR Blackbox shifts the focus to the **project**, tracking sessions, tokens, and waste directly in your working directory.

---

## 🚀 Why MR Blackbox?

Developers building with AI today face common challenges:
- **Invisible costs**: You don't know exactly how much a specific feature cost.
- **Fragmented data**: Claude, Gemini, and Codex expose data in different formats.
- **Historical instability**: Prices change, but the cost of your past sessions shouldn't.
- **Wasted tokens**: You don't know where the context is becoming too heavy or inefficient.

MR Blackbox answers: *How much did this app really cost to build?*

---

## ✨ Key Features

- 🕵️ **MR Transparent Tracing**: Turn it on with `mr on` and keep coding. It silently monitors coder logs without interrupting your workflow.
- 📊 **MR Usage Dashboard**: A full TUI (Terminal UI) dashboard with provider breakdowns, token tiers, and daily trends.
- 💰 **MR Cost Engine**: Precise calculation based on local pricing snapshots and stable USD/EUR exchange rates.
- 🧊 **MR Cache Inspector**: Analyzes cache efficiency (Context Caching) and shows how much you are saving.
- 🛡️ **Privacy-First**: All data, transcripts, and ledgers stay local in the `.mr-blackbox/` folder.
- 🌍 **Multi-language**: Supports both **English** and **Italian**.

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/youruser/MRBlackbox.git
cd MRBlackbox

# Install in editable mode
pip install -e .
```

---

## 📖 Quick Start

### 1. Initialize the project
Create the local ledger for your new SaaS:
```bash
mr init --name "My Awesome SaaS" --type "webapp"
```

### 2. Activate tracing
Start the "black box" before you begin coding with Claude or Gemini:
```bash
mr on
```

### 3. Check costs
At any time, view the quick summary or the full dashboard:
```bash
mr costview  # Quick view
mr usage     # Full dashboard
```

### 4. Analyze efficiency
See how much you are saving thanks to the cache:
```bash
mr cache
```

---

## 🤖 Supported Providers

| Provider | Status | Detail Level |
| :--- | :--- | :--- |
| **Claude Code** | Stable | **Exact** (Token tiers, Cache, Tools) |
| **Gemini CLI** | Beta | **Derived** (Tokens, Context Caching) |
| **Codex CLI** | Experimental | **Estimated** (Quota based) |

---

## 🗺️ Roadmap

- [x] **Phase 1**: Claude Code Support & Core Engine.
- [x] **Phase 2**: Gemini CLI Integration & Cache Inspector.
- [ ] **Phase 3**: Codex Support & Data Reliability Markers.
- [ ] **Phase 4**: MR Waste Score & Intelligence (savings suggestions).

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
<p align="center">
  Built with ❤️ for the Indie Hackers and AI Developers community.
</p>
