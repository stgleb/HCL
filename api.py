# method get server by name or list of all servers
from datetime import datetime

from decorators import lower_case
from models import Server, Component, Certification, db, Driver, FuelVersion, Type
from pony.orm.core import select, db_session, left_join, count, get


def has_intersection(set_1, set2):
    for elem in set_1:
        if elem in set2:
            return True

    return False


def check_type(type_name):
    if select(t for t in Type
              if t.name == type_name).count() == 0:
        return False

    return True


@db_session
def select_servers(name=None):
    servers = select(s for s in Server)[:]

    if name is not None:
        servers = filter(lambda s: name in s.name, servers)

    return servers


@db_session
def select_certified_servers(fuel_versions=None, name=None, vendor=None):
    if fuel_versions == ['None']:
        # select all servers that was not certified.
        servers = left_join((s, count(c))
                            for s in Server for c in s.certifications
                            if count(c) == 0)[:]
        servers = [s[0] for s in servers]
    elif fuel_versions is not None:
        #select servers whose certifications are in fuel_versions.
        servers = left_join((s, count(c))
                            for s in Server for c in s.certifications
                            if count(c) > 0
                            and c.fuel_version.name in fuel_versions)[:]
        servers = [s[0] for s in servers]
    else:
        servers = select(s for s in Server)[:]

    if name is not None:
        servers = filter(lambda s: name in s.name, servers)

    if vendor is not None:
        servers = filter(lambda s: vendor in s.vendor, servers)

    return servers


@db_session
def select_components(types=None, name=None):
    components = select(c for c in Component)[:]

    if types is not None:
        components = filter(lambda c: c.type in types)

    if name is not None:
        components = filter(lambda c: name in c.name)

    return components


@db_session
def select_certified_components(types=None, fuel_versions=None, server=None,
                                vendor=None, name=None):
    if fuel_versions == ['None']:
        components = left_join((component, server, count(certification))
                               for component in Component
                               for server in component.servers
                               for certification in server.certifications
                               if count(server.certifications) == 0 or
                               count(component.servers) == 0)[:]

        components = [c[0] for c in components]

        print components
    elif fuel_versions is not None and fuel_versions != []:
        components = left_join((component, count(server), count(certification))
                               for component in Component
                               for server in component.servers
                               for certification in server.certifications
                               if count(server.certifications) > 0 and
                               certification.fuel_version.name in fuel_versions)[:]

        components = [c[0] for c in components]

        print components
    else:
        components = select(c for c in Component)[:]

    if types is not None:
        components = filter(lambda c: c.type in types, components)

    if vendor is not None:
        components = filter(lambda c: vendor in c.vendor, components)

    if name is not None:
        components = filter(lambda c: name in c.name, components)

    if server is not None and server != '':
        components = filter(lambda c: name in [s.name for s in c.servers], components)

    return components


@lower_case
def select_driver(name=None, version=None):
    with db_session:
        drivers = select(d for d in Driver)[:]

        if name is not None:
            drivers = filter(lambda d: d.name == name,
                             drivers)

        if version is not None:
            drivers = filter(lambda d: d.version == version,
                             drivers)

    return drivers


@lower_case
def select_certification(server_name=None, date=None, fuel_versions=None):
    with db_session:
        certifications = select(c for c in Certification)[:]

        if server_name is not None:
            certifications = filter(lambda c: c.server.name == server_name,
                                    certifications)

        if date is not None:
            certifications = filter(lambda c: c.date == date,
                                    certifications)

        if fuel_versions is not None:
            certifications = filter(lambda c: c.fuel_version.name in fuel_versions,
                                    certifications)

    return certifications


@lower_case
@db_session
def select_fuel_versions(name=None):
    fuel_versions = select(fv for fv in FuelVersion)[:]

    if name is not None:
        fuel_versions = filter(lambda fv: fv.name == name, fuel_versions)

    return fuel_versions


@lower_case
@db_session
def select_types(name=None):
    types = select(type for type in Type)[:]

    if name is not None:
        types = filter(lambda type: type.name, types)

    return types

@lower_case
def add_server(component_names=None, certification_ids=None,
               name="", vendor="", comments="",
               specification_url=None, availability=None):
    with db_session:
        components = None
        certifications = None

        if component_names is not None:
            components = select(c for c in Component if c.name in component_names)[:]

        if certification_ids is not None:
            certifications = select(c for c in Certification
                                    if c.id in certification_ids)[:]

        server = Server(vendor=vendor, name=name, comments=comments)

        if specification_url is not None:
            server.specification_url = specification_url

        if availability is not None:
            server.availability = availability

        if components is not None:
            for c in components:
                server.components.add(c)

        if certifications is not None:
            for c in certifications:
                server.certifications.add(c)

    return server


@lower_case
def add_component(servers=None, type="", name="", vendor="",
                  comments="", hw_id="", driver=None):
    with db_session:
        if select(t for t in Type
                  if t.name == type).count() == 0:
            raise Exception('Unknown component type')

        if driver is None:
            raise Exception('Driver is not specified')
        else:
            driver = get(d for d in Driver if d.name == driver)

        component = Component(type=type, name=name,
                              vendor=vendor, comments=comments, driver=driver, hw_id=hw_id)

        if servers is not None:
            servers = select(s for s in Server if s.id in servers)[:]

            for s in servers:
                component.servers.add(s)

    return component


@lower_case
def add_certification(server=None, fuel_version=None,
                      date=datetime.now(), comments=None):
    with db_session:
        if fuel_version is None:
            raise Exception('Fuel version is not specified')
        else:
            fuel_version = FuelVersion.get(lambda fv: fuel_version == fv.name)

        if server is None:
            raise Exception('Specify server name')

        server = Server.get(lambda s: s.name == server)

        if server is None:
            raise Exception('No such server in database')

        certification = Certification(server=server, fuel_version=fuel_version,
                                      date=date)

        if comments is not None:
            certification.comments = comments

        # establishing  connection between server and certification
        certification.server = server
        server.certifications.add(certification)

    return certification


@lower_case
@db_session
def add_driver(name, version):
    with db_session:
        if select(d for d in Driver
                  if d.name == name and
                  d.version == version).count() > 0:
            raise Exception('Driver already exists')

        driver = Driver(name=name, version=version)

    return driver


@lower_case
@db_session
def add_driver_to_fuel(fuel_version, name, version):
    with db_session:
        if select(d for d in Driver
                  if d.name == name and
                  d.version == version).count() > 0:
            raise Exception('Driver already exists')

        fuel_version = get(fv for fv in FuelVersion if fv.name == fuel_version)

        if fuel_version is None:
            raise Exception('Unknown Fuel version')

        driver = Driver(fuel_version=fuel_version,
                        name=name, version=version)

    return driver


@lower_case
@db_session
def add_fuel_version(name=None, driver_names=None):
    with db_session:
        if driver_names is not None:
            drivers = select(d for d in Driver
                             if d.name in driver_names)[:]

        fuel_version = FuelVersion(name, drivers=drivers)

    return fuel_version


@lower_case
@db_session
def add_type(name):
    with db_session:
        type = Type(name=name)

    return type


@lower_case
@db_session
def update_server(components=None, name=None, vendor=None,
                  comments=None, specification_url=None, availability=None):
    server = Server.get(lambda s: s.name == name)

    if name is None:
        raise Exception('Server name is not specified')

    if vendor is not None:
        server.vendor = vendor

    if comments is not None:
        server.comments = comments

    if specification_url is not None:
        server.specification_url = \
        specification_url

    if availability is not None:
        server.availability = availability

    if components is not None:
        cmp = select(c for c in Component if c.name in components)[:]

        for c in cmp:
            server.components.add(c)
            c.servers.add(server)

    return server


@lower_case
@db_session
def update_component(servers=None, type=None, name=None, vendor=None,
                     comments=None, hw_id=None, driver=None):
    component = get(c for c in Component if c.name == name)

    if servers:
        servers = select(s for s in Server if s.name in servers)[:]
        component.servers.clear()

        for s in servers:
            component.servers.add(s)

    if type is not None and check_type(type):
        component.type = type

    if name is not None:
        component.name = name

    if vendor is not None:
        component.vendor = vendor

    if comments is not None:
        component.comments = comments

    if hw_id is not None:
        component.hw_id = hw_id

    if driver is not None:
        driver = Driver.get(lambda d: d.name == driver)

        if driver is not None:
            component.driver = driver

    return component


@lower_case
@db_session
def delete_server(name="", fuel_versions=None):
    if fuel_versions is None:
        db.execute("DELETE FROM Server "
                   "WHERE name='{0}';".format(name))

        return "Request for deleting server {} " \
               "has been accepted".format(name)
    else:
        return delete_server_from_certification(name, fuel_versions)


@lower_case
def delete_server_from_certification(name, fuel_versions):
    certifications = select(certification
                            for server in Server
                            for certification in Certification
                            if certification.fuel_version.name in
                            fuel_versions and
                            server.name == name)[:]

    with db_session:
        for c in certifications:
             db.execute("DELETE FROM Certification "
                   "WHERE id='{0}';".format(c.id))


@lower_case
def delete_component(name=None, hw_id=None):
    if name is not None:
        cmp = select(c for c in Component if c.name == name)[:]
    else:
        raise Exception('Specify component name')

    if hw_id is not None:
        components = filter(lambda c: c.hw_id == hw_id,
                            cmp)
    else:
        components = cmp

    if len(components) == 0:
        return "Nothing to delete"

    if len(components[0].servers) > 0:
        return "Cannot delete component that is used in servers"
    else:
        db.execute("DELETE FROM Component "
               "WHERE name='{0}';".format(components[0].name))
        return "Request for deleting component {0} " \
               "has been accepted".format(name)


if __name__ == '__main__':
    # select_servers("Super")

    select_certified_servers(fuel_versions=['Fuel5.0', 'Fuel6.0'],
                             vendor='Super')
    select_components()
    select_certified_components(types=['NIC', 'RAID'],
                                fuel_versions=['Fuel5.1',
                                               'Fuel6.0',
                                               'Fuel5.0',
                                               'Fuel4.1',
                                               'Fuel6.1'],
                                vendor='Intel')

    server_id = add_server(component_ids=[2, 6], vendor="IBM",
                           name="IBM Z-machine",
                           specification_url="www.ibm.com")

    certification_id = add_certification(servers=server_id,
                                         fuel_version='Fuel6.0')

    component_id = add_component(servers=[server_id],
                                 type="NIC",
                                 name='some cool ibm stuff',
                                 vendor='IBM')