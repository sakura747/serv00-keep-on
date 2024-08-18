from flask import Flask, request, jsonify, Response
import threading
import subprocess
import os
import logging
import requests

# 设置日志记录
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
app = Flask(__name__)


def is_process_running(process_name):
    """检查指定名称的进程是否在运行"""
    try:
        # 执行 `ps aux` 命令获取所有进程
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        # 检查进程是否在输出中
        return process_name in result.stdout
    except Exception as e:
        app.logger.error(f"Error checking process: {e}")
        return False

def run_local_file():
    """运行本地可执行文件"""
    current_directory = os.getcwd()
    app.logger.info(f'Current directory: {current_directory}')
    print(f'Current directory: {current_directory}')
    
    app.logger.info('Running local file')
    result = subprocess.run(['./tmp/sing-box', 'run', '-c', 'tmp/config.json'], capture_output=True, text=True)
    app.logger.info(f'Return code: {result.returncode}')
    app.logger.info(f'Stdout: {result.stdout}')
    app.logger.info(f'Stderr: {result.stderr}')
    print(f'Return code: {result.returncode}')
    print(f'Stdout: {result.stdout}')
    print(f'Stderr: {result.stderr}')


@app.route('/start-local-file')
def start_local_file():
    app.logger.info('Start local file route was accessed')

    # 检查是否有进程在运行
    process_name = './tmp/sing-box run -c tmp/config.json'
    if not is_process_running(process_name):
        # 如果进程没有在运行，则启动线程
        app.logger.info('Process not running, starting new thread')
        thread = threading.Thread(target=run_local_file)
        thread.start()
        return jsonify({"message": "Local file started in a separate thread!"})
    else:
        app.logger.info('Process is already running, skipping')
        return jsonify({"message": "Local file is already running!"})

TARGET_URL = "http://127.0.0.1:60661"

@app.route("/super", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route("/super/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy(path):
    # 记录请求信息
    app.logger.info(f'Received request: {request.method} {request.url}')
    
    # 构建目标URL
    url = f"{TARGET_URL}/super/{path}"
    app.logger.info(f'Target URL: {url}')
    
    # 获取请求方法
    method = request.method
    
    # 获取请求头和数据
    headers = {key: value for key, value in request.headers if key != 'Host'}
    data = request.get_data()
    app.logger.info(f'Request headers: {headers}')
    app.logger.info(f'Request data: {data}')
    
    # 发送请求到目标服务器
    try:
        response = requests.request(method, url, headers=headers, data=data, params=request.args)
        app.logger.info(f'Response status code: {response.status_code}')
    except requests.RequestException as e:
        app.logger.error(f'Request to target URL failed: {e}')
        return jsonify({"error": "Request to target URL failed"}), 500
    
    # 构建响应对象
    proxy_response = Response(response.content, response.status_code)
    
    # 转发目标服务器的响应头
    for key, value in response.headers.items():
        proxy_response.headers[key] = value
        app.logger.info(f'Response header: {key}: {value}')
    
    app.logger.info('Request successfully proxied')
    return proxy_response

if __name__ == '__main__':
    app.run(debug=True)
