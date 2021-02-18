from covid19.models.covid19_models import *
import json


class CountryService:                        # CRUD Operations of Country
    def __init__(self):
        self.country = Country()

    def get_all_country(self):
        countries = db.session.query(Country).all()
        list_of_countries = list()
        for country in countries:
            list_of_countries.append(country.to_json())
        return json.dumps(list_of_countries)

    def get_country(self, country_id):
        self.country = db.session.query(Country).filter_by(id=country_id).first()
        if not self.country:
            return {'error': 'data not found'}
        else:
            return self.country.to_json()

    def add_new_country(self, country_info):
        self.country = Country(
            iso=country_info['iso'], name=country_info['name']
        )
        db.session.add(self.country)  # Enter data one by one on db
        db.session.commit()
        return self.country.to_json()

    def update_country(self, country_info, country_id):
        self.country = db.session.query(Country).filter_by(id=country_id).first()
        if not self.country:
            return {'error': 'device not found'}
        else:
            if country_info['iso'] is not None:
                self.country.iso = country_info['iso']
            if country_info['name'] is not None:
                self.country.name = country_info['name']
            db.session.commit()
            return self.country.to_json()

    def delete_country(self, country_id):
        self.country = db.session.query(Country).get(country_id)
        if not self.country:
            return {'error': 'data not found'}
        else:
            db.session.delete(self.country)
        return self.country.to_json()


class ProvinceService:                        # CRUD Operations of Country
    def __init__(self):
        self.province = Province()

    def get_id(self,province,lat,long):
        self.province=db.session.query(Province).filter_by(province=province,lat=lat,long=long).first()
        if not self.province:
            return False
        return self.province.id

    def get_province(self, province_id):
        self.province = db.session.query(Province).filter_by(id=province_id).first()
        if not self.province:
            return False
        else:
            return self.province.to_json()

    def add_new_province(self, province_info, country_id):
        self.province = Province(
            province=province_info['province'], lat=province_info['lat'], long=province_info['long'],country_id=country_id
        )
        db.session.add(self.province)  # Enter data one by one on db
        db.session.commit()
        return self.province.to_json()

    def update_province(self, province_info, province_id):
        self.province = db.session.query(Province).filter_by(id=province_id).first()
        if not self.province:
            return {'error': 'device not found'}
        else:
            if province_info['province'] is not None:
                self.province.province = province_info['province']
            if province_info['lat'] is not None:
                self.province.lat = province_info['lat']
            if province_info['long'] is not None:
                self.province.long = province_info['long']
            db.session.commit()
            return self.province.to_json()

    def delete_device(self, province_id):
        self.province = db.session.query(Province).get(province_id)
        if not self.province:
            return {'error': 'data not found'}
        else:
            db.session.delete(self.province)
        return self.province.to_json()


class ReportService:                        # CRUD Operations of Country
    def __init__(self):
        self.report = Report()

    def get_report(self, report_id):
        self.report = db.session.query(Report).filter_by(id=report_id).first()
        if not self.report:
            return {'error': 'data not found'}
        else:
            return self.report.to_json()

    def add_new_report(self, report_info, province_id):
        self.report = Report(
            date=report_info['date'], confirmed=report_info['confirmed'], deaths=report_info['deaths'],
            recovered=report_info['recovered'], confirmed_diff=report_info['confirmed_diff'],
            deaths_diff=report_info['deaths_diff'], recovered_diff=report_info['recovered_diff'],
            last_update=report_info['last_update'], active=report_info['active'],
            active_diff=report_info['active_diff'], fatality_rate=report_info['fatality_rate'],
            province_id=province_id
        )
        db.session.add(self.report)  # Enter data one by one on db
        db.session.commit()
        return self.report.to_json()

    def update_report(self, report_info, report_id):
        self.province = db.session.query(Report).filter_by(id=report_id).first()
        if not self.province:
            return {'error': 'device not found'}
        else:
            if report_info['date'] is not None:
                self.report.date = report_info['date']
            if report_info['confirmed'] is not None:
                self.report.confirmed = report_info['confirmed']
            if report_info['deaths'] is not None:
                self.report.deaths = report_info['deaths']
            if report_info['recovered'] is not None:
                self.report.recovered = report_info['recovered']
            if report_info['confirmed_diff'] is not None:
                self.report.confirmed_diff = report_info['confirmed_diff']
            if report_info['deaths_diff'] is not None:
                self.report.deaths_diff = report_info['deaths_diff']
            if report_info['recovered_diff'] is not None:
                self.report.recovered_diff = report_info['recovered_diff']
            if report_info['last_update'] is not None:
                self.report.last_update = report_info['last_update']
            if report_info['active'] is not None:
                self.report.active = report_info['active']
            if report_info['active_diff'] is not None:
                self.report.active_diff = report_info['active_diff']
            if report_info['fatality_rate'] is not None:
                self.report.fatality_rate = report_info['fatality_rate']
            if report_info['province_id'] is not None:
                self.report.province_id = report_info['province_id']

            db.session.commit()
            return self.report.to_json()

    def delete_report(self, report_id):
        self.report = db.session.query(Report).get(report_id)
        if not self.report:
            return {'error': 'data not found'}
        else:
            db.session.delete(self.report)
        return self.report.to_json()