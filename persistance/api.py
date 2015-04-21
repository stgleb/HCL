

# method get server by name or list of all servers
from persistance.models import Server, Component
from pony.orm.core import select, db_session


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
def select_certified_servers(fuel_versions=None, server_name=None, vendor_name=None):
    servers = select(s for s in Server)[:]

    if fuel_versions is not None:
        result = []

        for server in servers:
            versions = server.certifications.fuel_version

            for fv in fuel_versions:
                if fv in versions:
                    result.append(server)
                    break

        servers = result

    if server_name is not None:
        servers = filter(lambda s: server_name in s.name, servers)

    if vendor_name is not None:
        servers = filter(lambda s: vendor_name in s.vendor, servers)

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
    components = select(c for c in Component)[:]

    if types is not None:
        components = filter(lambda c: c.type in types, components)

    if fuel_versions is not None:
        result = []

        for c in components:

            for server in c.servers:
                if server is not None:
                    versions = server.certifications.fuel_version

                    if has_intersection(versions, fuel_versions):
                        result.append(c)
                        break

        components = result

    if vendor is not None:
        components = filter(lambda c: vendor in c.vendor, components)

    if name is not None:
        components = filter(lambda c: name in c.name, components)

    return components


select_servers("Super")
select_certified_servers(fuel_versions=['Fuel 5.1', 'Fuel 6.0', 'Fuel 5.0', 'Fuel 4.1', 'Fuel 6.1'],
                         vendor_name='Super')
select_components()
select_certified_components(types=['NIC', 'RAID'], fuel_versions=['Fuel 5.1', 'Fuel 6.0', 'Fuel 5.0', 'Fuel 4.1', 'Fuel 6.1'],
                            vendor='Intel')