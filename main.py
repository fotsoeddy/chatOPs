from fastapi import FastAPI, Request
import subprocess
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = FastAPI()

# ===========================
# CONFIGURATION
# ===========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USERS = [int(os.getenv("AUTHORIZED_USER"))]
AUTHORIZED_DOMAINS = [os.getenv("DOMAIN_NAME")]

# ===========================
# COMMANDS
# ===========================
COMMANDS = {
    "deploy globalsoft": "bash scripts/deploy_globalsoft.sh",
    "restart globalsoft": "docker restart globalsoft_web",
    "docker ps": "docker ps",
    "logs globalsoft": "docker logs globalsoft_web --tail 20",
    "server status": "uptime"
}

# ===========================
# ROOT ENDPOINT (for testing)
# ===========================
@app.get("/")
async def root():
    return {"message": "ChatOps Bot is running ✅"}

# ===========================
# TELEGRAM WEBHOOK
# ===========================
@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    
    message = data.get("message", {})
    user_id = message.get("from", {}).get("id")
    text = message.get("text", "").lower().strip()

    if user_id not in AUTHORIZED_USERS:
        return {"status": "unauthorized"}

    command_to_run = COMMANDS.get(text)
    if not command_to_run:
        return {"status": "unknown command", "message": f"Command '{text}' not recognized"}

    try:
        output = subprocess.check_output(command_to_run, shell=True, stderr=subprocess.STDOUT)
        return {"status": "success", "output": output.decode()}
    except subprocess.CalledProcessError as e:
        error_output = e.output.decode() if e.output else str(e)
        return {"status": "error", "output": error_output}