from flask import Flask, Response, jsonify
from flask.globals import request
from healthcheck import HealthCheck
from decorators import AppDecorator
import gunicorn_conf
import json
import constants

app = Flask(__name__)
health = HealthCheck()
content_type = "application/json"

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/error')
def error():
    return '403-Bad Request'

@app.route('/ping', methods = ['GET'])
@AppDecorator.content_type_check
def get_ping():
    response = {}
    response['message'] = constants.hc_success
    (system_data, status, c_t) = health.run()
    response['code'] = status
    if status != 200:
        response['code'] = constants.failure_code
        response['message'] = constants.hc_failure
    return response

@app.route('/execution-parameters', methods = ['POST'])
@AppDecorator.content_type_check
def execution_params():
    response = {}
    try:
        response['code'] = constants.success_code
        response['MaxConcurrentTransforms'] = gunicorn_conf.workers
        response['MaxPayloadInMB'] = gunicorn_conf.max_payload_in_mb
        response['message'] = constants.ep_success
    except:
        response['code'] = constants.failure_code
        response['message'] = constants.ep_failure
    return response
# @app.route('/execution-parameters')

@app.route('/sort', methods = ['POST'])
@AppDecorator.content_type_check
def sort_list():
    request_data = json.loads(request.data)
    if 'input_list' in request_data.keys():
        if request_data['concurrent']:
            return request.json
        else:
            return sorted(request_data['input_list'])

# def init_db():
#     import db
#     database = db.get_db()
#     with open_resource('schema.sql', mode='r') as f:
#         database.cursor().executescript(f.read())
#     database.commit()

if __name__ == '__main__':
    # init_db()
    app.run()