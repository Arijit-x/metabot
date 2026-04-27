# 🤖 MetaBot — AI-Powered Data Catalog Assistant

> WeMakeDevs x OpenMetadata Hackathon | Track T-01: MCP Ecosystem & AI Agents
> Powered by Groq llama 3.3 + MCP Server + OpenMetadata Sandbox

---

## ✅ No Docker. No Bot Token. Just 1 API Key.

MetaBot auto-logs in to the OpenMetadata Sandbox using built-in admin credentials.
**You only need a Gemini API key to run this project.**

```
sandbox.open-metadata.org  ←  free, hosted, no setup
admin@open-metadata.org / Admin@1234  ←  auto-used by MetaBot
```

---

## 🚀 Quick Start (3 steps only)

### Step 1 — Get Groq API Key
Go to https://console.groq.com/keys → Create API Key

### Step 2 — Set up .env
```bash
cd backend
cp .env.example .env

```

### Step 3 — Run
```bash
# Terminal 1 — Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend
npm install
npm start
```

Visit **http://localhost:3000** 🎉

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│            MCP Clients                      │
│   Claude.ai Desktop  |  Cursor IDE          │
└──────────────┬──────────────────────────────┘
               │  MCP Protocol (stdio)
               ▼
┌─────────────────────────────────────────────┐
│        MCP Server  (mcp_server.py)          │
│  search_tables | get_table_details          │
│  get_table_owner | get_lineage | recent     │
└──────────────┬──────────────────────────────┘
               │  Auto-login (no bot token!)
               ▼
┌─────────────────────────────────────────────┐
│   OpenMetadata Sandbox (No Docker!)         │
│   https://sandbox.open-metadata.org         │
│   Auto-login: admin@open-metadata.org       │
└─────────────────────────────────────────────┘

Web App:
React UI → FastAPI → Gemini 1.5 Pro → Sandbox
```

---

## 📁 Project Structure

```
metabot/
├── backend/
│   ├── openmetadata.py         ← Sandbox client (auto-login)
│   ├── agent.py                ← Gemini 1.5 Pro AI agent
│   ├── main.py                 ← FastAPI server
│   ├── mcp_server.py           ← MCP server (stdio)
│   ├── get_sandbox_token.py    ← Connection test script
│   ├── mcp_config.json         ← Claude.ai / Cursor config
│   ├── requirements.txt
│   └── .env.example            ← Only GEMINI_API_KEY needed!
├── frontend/
│   ├── src/App.jsx             ← Chat UI
│   └── src/App.css             ← Dark theme
└── README.md
```

---

## 🔑 Environment Variables

| Variable | Required | Notes |
|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | From https://aistudio.google.com |
| `OM_BASE_URL` | Pre-filled | `https://sandbox.open-metadata.org` |
| `OM_TOKEN` | ❌ Leave blank | MetaBot auto-logs in! |

---

## 🔌 MCP Server (Claude.ai Desktop)

Add to Claude desktop config:
- Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "metabot-openmetadata": {
      "command": "python",
      "args": ["/full/path/to/metabot/backend/mcp_server.py"],
      "env": {
        "OM_BASE_URL": "https://sandbox.open-metadata.org",
        "OM_TOKEN": "",
        "GEMINI_API_KEY": "your_key_here"
      }
    }
  }
}
```

---

## 💬 Demo Questions

- *"Which tables contain customer data?"*
- *"Who owns the orders table?"*
- *"What columns does dim_customer have?"*
- *"Show lineage for fact_order table"*
- *"Which tables have PII tags?"*

---

## 📄 License
MIT
