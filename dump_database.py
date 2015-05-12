import argparse
import json
import sys
import csv
from models import Server, Component, Driver
from pony.orm import db_session


@db_session
def dump(file_name):
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        vendors = set(['Intel', 'Supermicro', 'Lenovo', 'Mellanox',
                   'HP', 'Dell', 'Ericsson'])
        default = Driver(name="default", version="1.0")

        for i, row in enumerate(reader):
            if i > 2:
                print row
                server_name = row[1]
                specification_url = row[2]
                availability = row[3]
                comments = row[7]

                if server_name in ['', '- // -']:
                    continue

                if len(set(server_name).intersection(vendors)) > 0:
                    server_vendor = set(server_name).intersection(vendors)[0]
                else:
                    server_vendor = " "

                if row[3] not in ['', '?']:
                    nic_name = row[3]
                    nic_vendor = None

                    if len(set(nic_name).intersection(vendors)) > 0:
                        nic_vendor = set(nic_name).intersection(vendors)[0]

                    if nic_vendor is not None:
                        nic = Component(name=nic_name, vendor=nic_vendor,
                                        type="nic", driver=default)
                    else:
                        nic = Component(name=nic_name, type="nic", driver=default)

                if row[5] not in ['', '?']:
                    chipset_name = row[5]
                    chipset_vendor = None

                    if len(set(chipset_name).intersection(vendors)) > 0:
                        chipset_vendor = set(chipset_name).intersection(vendors)[0]

                    if chipset_vendor is None:
                        chipset_vendor = " "

                    chipset = Component(name=repr(chipset_name),
                                        vendor=chipset_vendor,
                                        type="chipset", driver=default)


                s = Server(name=server_name, specification_url=specification_url,
                           availability=availability, comments=repr(comments), vendor=server_vendor)


def parse_args(argv):
    parser = argparse.ArgumentParser(description="command line parser")
    parser.add_argument('--file_name', type=str, required=True)

    return parser.parse_args(argv)


def main(argv):
    arg_obj = parse_args(argv)
    dump(arg_obj.file_name)


if __name__ == '__main__':
    main(sys.argv[1:])