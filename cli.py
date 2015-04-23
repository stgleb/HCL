from persistance import api
from persistance.api import select_certified_servers, select_certified_components
from pony.orm.core import db_session
import prettytable
import argparse


def dispatch_servers(command, argv):
    if command == 'list':
        list_servers(argv)
    elif command == 'add':
        add_server(argv)
    elif command == 'delete':
        pass
    elif command == 'update':
        pass
    else:
        raise Exception('unknown server command')


def parse_string(s):
    result = []
    quoted = False
    cur = ""

    for c in s:
        cur += c

        if c in {'"', "'"} and quoted == True:
            if cur != '':
                result.append(cur[:len(cur) - 1])
            cur = ""
            quoted = False
        elif c in {'"', "'"} and quoted == False:
            cur = cur[1:]
            quoted = True
        elif quoted == False and c == ' ':
            if cur != ' ':
                result.append(cur[:len(cur) - 1])
            cur = ""

    if cur != '':
        result.append(cur)
    return result


def dispatch_components(command, argv):
    if command == 'list':
        list_components(argv)
    elif command == 'add':
        add_component(argv)
    elif command == 'delete':
        pass
    elif command == 'update':
        pass
    else:
        raise Exception('unknown server command')


def get_parser():
    parser = argparse.ArgumentParser(description='Command line parser')
    parser.add_argument('--name', type=str, help='name')
    parser.add_argument('--vendor', type=str, help='vendor name')
    parser.add_argument(
        "--fuel_versions", type=str, nargs='+', help='Fuel build versions list')

    return parser


@db_session
def list_servers(argv):
    table = prettytable.PrettyTable(["name", "vendor", "Fuel versions",
                                "comments", "specification_url", "availability"])
    parser = get_parser()
    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)

    servers = select_certified_servers(**args)


    for s in servers:
       fuel_versions = ' '.join([c.fuel_version.name for c in s.certifications])
       table.add_row([s.name, s.vendor, fuel_versions, s.comments, s.specification_url, s.availability])

    print table


@db_session
def list_components(argv):
    table = prettytable.PrettyTable(["id", "name", "vendor", "type", "Fuel versions",
                                "comments"])
    parser = get_parser()
    parser.add_argument(
        "--types", type=str, nargs='+', help='Component type list')
    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)

    components = select_certified_components(**args)

    for c in components:
        fuel_versions_set = set()
        fuel_versions = ''

        for server in c.servers:
            [fuel_versions_set.add(x.fuel_version) for x in server.certifications]

        for fv in fuel_versions_set:
            fuel_versions += fv + ' '

        table.add_row([c.id, c.name, c.vendor, c.type, fuel_versions, c.comments])

    print table


def add_server(argv):
    table = prettytable.PrettyTable(["id", "name", "vendor", "Fuel versions",
                                "comments", "specification_url", "availability"])

    parser = argparse.ArgumentParser(description='Command line parser')
    parser.add_argument('--name', type=str, help='name', required=True)
    parser.add_argument('--vendor', type=str, help='vendor name', required=True)
    parser.add_argument('--certification_ids', type=int, nargs='+', help='certification ids')
    parser.add_argument('--component_ids', type=int, nargs='+', help='component ids')

    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)

    with db_session:
        s = api.add_server(**args)

    table.add_row([s.id, s.name, s.vendor, s.comments, s.specification_url, s.availability])
    print table


def add_component(argv):
    table = prettytable.PrettyTable(["id", "name", "vendor", "type", "Fuel versions",
                                "comments"])
    parser = argparse.ArgumentParser(description='Command line parser')
    parser.add_argument('--name', type=str, help='name', required=True)
    parser.add_argument('--vendor', type=str, help='vendor name', required=True)
    parser.add_argument('--type', type=str, help='type', required=True)
    parser.add_argument('--server_ids', type=int, nargs='+', help='server ids')

    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)

    with db_session:
        c = api.add_component(**args)

        # fetching fuel versions that corresponds to component
        fuel_versions_set = set()
        fuel_versions = ''

        for server in c.servers:
            [fuel_versions_set.add(x.fuel_version) for x in server.certifications]

        for fv in fuel_versions_set:
            fuel_versions += fv + ' '

    table.add_row([c.id, c.name, c.vendor, c.type, fuel_versions, c.comments])

    print table


def delete_server(server_id):
    # select(s for s in Server if s.id == server_id)
    pass


def delete_component(component_id):
    pass


def main():
    while True:
        s = raw_input()
        #exmaples of commands
        #servers list
        # s = 'components list --fuel_version Fuel5.1 Fuel6.1'
        # s = 'components list --type RAID --fuel_version Fuel5.1 Fuel6.1'
        # s = 'server list --fuel_version Fuel5.1 Fuel6.1'
        # s = "server add --name 'My_server' --vendor 'Some_vendor'"
        # s = "component add --name 'aa' --vendor 'bb' --type 'NIC' --server_ids 1"
        array = parse_string(s)
        object_type, command= array[0], array[1]

        if len(array) > 2:
            argv = array[2:]
        else:
            argv = []

        if object_type == 'server':
            dispatch_servers(command=command, argv=argv)
        elif object_type == 'component':
            dispatch_components(command=command, argv=argv)
        else:
            raise Exception('Wrong command')


if __name__ == '__main__':
    main()






