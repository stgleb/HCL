# method get server by name or list of all servers
from persistance.models import Server, Component, Certification
from pony.orm.core import select, db_session, left_join, count


def has_intersection(set_1, set2):
    for elem in set_1:
        if elem in set2:
            return True

    return False


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
                            and c.fuel_version in fuel_versions)[:]
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
def select_certified_components(types=None, fuel_versions=None, vendor=None, name=None):
    if fuel_versions == ['None']:
        components = left_join((component, server, count(certification))
                               for component in Component
                               for server in component.servers
                               for certification in server.certifications
                               if count(server.certifications) == 0 or
                               count(component.servers) == 0)[:]

        components = [c[0] for c in components]

        print components
    elif fuel_versions is not None:
        components = left_join((component, count(server), count(certification))
                               for component in Component
                               for server in component.servers
                               for certification in server.certifications
                               if count(server.certifications) > 0 and
                               certification.fuel_version in fuel_versions)[:]

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

    return components


@db_session
def add_server(component_ids, certification_ids, vendor, comments,
               specification_url, availability):
    components = select(c for c in Component if c.id in component_ids)
    certifications = select(c for c in Certification
                            if c.id in certification_ids)

    server = Server(vendor=vendor, comments=comments,
                    specification_url=specification_url,
                    availability=availability)

    for c in components:
        server.components.add(c)

    for c in certifications:
        server.certifications.add(c)


def add_component(server_ids, name, vendor, comments):
    servers = select(s for s in Server if s.id in server_ids)
    component = Component(name=name, vendor=vendor, comments=comments)

    for s in servers:
        component.servers.add(s)


def add_certification(server_id, fuel_version, date, comments):
    server = Server.get(s for s in Server if s.id == server_id)
    certification = Certification(fuel_version=fuel_version,
                                  date=date, comments=comments)
    # establishing  connection between server and certification
    certification.server = server
    server.certifications.add(certification)


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