from fastapi import FastAPI, Request
import subprocess

app = FastAPI()

# ===========================
# CONFIGURATION
# ===========================
BOT_TOKEN = "8510147575:AAFggKrM4zNP9sEIXfS5imQssIRJG1H-E0w"
AUTHORIZED_USERS = [2139237822]  # Your Telegram user ID
AUTHORIZED_DOMAINS = ["chatop.nitypulse.com"]  # Optional check

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
    
    # Extract Telegram message
    message = data.get("message", {})
    user_id = message.get("from", {}).get("id")
    text = message.get("text", "").lower().strip()

    # Check if user is authorized
    if user_id not in AUTHORIZED_USERS:
        return {"status": "unauthorized"}

    # Find the command
    command_to_run = COMMANDS.get(text)
    if not command_to_run:
        return {"status": "unknown command", "message": f"Command '{text}' not recognized"}

    try:
        # Execute the command
        output = subprocess.check_output(command_to_run, shell=True, stderr=subprocess.STDOUT)
        result = output.decode()
        return {"status": "success", "output": result}
    except subprocess.CalledProcessError as e:
        error_output = e.output.decode() if e.output else str(e)
        return {"status": "error", "output": error_output}