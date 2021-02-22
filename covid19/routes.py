from manage import app
import requests
@app.route('/index',methods=['GET'])
def index():
    return "hi its index"

