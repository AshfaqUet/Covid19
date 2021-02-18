from covid19.covid_api import covid_api
import requests
from covid19.models.covid19_models import Country, Province, Report
from flask import Response, request
from covid19.covid_api.const import *
import json
from covid19.covid_api.crud.covid19 import *

@covid_api.route('/get/countries', methods=['GET'])
def get_countries():
    country_service = CountryService()
    result = country_service.get_all_country()
    print("Here type is ",type(result))

    if type(result) is str:
        return result
    else:
        return {"message":"Allah knows better than me, Allah help me"}
    # resp = requests.get('https://covid-api.com/api/regions')  # hitting online server to get data
    # if resp.status_code != 200:
    #     # This means something went wrong.
    #     return Response(ONLINE_SERVER_ERROR, resp.status_code)
    # return Response(json.dumps(resp.json()['data']), 200)