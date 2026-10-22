from flask import Flask, render_template, jsonify
import json
import os
 
app = Flask(__name__)
 
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "fields.json")
 
def load_fields():
    with open(DATA_PATH) as f:
        return json.load(f)
 
@app.route("/")
def index():
    fields = load_fields()
    # Alert when moisture < 30%
    alerts = [f for f in fields if f["soil_moisture"] < 30]
    total_water = sum(f["water_consumption"] for f in fields)
    lowest = min(fields, key=lambda x: x["soil_moisture"])
    # Prioritized irrigation list (lowest moisture first)
    priority = sorted(
        [f for f in fields if f["soil_moisture"] < 30],
        key=lambda x: x["soil_moisture"]
    )
    return render_template(
        "index.html",
        fields=fields,
        alerts=alerts,
        total_water=total_water,
        lowest=lowest,
        priority=priority
    )
 
@app.route("/api/fields")
def api_fields():
    return jsonify(load_fields())
 
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
