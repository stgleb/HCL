from datetime import datetime
from pony.orm import *

db = Database("sqlite", "database.sqlite", create_db=True)


class Server(db.Entity):
    _table_ = "Server"
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    components = Set("Component")
    certifications = Set("Certification")
    vendor = Required(str)
    comments = Optional(str)
    specification_url = Optional(str)
    availability = Optional(str)

    def __str__(self):
        return "id: {0} name: {1} vendor: {2}".\
            format(self.id, self.name, self.vendor)


class Component(db.Entity):
    id = PrimaryKey(int, auto=True)
    servers = Set(Server)
    name = Required(str)
    vendor = Required(str)
    comments = Optional(str)
    type = Required(str)


class Certification(db.Entity):
    id = PrimaryKey(int, auto=True)
    server = Optional(Server)
    fuel_version = Required(str)
    date = Required(datetime)
    comments = Optional(str)


class HardwareId(db.Entity):
    id = PrimaryKey(int, auto=True)
    hw_id = Required(str)
    component_name = Required(unicode)


class Wishlist(db.Entity):
    id = PrimaryKey(int, auto=True)
    server_name = Required(unicode)


sql_debug(True)
db.generate_mapping(create_tables=True)
