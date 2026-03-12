# 🤖 ChatOps Bot

A lightweight **ChatOps bot** that lets you manage your server infrastructure directly from **Telegram**. Built with [FastAPI](https://fastapi.tiangolo.com/) and deployable via Docker.

---

## ✨ Features

- **Telegram-powered** — Send commands from Telegram, get instant results
- **Secure** — Only authorized users can execute commands
- **Live deployment logs** — Streams deployment output line-by-line to Telegram
- **Dockerized** — One-command setup with Docker Compose
- **Extensible** — Easily add new commands and deploy scripts

## 📋 Available Commands

| Command               | Description                              |
| --------------------- | ---------------------------------------- |
| `deploy globalsoft`   | Pull latest code & redeploy via Docker   |
| `restart globalsoft`  | Restart the `globalsoft_web` container    |
| `docker ps`           | List running Docker containers           |
| `logs globalsoft`     | Show last 20 lines of container logs     |
| `server status`       | Display server uptime                    |

---

## 🛠️ Tech Stack

- **Python 3.11**
- **FastAPI** + **Uvicorn**
- **python-telegram-bot** / Telegram Bot API
- **Docker** + **Docker Compose**

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- A [Telegram Bot Token](https://core.telegram.org/bots#botfather) from BotFather
- Your Telegram user ID (get it from [@userinfobot](https://t.me/userinfobot))

### 1. Clone the repository

```bash
git clone https://github.com/your-username/chatops.git
cd chatops
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
# Telegram bot token from BotFather
BOT_TOKEN=your-bot-token-here

# Your Telegram user ID (only this user can run commands)
AUTHORIZED_USER=your-telegram-user-id

# Domain where the bot is hosted
DOMAIN_NAME=your-domain.com
```

### 3. Build & run with Docker Compose

```bash
docker compose up -d --build
```

The bot will be available on **port 8100**.

### 4. Set the Telegram webhook

Point Telegram to your bot's webhook endpoint:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://<YOUR_DOMAIN>/webhook"
```

Verify the webhook is set:

```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

---

## 📁 Project Structure

```
chatops/
├── main.py              # FastAPI app — webhook handler & command execution
├── scripts/
│   └── deploy_globalsoft.sh   # Deployment script for GlobalSoft
├── Dockerfile           # Container image definition
├── docker-compose.yml   # Docker Compose orchestration
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not committed)
└── .gitignore
```

---

## ➕ Adding New Commands

Edit the `COMMANDS` dictionary in `main.py`:

```python
COMMANDS = {
    "deploy globalsoft": "bash scripts/deploy_globalsoft.sh",
    "restart globalsoft": "docker restart globalsoft_web",
    "docker ps": "docker ps",
    "logs globalsoft": "docker logs globalsoft_web --tail 20",
    "server status": "uptime",
    # Add your own commands here 👇
    "disk usage": "df -h",
    "memory": "free -m",
}
```

---

## 🔒 Security Notes

- Only the `AUTHORIZED_USER` Telegram ID can execute commands
- The `.env` file containing secrets is **git-ignored**
- The Docker socket is mounted for container management — use with caution in production

---

## 📄 License

This project is open source. Feel free to use and modify it as you see fit.
