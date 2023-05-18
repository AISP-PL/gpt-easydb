'''
    Abstract class to view response object
'''
from models.dialog import Dialog
from argparse import Namespace


class ViewDialog:
    ''' View response object '''

    @staticmethod
    def View(args : Namespace , dialog: Dialog) -> str:
        ''' View response '''
        text = ''
        text += f"Q:{dialog.question}\n"
        if (dialog.answer is not None):
            text += f"A:{dialog.answer.text}\n"


        return text
