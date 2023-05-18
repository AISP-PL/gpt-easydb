'''
    Simple dialog line with question and answer.
    Dataclass for a dialog line.
'''
from dataclasses import dataclass, field

from helpers.Response import Response

@dataclass
class Dialog:
    ''' Simple dialog line with question and answer. '''
    # Question
    question: str = ''
    # Answer
    answer: Response = field(init=True, default=None)

    def __post_init__(self):
        ''' Initialize class. '''
        pass