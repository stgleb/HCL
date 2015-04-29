import argparse
import sys


def dump(email, password, document_id):
     client = gspread.Client(auth=('user@example.com', 'qwertypassword'))

     
def parse_args(argv):
    parser = argparse.ArgumentParser(description="command line parser")
    parser.add_argument('--email', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    parser.add_argument('--document_id', type=str, required=True)

    return parser.parse_args(argv)


def main(argv):
    arg_obj = parse_args(argv)


if __name__ == '__main__':
    main(sys.argv[1:])