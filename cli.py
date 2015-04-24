import sys
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
        delete_server(argv)
    elif command == 'update':
        update_server(argv)
    else:
        raise Exception('unknown server command')


def dispatch_components(command, argv):
    if command == 'list':
        list_components(argv)
    elif command == 'add':
        add_component(argv)
    elif command == 'delete':
        delete_component(argv)
    elif command == 'update':
        update_component(argv)
    else:
        raise Exception('unknown server command')


def dispatch_drivers(command, argv):
    if command == 'list':
        list_drivers(argv)
    elif command == 'add':
        add_driver(argv)
    elif command == 'delete':
        pass
    elif command == 'update':
        pass
    else:
        raise Exception('unknown driver command')


def dispatch_certifications(command, argv):
    if command == 'list':
        list_certifications(argv)
    elif command == 'add':
        add_certification(argv)
    elif command == 'delete':
        raise NotImplementedError('delete method will be implemented')
    elif command == 'update':
        raise NotImplementedError('Update method will be implemented')
    else:
        raise Exception('unknown driver command')


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


def get_parser():
    parser = argparse.ArgumentParser(description='Command line parser')
    parser.add_argument('--name', type=str, help='name')
    parser.add_argument('--vendor', type=str, help='vendor name')
    parser.add_argument(
        "--fuel_versions", type=str, nargs='+', help='Fuel build versions list')

    return parser


@db_session
def list_servers(argv):
    table = prettytable.PrettyTable(["name", "vendor", "Fuel versions",  "components",
                                "comments", "specification_url", "availability"])
    parser = get_parser()

    if len(argv) == 1 and (argv[0] == '-h'
       or argv[0] == '--help'
       or argv[0] == 'help'):
        parser.print_help()
        return

    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)

    servers = select_certified_servers(**args)

    for s in servers:
       components = ', '.join([c.name for c in s.components])

       fuel_versions = ' '.join([c.fuel_version.name for c in s.certifications])
       table.add_row([s.name, s.vendor, fuel_versions, components, s.comments, s.specification_url, s.availability])



    print table


@db_session
def list_components(argv):
    table = prettytable.PrettyTable(["name", "vendor", "type", "Fuel versions",
                                "comments"])

    parser = argparse.ArgumentParser(description='List components')
    parser.add_argument('--name', type=str, help='name')
    parser.add_argument('--vendor', type=str, help='vendor name')
    parser.add_argument(
        "--fuel_versions", type=str, nargs='+', help='Fuel build versions list')
    parser.add_argument(
        "--types", type=str, nargs='+', help='Component type list')

    if len(argv) == 1 and (argv[0] == '-h'
       or argv[0] == '--help'
       or argv[0] == 'help'):
        parser.print_help()
        return

    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)

    components = select_certified_components(**args)

    for c in components:
        fuel_versions_set = set()
        fuel_versions = ''

        for server in c.servers:
            [fuel_versions_set.add(x.fuel_version.name) for x in server.certifications]

        for fv in fuel_versions_set:
            fuel_versions += fv + ' '

        table.add_row([c.name, c.vendor, c.type, fuel_versions, c.comments])

    print table


def list_certifications(argv):
    table = prettytable.PrettyTable(["server name", "date", "fuel_version"])

    parser = argparse.ArgumentParser(description='list certifications')
    parser.add_argument('--server_name', type=str, help='name')
    parser.add_argument('--date', type=str, help='vendor name')
    parser.add_argument(
        "--fuel_versions", type=str, nargs='+', help='Fuel build versions list')

    if len(argv) == 1 and (argv[0] == '-h'
       or argv[0] == '--help'
       or argv[0] == 'help'):
        parser.print_help()
        return

    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)

    with db_session:
        certifications = api.select_certification(**args)

        for c in certifications:
            table.add_row((c.server.name, c.date, c.fuel_version.name))

    print table


@db_session
def list_drivers(argv):
    table = prettytable.PrettyTable(["name", "version"])

    parser = argparse.ArgumentParser(description='List drivers')
    parser.add_argument('--name', type=str, help='name')
    parser.add_argument('--version', type=str, help='driver version')

    if len(argv) == 1 and (argv[0] == '-h'
       or argv[0] == '--help'
       or argv[0] == 'help'):
        parser.print_help()
        return

    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)
    drivers = api.select_driver(**args)

    for d in drivers:
        table.add_row((d.name, d.version))

    print table


def add_driver(argv):
    table = prettytable.PrettyTable(["name", "version"])

    parser = argparse.ArgumentParser(description='adding driver')
    parser.add_argument('--name', type=str, help='name', required=True)
    parser.add_argument('--version', type=str, help='version')

    if len(argv) == 1 and (argv[0] == '-h'
       or argv[0] == '--help'
       or argv[0] == 'help'):
        parser.print_help()
        return

    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)

    with db_session:
        d = api.add_driver(**args)


    table.add_row((d.name, d.version))

    print table


def add_server(argv):
    table = prettytable.PrettyTable(["name", "vendor", "Fuel versions",
                                "comments", "specification_url", "availability"])

    parser = argparse.ArgumentParser(description='Command line parser')
    parser.add_argument('--name', type=str, help='name', required=True)
    parser.add_argument('--vendor', type=str, help='vendor name', required=True)
    parser.add_argument('--component_names', type=int, nargs='+', help='component names')

    if len(argv) == 1 and (argv[0] == '-h'
       or argv[0] == '--help'
       or argv[0] == 'help'):
        parser.print_help()
        return

    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)

    with db_session:
        s = api.add_server(**args)

        fuel_versions = ''

        for c in s.certifications:
            fuel_versions += c.fuel_version.name + ', '

    table.add_row([s.name, s.vendor, fuel_versions, s.comments, s.specification_url, s.availability])
    print table


def add_component(argv):
    table = prettytable.PrettyTable(["name", "vendor", "type", "Fuel versions",
                                     "driver name", "comments"])
    parser = argparse.ArgumentParser(description='Command line parser')
    parser.add_argument('--name', type=str, help='name', required=True)
    parser.add_argument('--vendor', type=str, help='vendor name')
    parser.add_argument('--type', type=str, help='type', required=True)
    parser.add_argument('--servers', type=str, nargs='+', help='server name')
    parser.add_argument('--driver', type=str, help='driver name')

    if len(argv) == 1 and (argv[0] == '-h'
       or argv[0] == '--help'
       or argv[0] == 'help'):
        parser.print_help()
        return

    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)

    with db_session:
        c = api.add_component(**args)

        # fetching fuel versions that corresponds to component
        fuel_versions_set = set()
        fuel_versions = ''

        for server in c.servers:
            [fuel_versions_set.add(x.fuel_version.name) for x in server.certifications]

        for fv in fuel_versions_set:
            fuel_versions += fv + ' '

    table.add_row([c.name, c.vendor, c.type, fuel_versions, c.driver.name, c.comments])

    print table


def add_certification(argv):
    table = prettytable.PrettyTable(["date", "fuel_version", "server",
                                "comments"])
    parser = argparse.ArgumentParser(description='Command line parser')

    parser.add_argument('--fuel_version', type=str, help='name', required=True)
    parser.add_argument('--date', type=str, help='date of certification')
    parser.add_argument('--server', type=str, help='server name', required=True)
    parser.add_argument('--comments', type=str, help='comments')

    if len(argv) == 1 and (argv[0] == '-h'
       or argv[0] == '--help'
       or argv[0] == 'help'):
        parser.print_help()
        return

    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)

    with db_session:
        certification = api.add_certification(**args)

    table.add_row((certification.date, certification.fuel_version.name,
                   certification.server.name, certification.comments))

    print table


def update_server(argv):
    table = prettytable.PrettyTable(["name", "vendor", "components",
                                     "specification_url", "availability", "comments"])

    parser = argparse.ArgumentParser(description='Command line parser')
    parser.add_argument('--name', type=str, help='name', required=True)
    parser.add_argument('--vendor', type=str, help='vendor name')
    parser.add_argument('--components', type=str, nargs='+', help='component name')
    parser.add_argument('--availability', type=str, help='availability')
    parser.add_argument('--specification_url', type=str, help='specification url')

    if len(argv) == 1 and (argv[0] == '-h'
       or argv[0] == '--help'
       or argv[0] == 'help'):
        parser.print_help()
        return

    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)
    components = ""

    with db_session:
        s = api.update_server(**args)

        for c in s.components:
            components += c.name + ', '

    table.add_row((s.name, s.vendor, components, s.specification_url, s.availability, s.comments))

    print table


def update_component(argv):
    table = prettytable.PrettyTable(["name", "vendor", "type", "Fuel versions",
                                     "driver name", "comments"])

    parser = argparse.ArgumentParser(description='Command line parser')
    parser.add_argument('--name', type=str, help='name', required=True)
    parser.add_argument('--vendor', type=str, help='vendor name')
    parser.add_argument('--type', type=str, help='type')
    parser.add_argument('--servers', type=str, nargs='+', help='server name')
    parser.add_argument('--driver', type=str, help='driver name')

    if len(argv) == 1 and (argv[0] == '-h'
       or argv[0] == '--help'
       or argv[0] == 'help'):
        parser.print_help()
        return

    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)

    with db_session:
        c = api.update_component(**args)

        fuel_versions_set = set()
        fuel_versions = ''

        for server in c.servers:
            [fuel_versions_set.add(x.fuel_version.name) for x in server.certifications]

        for fv in fuel_versions_set:
            fuel_versions += fv + ' '

    table.add_row([c.name, c.vendor, c.type, fuel_versions, c.driver.name, c.comments])

    print table


def delete_server(argv):
    parser = argparse.ArgumentParser(description='Command line parser')
    parser.add_argument('--name', type=str, help='name', required=True)
    parser.add_argument('--fuel_versions', type=str, help='fuel versions')

    if len(argv) == 1 and (argv[0] == '-h'
       or argv[0] == '--help'
       or argv[0] == 'help'):
        parser.print_help()
        return

    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)

    with db_session:
        print api.delete_server(**args)


def delete_component(argv):
    parser = argparse.ArgumentParser(description='Command line parser')
    parser.add_argument('--name', type=str, help='name')
    parser.add_argument('--hw_id', type=str, help='hardware id')

    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)

    if 'name' not in args \
            and 'hw_id'not in args:
        raise Exception('provide either component name or hardware id')

    with db_session:
        print api.delete_component(**args)


def help_user():
    print 'Command line util for manipulating Hardware compatibility list \n' \
          'database' \
          'There are 4 entities you are able to manipulate\n' \
          ' - server\n' \
          ' - component\n' \
          ' - driver\n' \
          ' -certification\n' \
          '' \
          'Each of them supports 4 commands: add, list, delete, update\n' \
          'type <entity_type> <command> --help\n' \
          'to see detailed explanation of arguments\n'


def main():
    while True:
        sys.stdout.write(">>>")
        s = raw_input()

        if s == 'exit':
            return
        #exmaples of commands
        #servers list
        # s = 'components list --fuel_version Fuel5.1 Fuel6.1'
        # s = 'components list --type RAID --fuel_version Fuel5.1 Fuel6.1'
        # s = 'server list --fuel_version Fuel5.1 Fuel6.1'
        # s = "server add --name 'My_server' --vendor 'Some_vendor'"
        # s = "component add --name 'aa' --vendor 'bb' --type 'NIC' --server_ids 1"
        try:
            array = parse_string(s)

            object_type = array[0]

            if len(array) >= 2:
                command = array[1]

            if len(array) > 2:
                argv = array[2:]
            else:
                argv = []

            if object_type == 'server':
                dispatch_servers(command=command, argv=argv)
            elif object_type == 'component':
                dispatch_components(command=command, argv=argv)
            elif object_type == 'driver':
                dispatch_drivers(command=command, argv=argv)
            elif object_type == 'certification':
                dispatch_certifications(command=command, argv=argv)
            elif object_type == 'help':
                help_user()
            else:
                print 'Wrong command, pleasy type command help'
        except Exception:
            pass
        finally:
            pass

if __name__ == '__main__':
    main()






