'''
    Abstract class to view response object
'''
from helpers.Response import Response


class ViewResponse:
    ''' View response object '''

    @staticmethod
    def View(response: Response):
        ''' View response '''
        print('# AI\n')
        print(f'{response.text}\n')
        print('-------------------\n')
        print('# Sources.\n')
        print(f'{response.sources}\n')
