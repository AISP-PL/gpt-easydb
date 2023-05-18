'''
    This is the main file for the Auto Vector Database.
'''
import logging
import sys
import argparse
from helpers.AutoVectorDatabase import AutoVectorDatabase
from helpers.LoggingSetup import loggingSetup
from dotenv import load_dotenv
from controllers.conversation import Conversation
from models.dialog import Dialog
from views.ViewResponse import ViewResponse

def parseArguments():
    ''' Parse command line arguments '''
    # Create parser
    parser = argparse.ArgumentParser(
        description='Auto Vector Database')

    # Add arguments
    parser.add_argument('-vs', '--view-sources', action='store_true',
                        help='View sources of response.')

    # Parse arguments
    args = parser.parse_args()

    # Return arguments
    return args


def main():
    ''' Main function '''
    # Load .env file
    load_dotenv()

    # Arguments : Parse
    args = parseArguments()

    # Logging : Setup
    loggingSetup(console_log_enabled=True,
                 logfile_enabled=False)

    # Database : Create
    database = AutoVectorDatabase(databasePath='database')

    # Conversation : Create
    conversation = Conversation()

    # Prompt : Prompt database in a loop
    prompt = ''
    while (len(prompt) != 'q'):
        # User input : get prompt
        prompt = input('Prompt (write `q` to exit):')
        # Prompt : Check
        if (len(prompt) == 0) or (prompt == 'q'):
            break

        # Database : Query prompt
        response = database.Query(prompt)

        # Response : Print
        ViewResponse.View(args, response)

        # Conversation : Add dialog
        conversation.Add(Dialog(question=prompt, answer=response))

    # Conversation : Save
    conversation.Save(args=args)


if __name__ == '__main__':
    main()
