'''
    Abstract class to view response object
'''
from helpers.Response import Response
from argparse import Namespace


class ViewResponse:
    ''' View response object '''

    @staticmethod
    def View(args : Namespace , response: Response):
        ''' View response '''
        print('# AI\n')
        print(f'{response.text}\n')

        if (args.view_sources):
            print('# Sources.\n')
            print(f'{response.sources}\n')
        
        print('-------------------\n')
