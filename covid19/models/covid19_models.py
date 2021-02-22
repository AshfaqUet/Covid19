from covid19 import db
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import datetime
import uuid


class Country(db.Model):
    id = Column(String(32), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    iso = Column(String(32), nullable=False)

    __tablename__ = "country"

    # relationships
    province = relationship("Province", backref="country", lazy="dynamic")

    def __init__(self, iso=None, name=None):
        self.id = str(uuid.uuid4().hex)
        self.iso = iso
        self.name = name

    def to_json(self):
        return {
            'iso': self.iso,
            'name': self.name
        }


class Province(db.Model):
    id = Column(String(32), primary_key=True)
    province = Column(String(255))
    lat = Column(String(32))
    long = Column(String(32))

    __tablename__ = 'province'

    # relationships
    country_id = Column(String(32), ForeignKey('country.id'), nullable=False)

    # relationship with report
    report = relationship("Report", backref="province", lazy="dynamic")

    def __init__(self, province=None, lat=None, long=None, country_id=None):
        self.id = str(uuid.uuid4().hex)
        self.province = province
        self.lat = lat
        self.long = long

        self.country_id = country_id

    def to_json(self):
        return {
            'id': self.id,
            'province': self.province,
            'lat': self.lat,
            'long': self.long,
            'country': self.country_id
        }


class Report(db.Model):
    id = Column(String(32), primary_key=True)
    date = Column(Date(), default=datetime.date, nullable=False)
    confirmed = Column(Integer, default=0, nullable=False)
    deaths = Column(Integer, default=0, nullable=False)
    recovered = Column(Integer, default=0, nullable=False)
    confirmed_diff = Column(Integer, default=0, nullable=False)
    deaths_diff = Column(Integer, default=0, nullable=False)
    recovered_diff = Column(Integer, default=0, nullable=False)
    last_update = Column(Date(), default=datetime.date, nullable=False)
    active = Column(Integer, default=0, nullable=False)
    active_diff = Column(Integer, default=0, nullable=False)
    fatality_rate = Column(Integer, default=0, nullable=False)

    __tablename__ = 'report'
    # relationship
    province_id = Column(String(32), ForeignKey('province.id'), nullable=False)

    def __init__(self, date=None, confirmed=None, deaths=None, recovered=None, confirmed_diff=None, deaths_diff=None,
                 recovered_diff=None, last_update=None, active=None, active_diff=None, fatality_rate=None,
                 province_id=None):
        self.id = str(uuid.uuid4().hex)
        self.date = date
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered
        self.confirmed_diff = confirmed_diff
        self.deaths_diff = deaths_diff
        self.recovered_diff = recovered_diff
        self.last_update = last_update
        self.active = active
        self.active_diff = active_diff
        self.fatality_rate = fatality_rate

        self.province_id = province_id

    def to_json(self):
        return {
            'id': self.id,
            'date': self.date,
            'confirmed': self.confirmed,
            'deaths': self.deaths,
            'recovered': self.recovered,
            'confirmed_diff': self.confirmed_diff,
            'deaths_diff': self.deaths_diff,
            'recovered_diff': self.recovered_diff,
            'last_update': self.last_update,
            'active': self.active,
            'active_diff': self.active_diff,
            'fatality_rate': self.fatality_rate,

            'province': self.province_id
        }
