import datetime


class ServerDTO():
    def __init__(self, server):
        self.name = server.name
        self.vendor = server.vendor
        self.comments = server.comments
        self.specification_url = server.specification_url
        self.availability = server.availability

    components = str
    fuel_versions = str
    vendor = str
    comments = str
    name = str
    specification_url = str
    availability = str


class ComponentDTO():
    def __init__(self, component):
        self.name = component.name
        self.vendor = component.vendor
        self.type = component.type
        self.hw_id = component.hw_id
        self.driver = component.driver.name

    name = str
    vendor = str
    comments = str
    type = str
    hw_id = str
    driver = str


class DriverDTO():
    def __init__(self, driver):
        self.name = driver.name
        self.version = driver.version

    version = str
    name = str


class FuelVersionDTO():
    name = str

    def __init__(self, fuel_version):
        self.name = fuel_version.name


class CertificationDTO():
    server = str
    date = datetime.date
    comments = str
    fuel_version = str

    def __init__(self, certification):
        self.date = certification.date
        self.server = certification.server.name
        self.comments = certification.comments
        self.fuel_version = certification.fuel_version.name