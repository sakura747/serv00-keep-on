from flask import Flask, request, jsonify, Response,send_from_directory
import threading
import subprocess
import os
import logging
import requests

# 设置日志记录
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
app = Flask(__name__)
runMaster = os.getenv('runMaster', 'Not Set')
def run_local_file():
    runMaster = os.getenv('runMaster', 'Not Set')
    current_directory = os.getcwd()
    app.logger.info(f'Current directory: {current_directory}')
    print(f'Current directory: {current_directory}')
    
    app.logger.info('Running local file')
    result = subprocess.run([runMaster], capture_output=True, text=True)
    app.logger.info(f'Return code: {result.returncode}')
    app.logger.info(f'Stdout: {result.stdout}')
    app.logger.info(f'Stderr: {result.stderr}')
    print(f'Return code: {result.returncode}')
    print(f'Stdout: {result.stdout}')
    print(f'Stderr: {result.stderr}')
@app.route('/')
def index():
    return send_from_directory('src/html', 'index.html')

@app.route('/start-local-file')
def start_local_file():
    app.logger.info('Start local file route was accessed')
    thread = threading.Thread(target=run_local_file)
    thread.start()
    return jsonify({"message": "Local file started in a separate thread!"})

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('src', filename)

if __name__ == '__main__':
    app.run(debug=True)

