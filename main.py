'''
    This is the main file for the Auto Vector Database.
'''
import logging
import sys
import argparse
from helpers.AutoVectorDatabase import AutoVectorDatabase
from helpers.LoggingSetup import loggingSetup
from dotenv import load_dotenv

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

    # Prompt : Prompt database in a loop
    prompt = ''
    while (len(prompt) != 'q'):
        # User input : get prompt
        prompt = input('Prompt (write `q` to exit):')
        # Prompt : Check
        if (len(prompt) == 0) or (prompt == 'q'):
            sys.exit(0)

        # Database : Query prompt
        response = database.Query(prompt)

        # Response : Print
        ViewResponse.View(args, response)


if __name__ == '__main__':
    main()
