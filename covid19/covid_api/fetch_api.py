from covid19.covid_api import covid_api
import requests
from covid19.models.covid19_models import Country, Province, Report
from flask import Response, request
from covid19.covid_api.const import ONLINE_SERVER_ERROR, INVALID_PAYLOAD
import json
from covid19.covid_api.crud.covid19 import CountryService, ProvinceService, ReportService
from covid19 import db

@covid_api.route('/fetch/index', methods=['GET'])
def index():
    return "hi its fetch index"


@covid_api.route('/fetch/countries', methods=['GET'])
def countries():
    """
    This API fetch all the countries from online server
    :return: countries data in case of successful completion
             online server error if does not receive data from server
    """
    resp = requests.get('https://covid-api.com/api/regions')  # hitting online server to get data
    if resp.status_code != 200:
        # This means something went wrong.
        return Response(ONLINE_SERVER_ERROR, resp.status_code)
    return Response(json.dumps(resp.json()['data']), 200)


@covid_api.route('/countries', methods=['POST'])
def save_countries():
    """
    This API post/save the countries data in to the local database
    :requirement: Json data is required to enter in the database
    :return: same data after saving in local db
            if data not provided, it will return 'Json data required', 400 status code
            if data not provided in list, it will return 'Invalid payload' 400 status code
    """
    countries = json.loads(request.data)
    print("Countries = ", countries)
    if countries is None:
        return Response('Json data required', 400)
    if type(countries) is list:
        for country in countries:
            country_exists = db.session.query(Country).filter_by(iso=country['iso'], name=country['name']).first()
            if country_exists:
                continue
            country_object = CountryService()
            country_object.add_new_country(country)
        return Response(json.dumps(countries), 200)
    else:
        return Response(INVALID_PAYLOAD, 400)


@covid_api.route('/fetch/provinces', methods=['GET'])
def provinces():
    """
    This API will fetch data from the online server
    :requirements: iso parameter in required to fetch data
    :return: data fetched from online server
            if iso not provided, it will return 'iso is required in param', 400 status code
            if failed to fetch data from server, it will return 'Online server error' with respected status code
    """
    # ####################Fetch
    iso = request.args.get('iso')
    if iso is None:
        return Response("iso is required as param", 400)
    url = 'https://covid-api.com/api/provinces?iso=' + str(iso)  # url for one country provinces
    resp = requests.get(url)
    if resp.status_code != 200:
        # This means something went wrong while getting provinces from online sever.
        return Response(ONLINE_SERVER_ERROR, resp.status_code)
    return Response(json.dumps(resp.json()['data']), 200)

    # ########## Fetch and save all the country provinces in db in one run
    # countries = Country.query.all()             # get all the countries data from local db to get their provinces
    # for country in countries:
    #     url = 'https://covid-api.com/api/provinces?iso='+str(country.iso)   # url for one country provinces
    #     resp = requests.get(url)
    #     if resp.status_code != 200:
    #         # This means something went wrong while getting provinces from online sever.
    #         return Response(ONLINE_SERVER_ERROR,resp.status_code)
    #     for province in dict(resp.json())['data']:      # getting one by one each province from the response of server
    #
    #         print("Province ", province)
    #         province_object = ProvinceService()
    #         province_object.add_new_province(province,country.id)
    # return Response(json.dumps(resp.json()['data']), 200)


@covid_api.route('/provinces', methods=['POST'])
def save_provinces():
    """
        This API post/save the provinces data in to the local database
        :requirement: Json data is required to enter in the database
        :return: same data after saving in local db
                if data not provided, it will return 'Json data required', 400 status code
                if data not provided in list, it will return 'Invaid payload' 400 status code

                As country have one-to-many relationship with province
                so it wil return 'Foreign key constraint Error',200 status code, if country not exist in the database
        """
    provinces = json.loads(request.data)
    if provinces is None:
        return Response("Json data required", 400)
    if type(provinces) is list:
        for province in provinces:
            province_exists = db.session.query(Province).filter_by(province=province['province'], lat=province['lat'],
                                                                   long=province['long']).first()
            if province_exists:
                continue
            country = Country.query.filter_by(iso=province['iso'], name=province['name']).first()
            if country is None:
                return Response(json.dumps({"Message":"Country of this province not exist in database, Foreign key constraint"}),200)
            province_object = Province(province=province['province'], lat=province['lat'], long=province['long'],
                                       country_id=country.id)
            db.session.add(province_object)  # Enter data one by one on db
            db.session.commit()
        return Response(json.dumps(provinces), 200)
    else:
        return Response(INVALID_PAYLOAD, 400)


@covid_api.route('/fetch/reports', methods=['GET'])
def reports():
    """
        This API will fetch data from the online server
        :param: it handles multiple params and their combination
                1) region
                2) province
                3) date
                you can use any combination of these parameter, without these parameter it takes too much time to
                fetch data form the online server

        :return: data fetched from online server
                if failed to fetch data from server, it will return 'Online server error' with respected status code

        NOTE: As to fetch whole data from the database and save it in database is too much time consuming so when user
              fetch the data we will check if province for that report exist in our database for future use we will
              store data in our local database(Foreign key constraint), if province not exist in our database
              we will not store data (foreign key constraint) and return data

        """
    # #########################################################Fetch data
    region = request.args.get('region')
    province = request.args.get('province')
    date = request.args.get('date')
    if region is not None and province is not None and date is not None:
        url = 'https://covid-api.com/api/reports?region_name=' + str(region) + '&region_province=' \
              + str(province) + '&date=', str(date)
    elif region is not None and province is not None and date is None:
        url = 'https://covid-api.com/api/reports?region_name=' + str(region) + '&region_province=' + str(province)
    elif region is not None and province is None and date is not None:
        url = 'https://covid-api.com/api/reports?region_name=' + str(region) + '&date=' + str(date)
    elif region is None and province is not None and date is not None:
        url = 'https://covid-api.com/api/reports?region_province=' + str(province) + '&date=' + str(date)
    elif region is not None and province is None and date is None:
        url = 'https://covid-api.com/api/reports?region_name=' + str(region)
    elif region is None and province is not None and date is None:
        url = 'https://covid-api.com/api/reports?region_province=' + str(province)
    elif region is None and province is None and date is not None:
        url = 'https://covid-api.com/api/reports?date=' + str(date)
    else:
        url = 'https://covid-api.com/api/reports'
    resp = requests.get(url)
    if resp.status_code != 200:
        # This means something went wrong.
        return Response(ONLINE_SERVER_ERROR, resp.status_code)

    # #######################################Fetch and save data to populate database simultaneoustly
    for record in dict(resp.json())['data']:      # getting one by one each province from the response of server
        report_object = ReportService()
        province_object = ProvinceService()
        province_id = province_object.get_id(province=record['region']['province'],lat=record['region']['lat'],
                                             long=record['region']['long'])
        if province_id is False:        # if province not exist in db. Only fetch data and return to user
            continue
        report_object.add_new_report(record, province_id)
    #############################################################################################################
    return Response(json.dumps(resp.json()['data']), 200)


@covid_api.route('/reports', methods=['POST'])
def save_reports():
    reports = json.loads(request.data)
    if reports is None:
        return Response("Json data required", 400)
    if type(reports) is list:
        for report in reports:
            report_exists = db.session.query(Report).filter_by(date=report['date'], confirmed=report['confirmed'],
                                                               deaths=report['deaths'], recovered=report['recovered'],
                                                               confirmed_diff=report['confirmed_diff'],
                                                               deaths_diff=report['deaths_diff'],
                                                               recovered_diff=report['recovered_diff'],
                                                               last_update=report['last_update'],
                                                               active=report['active'],
                                                               active_diff=report['active_diff'],
                                                               fatality_rate=report['fatality_rate']).first()
            if report_exists:
                continue
            province = Province.query.filter_by(province=report['region']['province'], lat=report['region']['lat'],
                                                long=report['region']['long']).first()
            if province is None:
                return Response(json.dumps({"Message": "Province not found for these reports, Foriegn key constraint"}),200)
            report_object = Report(date=report['date'], confirmed=report['confirmed'], deaths=report['deaths'],
                                   recovered=report['recovered'], confirmed_diff=report['confirmed_diff'],
                                   deaths_diff=report['deaths_diff'], recovered_diff=report['recovered_diff'],
                                   last_update=report['last_update'], active=report['active'],
                                   active_diff=report['active_diff'], fatality_rate=report['fatality_rate'],
                                   province_id=province.id)
            db.session.add(report_object)  # Enter data one by one on db
            db.session.commit()
        return Response(json.dumps(reports), 200)
    else:
        return Response(INVALID_PAYLOAD, 400)

