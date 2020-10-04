from flask import Flask
from multiprocessing import Pool
from flask.globals import request
from healthcheck import HealthCheck
from utils.decorators import AppDecorator
import gunicorn_conf
import json
from utils import constants
from utils import endpoints
import time
import concurrent.futures
from utils import merge_sort
from utils import scrap

app = Flask(__name__)
content_type = "application/json"

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/error')
def error():
    return '403-Bad Request'

@app.route(endpoints.ping, methods = ['GET'])
@AppDecorator.content_type_check
def get_ping():
    response = {}
    health = HealthCheck()
    response['message'] = constants.hc_success
    (system_data, status, c_t) = health.run()
    response['code'] = status
    if status != 200:
        response['code'] = constants.failure_code
        response['message'] = constants.hc_failure
    return response

@app.route(endpoints.exec_params, methods = ['POST'])
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

@app.route(endpoints.sort, methods = ['POST'])
@AppDecorator.content_type_check
@AppDecorator.limit_content_length(gunicorn_conf.max_payload_in_mb)
def sort_list():
    request_data = json.loads(request.data)
    response = {}
    if 'input_list' in request_data.keys():
        start_time = time.time()
        input_list = request_data['input_list']
        if request_data['concurrent']:
            response['code'] = constants.success_code
            with concurrent.futures.ThreadPoolExecutor(gunicorn_conf.workers) as executor:
                future = executor.submit(merge_sort.sort, numbers = input_list, executor = executor)
                sorted_list = future.result()
        else:
            sorted_list = sorted(input_list)
        end_time = time.time()
        time_consumed = int(round((end_time - start_time)))
        response['code'] = constants.success_code
        response['message'] = constants.sort_success
        response['time-taken'] = str(time_consumed) + "s"
        response['sorted-list'] = sorted_list
        return response
    else:
        return error()

@app.route(endpoints.web_crawl, methods = ['POST'])
@AppDecorator.content_type_check
@AppDecorator.limit_content_length(gunicorn_conf.max_payload_in_mb)
def web_crawl():
    request_data = json.loads(request.data)
    response = {}
    if 'input_list' in request_data.keys():
        start_time = time.time()
        input_list = request_data['input_list']
        if request_data['parallel']:
            response['code'] = constants.success_code
            p = Pool(gunicorn_conf.max_process_pool)
            sorted_list = p.map(scrap.scrape, input_list)
            p.terminate()
            p.join()
        else:
            sorted_list = scrap.webcrawl(input_list)
            print('sorted_list ',sorted_list)
        end_time = time.time()
        time_consumed = int(round((end_time - start_time)))
        response['code'] = constants.success_code
        response['message'] = constants.sort_success
        response['time-taken'] = str(time_consumed)+"s"
        response['sorted-list'] = sorted_list
        return response
    else:
        return error()
# def init_db():
#     import db
#     database = db.get_db()
#     with open_resource('schema.sql', mode='r') as f:
#         database.cursor().executescript(f.read())
#     database.commit()

if __name__ == '__main__':
    # init_db()
    app.run()