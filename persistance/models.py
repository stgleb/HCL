from datetime import date
from pony.orm import *

db = Database("sqlite", "database.sqlite", create_db=True)


class Server(db.Entity):
    _table_ = "Servers"
    id = PrimaryKey(int, auto=True)
    components = Set("Component")
    certifications = Set("Certification")
    vendor = Required(str)
    comments = Required(str)


class Component(db.Entity):
    id = PrimaryKey(int, auto=True)
    servers = Set(Server)
    name = Required(str)
    vendor = Required(str)
    comments = Required(str)


class Certification(db.Entity):
    id = PrimaryKey(int, auto=True)
    server = Required(Server)
    Fuel_version = Required(str)
    Date = Required(date)
    Comments = Required(str)


class HardwareId(db.Entity):
    id = PrimaryKey(int, auto=True)
    HW_id = Required(str)
    component_name = Required(unicode)


class Wishlist(db.Entity):
    id = PrimaryKey(int, auto=True)
    Server_name = Required(unicode)


sql_debug(True)
# db.generate_mapping(create_tables=True)