'''
    Vector database query response.
'''

from dataclasses import dataclass


@dataclass
class Response:
    '''
        Vector database query response.
    '''
    # Response : Response text
    text: str = None
    # Response : Response sources
    sources: list = None
