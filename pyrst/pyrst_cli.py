# coding=utf-8
#! usr/bin/env/python

import argparse
import json
import yaml
from base64 import b64decode

from pyrst.client import BirstClient
from pyrst.exceptions import MissingCredentialsException
from pyrst.handlers import CsvHandler, JsonHandler, DfHandler


parser = argparse.ArgumentParser(description='A Birst client.')

parser.add_argument('-q', '--query',
                    required = True)
parser.add_argument('-s', '--space',
                    required = True,
                    type = str)
parser.add_argument('-u', '--username',
                    required = False,
                    type = str)
parser.add_argument('-p', '--password',
                    required = False,
                    type = str)
parser.add_argument('-i', '--instance',
                    required = False,
                    type = str)
parser.add_argument('-f', '--configfile',
                    required = False,
                    type = str)
parser.add_argument('-o', '--outputfile',
                    required = False,
                    type = str)
parser.add_argument('-H', '--handler',
                    required = False,
                    default = "JSON",
                    choices = [None, "CSV", "JSON", "DF", "XLS"])


def main():
    args = parser.parse_args()

    if args.username and args.password:
        cl = BirstClient(user = args.username,
                         password = args.password,
                         instance = args.instance if args.instance else "app2102")
    elif args.configfile:
        with open(args.configfile, 'r') as config_file:
            config = yaml.load(config_file)
            password = b64decode(config["password"]) if config["password_is_encrypted"] else config["password"]

        cl = BirstClient(user = config["username"],
                         password = password,
                         instance = getattr(config, "instance", "app2102"))
    else:
        raise MissingCredentialsException

    cl.login()

    _handler_map = {"CSV": CsvHandler,
                    "JSON": JsonHandler,
                    "DF": DfHandler,
                    "XLS": DfHandler}

    _res = cl.retrieve(space = args.space,
                      query = args.query,
                      handler = _handler_map[args.handler])

    if args.outputfile:
        if args.handler == "XLS":
            _res.to_excel(args.outputfile,
                          index = False,
                          header = True,
                          na_rep = "N/A",
                          float_format="%.2f")
        else:
            with open(args.outputfile, 'w') as output_file:
                if args.handler == "JSON":
                    json.dump(_res, output_file)
                elif args.handler == "DF":
                    output_file.write(_res.to_string())
                elif args.handler == "XLS":
                    _res.to_excel()
                else:
                    output_file.write(str(_res))
    else:
        print _res

if __name__ == '__main__':
    main()