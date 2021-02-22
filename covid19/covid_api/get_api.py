from covid19.covid_api import covid_api
from covid19.covid_api.crud.covid19 import CountryService, ProvinceService, ReportService, get_all_province, \
    get_all_reports, get_all_country
import json

@covid_api.route('/countries', methods=['GET'])
def get_countries():
    """
    Get all the countries from local database and return
    :return: all the countries exist in the local database
    """
    result = get_all_country()
    return result


@covid_api.route('/provinces', methods=['GET'])
def get_provinces():
    """
    Get all the provinces form the local database and return
    :return: all the provinces exist in the local database along with their countries
    """
    result = get_all_province()
    provinces = json.loads(result)
    list_of_provinces = list()
    for province in provinces:
        country_service = CountryService()
        country=country_service.get_country(province['country'])
        province['country'] = country
        list_of_provinces.append(province)
    return json.dumps(list_of_provinces)


@covid_api.route('/reports', methods=['GET'])
def get_reports():
    """
    Get all the reports from local db and return along with its provinces
    :return: all the reports from local db and return along with its provinces
    """
    result = get_all_reports()
    reports = json.loads(result)
    list_of_reports = list()
    for report in reports:
        province_service = ProvinceService()
        province = province_service.get_province(report['province'])
        report['province'] = province
        list_of_reports.append(report)
    return json.dumps(list_of_reports)
