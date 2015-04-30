import argparse
import json
import sys
import gspread
from oauth2client.client import SignedJwtAssertionCredentials


def save_to_db(items):
    print items


def authorize(file_name):
    json_key = json.load(open(file_name))
    scope = ['https://spreadsheets.google.com/feeds', 'https://docs.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    gc = gspread.authorize(credentials)

    return gc


def dump(file_name, document_id):
    gc = authorize(file_name)
    sht = gc.openall()
    worksheet = sht.get_worksheet(0)

    for row_index in range(worksheet.row_count):
        save_to_db(worksheet.row_values(row_index))


def parse_args(argv):
    parser = argparse.ArgumentParser(description="command line parser")
    parser.add_argument('--file_name', type=str, required=True)
    parser.add_argument('--document_id', type=str, required=True)

    return parser.parse_args(argv)


def main(argv):
    arg_obj = parse_args(argv)
    dump(arg_obj.file_name, arg_obj.document_id)

if __name__ == '__main__':
    main(sys.argv[1:])