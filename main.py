'''
    This is the main file for the Auto Vector Database.
'''
import logging
import sys
from helpers.AutoVectorDatabase import AutoVectorDatabase
from helpers.LoggingSetup import loggingSetup
from dotenv import load_dotenv

from views.ViewResponse import ViewResponse


def main():
    ''' Main function '''
    # Load .env file
    load_dotenv()

    # Logging : Setup
    loggingSetup(console_log_enabled=True,
                 logfile_enabled=False)

    # Database : Create
    database = AutoVectorDatabase(databasePath='database')

    # User input : get prompt
    prompt = input('Prompt:')
    # Prompt : Check
    if (len(prompt) == 0):
        logging.error('Prompt is empty.')
        sys.exit(-1)

    # Database : Query prompt
    response = database.Query(prompt)

    # Response : Print
    ViewResponse.View(response)


if __name__ == '__main__':
    main()
