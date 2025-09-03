from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)

# Path to your wiki.json
data_file = "/media/xyt564/sd_card/python/new/wiki-web/wiki.json"
os.makedirs(os.path.dirname(data_file), exist_ok=True)
if not os.path.exists(data_file):
    with open(data_file, "w") as f:
        json.dump({}, f, indent=2)

# ----------- DATA HANDLERS -----------
def load_data():
    with open(data_file, "r") as f:
        return json.load(f)

def save_data(data):
    with open(data_file, "w") as f:
        json.dump(data, f, indent=2)

# ----------- ROUTES -----------
@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "")
    data = load_data()
    if query:
        notes = {k:v for k,v in data.items() if query.lower() in k.lower() or any(query.lower() in t.lower() for t in v.get("tags", []))}
    else:
        notes = data
    notes_sorted = dict(sorted(notes.items(), key=lambda item: item[0].lower()))
    return render_template("index.html", notes=notes_sorted, note=None, current_title=None, query=query)

@app.route("/note/<title>", methods=["GET", "POST"])
def note(title):
    data = load_data()
    all_notes = sorted(data.keys(), key=lambda s: s.lower())

    if request.method == "POST":
        content = request.form.get("content", "")
        tags = [t.strip() for t in request.form.get("tags", "").split(",") if t.strip()]
        data[title] = {"content": content, "tags": tags}
        save_data(data)

    note_data = data.get(title, {"content": "", "tags": []})

    query = request.args.get("q", "")
    if query:
        notes_filtered = {k:v for k,v in data.items() if query.lower() in k.lower() or any(query.lower() in t.lower() for t in v.get("tags", []))}
    else:
        notes_filtered = data
    notes_sorted = dict(sorted(notes_filtered.items(), key=lambda item: item[0].lower()))

    return render_template("index.html", notes=notes_sorted, note=note_data, current_title=title, query=query)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if title:
        data = load_data()
        if title not in data:
            data[title] = {"content": "", "tags": []}
            save_data(data)
    return redirect(url_for("index"))

@app.route("/delete/<title>")
def delete(title):
    data = load_data()
    if title in data:
        data.pop(title)
        save_data(data)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
