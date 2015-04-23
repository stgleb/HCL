from datetime import datetime
from pony.orm import *

db = Database("sqlite", "database.sqlite", create_db=True)


class Server(db.Entity):
    _table_ = "Server"
    id = PrimaryKey(int, auto=True)
    components = Set("Component")
    certifications = Set("Certification")
    vendor = Required(str)
    comments = Optional(str)
    name = Required(str, unique=True)
    specification_url = Optional(str)
    availability = Optional(str)

    def __str__(self):
        return "id: {0} name: {1} vendor: {2}".\
            format(self.id, self.name, self.vendor)


class Component(db.Entity):
    id = PrimaryKey(int, auto=True)
    servers = Set(Server)
    name = Required(str)
    vendor = Optional(str)
    comments = Optional(str)
    type = Required(str)
    hw_id = Optional(unicode, unique=True)
    driver = Required("Driver")


class Certification(db.Entity):
    id = PrimaryKey(int, auto=True)
    server = Required(Server)
    date = Optional(datetime)
    comments = Optional(str)
    fuel_version = Required("FuelVersion")


class FuelVersion(db.Entity):
    id = PrimaryKey(int, auto=True)
    certifications = Set(Certification)
    name = Required(str, unique=True)
    drivers = Set("Driver")


class Driver(db.Entity):
    fuel_versions = Set(FuelVersion)
    version = Required(str)
    name = Required(str, unique=True)
    components = Set(Component)
    composite_key(name, version)


class Type(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(unicode)


class HardwareId(db.Entity):
    id = PrimaryKey(int, auto=True)
    hw_id = Required(str)
    component_name = Required(unicode)


class Wishlist(db.Entity):
    id = PrimaryKey(int, auto=True)
    server_name = Required(unicode)


sql_debug(True)
db.generate_mapping(create_tables=True)
