'''
Created on 3 sty 2020
@author: spasz
'''
import json
import os
import logging
from json.decoder import JSONDecodeError


def jsonRead(filename: str) -> dict:
    ''' Reads json as dict.'''
    # File not exists
    if (not os.path.isfile(filename)):
        logging.fatal('(Json) File %s not exists!', filename)
        return {}

    with open(filename, 'r') as f:
        try:
            data = json.load(f)
            logging.debug('(Json) Readed %s.\n', (filename))
            return data
        except JSONDecodeError:
            logging.error('(Json) Invalid JSON file content!')
            return {}


def jsonWrite(filename: str, data: dict) -> None:
    ''' Write data dict as json.'''
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=False, default=str)

    logging.debug('(Json) Written %s.\n', filename)


def jsonShow(data: dict):
    ''' Show json data.'''
    logging.info('\n%s\n', json.dumps(
        data, indent=4, sort_keys=False, default=str))


def jsonToStr(data: dict):
    ''' Returns string json data.'''
    return json.dumps(data, indent=4, sort_keys=False, default=str)


def jsonFromStr(data: str) -> dict:
    ''' Returns string json data.'''
    return json.loads(data)
