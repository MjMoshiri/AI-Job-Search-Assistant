from flask import Flask, request, jsonify
from service import create_tables, check_if_id_exists, add,update, get_recent,get_unprocessed
from typing import Dict
import time


app = Flask(__name__)

with app.app_context():
    attempts = 0
    while attempts < 10:
        try:
            create_tables()
            break
        except Exception as e:
            print(f"An error occurred: {e}. Retrying in 5 seconds...")
            time.sleep(5)
            attempts += 1
    if attempts == 10:
        print("Max attempts reached. Stopping execution.")


@app.route('/job/<string:job_id>', methods=['PUT'])
def update_job(job_id) -> jsonify:
    if not request.json:
        return jsonify({"error": "No JSON payload provided"}), 400
    try:
        job_details: Dict = request.json
        if not check_if_id_exists(job_id):
            return jsonify({"error": "Job with this ID does not exist"}), 404
        if update(job_id, job_details):
            return jsonify({"message": "Job application updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update job application"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    

@app.route('/job', methods=['POST'])
def create_job() -> jsonify:
    if not request.json:
        return jsonify({"error": "No JSON payload provided"}), 400
    try:
        job_details: Dict = request.json
        if (check_if_id_exists(job_details.get("id"))):
            return jsonify({"error": "Job with this ID already exists"}), 409
        if add(job_details):
            return jsonify({"message": "Job application created successfully"}), 201
        else:
            return jsonify({"error": "Failed to create job application"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/jobs/', defaults={'num': 10}, methods=['GET'])
@app.route('/jobs/<int:num>', methods=['GET'])
def get_all_jobs(num: int) -> jsonify:
    try:
        jobs = get_recent(num)
        return jsonify([job.to_json() for job in jobs]), 200
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500
    
@app.route('/unprocessed/', defaults={'num': 10}, methods=['GET'])
@app.route('/unprocessed/<int:num>', methods=['GET'])
def get_unprocessed_jobs(num: int) -> jsonify:
    try:
        jobs = get_unprocessed(num)
        return jsonify([job.to_json() for job in jobs]), 200
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500

if __name__ == '__main__':
    app.run(debug=True,port=5995, host='0.0.0.0')
