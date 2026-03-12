from fastapi import FastAPI, Request
import subprocess
import os

app = FastAPI()

# Only your Telegram ID can use the bot
AUTHORIZED_USERS = [2139237822]  # Replace with your Telegram user ID
AUTHORIZED_DOMAINS = ["chatop.nitypulse.com"]

# Simple command router
COMMANDS = {
    "deploy globalsoft": "bash scripts/deploy_globalsoft.sh",
    "restart globalsoft": "docker restart globalsoft_web",
    "docker ps": "docker ps",
    "logs globalsoft": "docker logs globalsoft_web --tail 20",
    "server status": "uptime"
}

@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()
    
    # Telegram message data
    message = data.get("message", {})
    user_id = message.get("from", {}).get("id")
    text = message.get("text", "").lower()

    if user_id not in AUTHORIZED_USERS:
        return {"status": "unauthorized"}

    command_to_run = COMMANDS.get(text)

    if not command_to_run:
        return {"status": "unknown command", "message": f"Command '{text}' not recognized"}

    try:
        output = subprocess.check_output(command_to_run, shell=True, stderr=subprocess.STDOUT)
        return {"status": "success", "output": output.decode()}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "output": e.output.decode()}