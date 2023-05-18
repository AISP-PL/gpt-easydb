'''
    Simple model for a conversation, where each
    conversation is a list of dialogs. Dataclass.
'''
from argparse import Namespace
from dataclasses import dataclass, field
from datetime import datetime
import logging
from models.dialog import Dialog
from views.ViewDialog import ViewDialog

@dataclass
class Conversation:
    ''' Simple model for a conversation. '''
    # List of dialogs
    dialogs: list = field(init=False, default_factory=list)
    # Timestamp with creation
    timestamp: str = field(init=False, default_factory=lambda : datetime.now())

    def __post_init__(self):
        ''' Initialize class. '''
        pass

    @property
    def filepath(self) -> str:
        ''' Get filepath. '''
        return f'conversations/Conversation_{self.timestamp.strftime("%Y.%m.%d_%H:%M")}.txt'
    
    @property
    def dialogs_count(self) -> int:
        ''' Get dialogs count. '''
        return len(self.dialogs)


    def Add(self, dialog : Dialog):
        ''' Add dialog to conversation. '''
        self.dialogs.append(dialog)

    def Save(self, args : Namespace = None):
        ''' Save conversation to file. '''
        with open(self.filepath, 'w') as file:
            for dialog in self.dialogs:
                text = ViewDialog.View(args=args, dialog=dialog)
                file.write(text)
        
        logging.info(f'Conversation saved to {self.filepath}')
                

    