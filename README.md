# MR Blackbox — AI Coding Cost Observability

<p align="center">
  <img src="https://img.shields.io/badge/Status-v1.0.0--Stable-667eeb?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Local--First-Privacy_by_Design-green?style=for-the-badge" alt="Local First">
  <img src="https://img.shields.io/badge/Language-EN%20%7C%20IT-blue?style=for-the-badge" alt="Multi-language">
</p>

**MR Blackbox** is a local "black box" for your AI development. It accurately measures how much it costs to build every single project (apps, websites, SaaS) using AI agentic coders like **Claude Code**, **Gemini CLI**, and **Codex CLI**.

While cloud providers show costs at an account level, MR Blackbox focuses on the **Project Ledger**, tracking sessions, tokens, cache efficiency, and waste directly in your working directory.

---

## 🚀 Why MR Blackbox?

Developers building with AI agentic tools face common challenges:
- **Invisible costs**: No immediate feedback on how much a specific task or feature cost.
- **Data fragmentation**: Different tools (Claude vs Gemini) use different metrics and logs.
- **Cache Blindness**: You don't know if your context caching is actually working or saving you money.
- **Historical drift**: API prices change, but the cost of your past development sessions should remain fixed in your history.

MR Blackbox answers: **"How much did this specific app really cost to build?"**

---

## ✨ Key Features

- 🕵️ **MR Transparent Tracing**: Turn it on once (`mr on`) and keep coding. It silently monitors your coder's logs in the background without affecting performance.
- 📊 **MR Usage Dashboard**: High-fidelity TUI (Terminal UI) showing provider splits, token tiers, and daily spending trends.
- 💰 **MR Cost Engine**: Precise cost calculation using local pricing snapshots and stable USD/EUR conversion.
- 🧊 **MR Cache Inspector**: Deep-dive into Context Caching efficiency to see your real-world savings.
- 🧠 **MR Intelligence**: Calculate your **Waste Score** and use **Cost Replay** to find cheaper development routes.
- 🛡️ **Privacy-First**: No data leaves your machine. Transcripts, logs, and ledgers stay in the `.mr-blackbox/` folder.
- 🌍 **Native i18n**: Full support for **English** and **Italian**.

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

### 1. Initialize your project
Create the local cost ledger for your project:
```bash
mr init --name "My SaaS App" --type "webapp"
```

### 2. Activate the Blackbox
Start tracing before you launch your AI coder (Claude/Gemini):
```bash
mr on
```

### 3. Check your project cost
At any time, view your spending:
```bash
mr costview  # Compact view
mr usage     # Full observability dashboard
```

---

## 🕹️ Command Reference

| Command | Description |
| :--- | :--- |
| `mr init` | Setup the `.mr-blackbox` infrastructure in the current folder. |
| `mr on` | Start the background worker (Transparent Tracing). |
| `mr off` | Stop the background worker. |
| `mr status` | Check if tracing is active and view project metadata. |
| `mr ingest` | Manually import the latest detected session. |
| `mr usage` | Launch the full ASCII dashboard. |
| `mr cache` | View cache efficiency and estimated savings. |
| `mr waste` | Calculate the project **Waste Score** (0-100). |
| `mr replay` | Simulate alternative (cheaper) routing strategies. |
| `mr report` | Generate a shareable Markdown report in `.mr-blackbox/reports/`. |

---

## 🤖 Supported Providers & Reliability

| Provider | Integration | Reliability | Data Level |
| :--- | :--- | :--- | :--- |
| **Claude Code** | Stable | **Exact** | Full token tiers, Cache Read/Write, Tool usage. |
| **Gemini CLI** | Beta | **Derived** | Prompt/Candidate tokens, Context Caching. |
| **Codex CLI** | Experimental | **Estimated** | Request/Quota based estimation. |

---

## 🧠 Intelligence & Optimization

### MR Waste Score
Run `mr waste` to see how efficiently you are using AI. A high score (60+) indicates:
- Repeated context loading (poor cache usage).
- Using expensive models (Sonnet) for simple tasks (file scanning).
- Oversized transcripts being sent back into the context.

### MR Cost Replay
Run `mr replay` to see how much you *could* have saved. It analyzes your project history and suggests an optimized route (e.g., *"Using Gemini Flash for repo scans would have saved you 45%"*).

---

## 🌍 Language Selection (i18n)

MR Blackbox detects your language, but you can override it using the `MR_LANG` environment variable:

```bash
# Force Italian
export MR_LANG=it
mr usage

# Force English
export MR_LANG=en
mr usage
```

---

## 🛡️ Privacy & Storage

All data is stored in the `.mr-blackbox/` hidden directory within your project:
- `ledger.json`: The aggregated cost registry.
- `sessions/`: Detailed data for every individual AI session.
- `pricing/`: Snapshots of API rates used for stable history.

**Important**: The `.gitignore` provided by default ensures that your private cost data is never committed to public repositories.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
<p align="center">
  Built with ❤️ for the <b>Indie Hackers</b> and <b>AI Engineers</b> community.<br>
  <i>"Control your AI costs, build better software."</i>
</p>
