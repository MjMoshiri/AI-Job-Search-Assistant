from flask import Flask, request, jsonify
from service import add_job_application, create_tables
from typing import Dict

app = Flask(__name__)
with app.app_context():
    create_tables()

@app.route('/job', methods=['POST'])
def create_job() -> jsonify:
    if not request.json:
        return jsonify({"error": "No JSON payload provided"}), 400
    try:
        job_details: Dict = request.json
        add_job_application(job_details)
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True,port=5995, host='0.0.0.0')
