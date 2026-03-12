from fastapi import FastAPI, Request
import subprocess
import os
import requests
from dotenv import load_dotenv

# ===========================
# LOAD ENVIRONMENT VARIABLES
# ===========================
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USERS = [int(os.getenv("AUTHORIZED_USER"))]
AUTHORIZED_DOMAINS = [os.getenv("DOMAIN_NAME")]

SSH_USER = os.getenv("SSH_USER")
SSH_HOST = os.getenv("SSH_HOST")
DEPLOY_SCRIPT_PATH = os.getenv("DEPLOY_SCRIPT_PATH")

# ===========================
# FASTAPI APP
# ===========================
app = FastAPI()

# ===========================
# COMMANDS
# ===========================
COMMANDS = {
    "restart globalsoft": f"ssh -o StrictHostKeyChecking=no {SSH_USER}@{SSH_HOST} 'docker restart globalsoft_web'",
    "docker ps": f"ssh -o StrictHostKeyChecking=no {SSH_USER}@{SSH_HOST} 'docker ps'",
    "logs globalsoft": f"ssh -o StrictHostKeyChecking=no {SSH_USER}@{SSH_HOST} 'docker logs globalsoft_web --tail 20'",
    "server status": f"ssh -o StrictHostKeyChecking=no {SSH_USER}@{SSH_HOST} 'uptime'"
}

# ===========================
# TELEGRAM UTILITY
# ===========================
def send_telegram_message(chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# ===========================
# ROOT ENDPOINT (TEST)
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

    # Unauthorized user
    if user_id not in AUTHORIZED_USERS:
        return {"status": "unauthorized"}

    # Deploy GlobalSoft separately to stream logs
    if text == "deploy globalsoft":
        send_telegram_message(user_id, "🚀 Starting deployment of GlobalSoft...")

        # Build SSH command with Option 1
        ssh_cmd = f"ssh -o StrictHostKeyChecking=no {SSH_USER}@{SSH_HOST} '{DEPLOY_SCRIPT_PATH}'"
        
        process = subprocess.Popen(
            ssh_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )

        # Stream logs live
        for line in process.stdout:
            if line.strip():
                send_telegram_message(user_id, f"📄 {line.strip()}")
        process.wait()

        send_telegram_message(user_id, "✅ Deployment finished.")
        return {"status": "success", "message": "Deployment finished."}

    # Normal commands
    command_to_run = COMMANDS.get(text)
    if not command_to_run:
        send_telegram_message(user_id, f"❌ Command '{text}' not recognized")
        return {"status": "unknown command"}

    try:
        output = subprocess.check_output(command_to_run, shell=True, stderr=subprocess.STDOUT, text=True)
        send_telegram_message(user_id, f"✅ Command executed successfully:\n{output}")
        return {"status": "success", "output": output}
    except subprocess.CalledProcessError as e:
        error_output = e.output if e.output else str(e)
        send_telegram_message(user_id, f"❌ Error executing command:\n{error_output}")
        return {"status": "error", "output": error_output}