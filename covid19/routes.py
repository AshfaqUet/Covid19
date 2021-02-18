from manage import app
import requests
@app.route('/index',methods=['GET'])
def index():
    return "hi its index"

@app.route('/countries',methods=['GET'])
def countries():
    resp = requests.get('https://covid-api.com/api/regions')
    # if resp.status_code != 200:
    #     # This means something went wrong.
    #     raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    # for todo_item in resp.json():
    #     print('{} {}'.format(todo_item['id'], todo_item['summary']))
    return resp.json()
