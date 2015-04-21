from persistance.api import select_certified_servers, select_certified_components
from pony.orm.core import db_session
import prettytable
import argparse


def get_parser():
    parser = argparse.ArgumentParser(description='Command line parser')
    parser.add_argument('--name', type=str, help='name')
    parser.add_argument('--vendor', type=str, help='vendor name')
    parser.add_argument(
        "--fuel_versions", type=str, nargs='+', help='Fuel build versions list')

    return parser


@db_session
def list_servers(argv):
    table = prettytable.PrettyTable(["id", "name", "vendor", "Fuel versions",
                                "comments", "specification_url", "availability"])
    parser = get_parser()
    arg_obj = parser.parse_args(argv)
    args = vars(arg_obj)

    servers = select_certified_servers(**args)


    for s in servers:
       fuel_versions = ' '.join([c.fuel_version for c in s.certifications])
       table.add_row([s.id, s.name, s.vendor, fuel_versions, s.comments, s.specification_url, s.availability])

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


def main():
    while True:
        # s = raw_input()
        #exmaples of commands
        s = 'list_components --fuel_version Fuel5.1 Fuel6.1'
        cmd, argv = s.split()[0], s.split()[1:]

        if cmd == 'list_servers':
            list_servers(argv=argv)
        elif cmd == 'list_components':
            list_components(argv=argv)
        else:
            raise Exception('Wrong command')

if __name__ == '__main__':
    main()






