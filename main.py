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
        ViewResponse.View(response)


if __name__ == '__main__':
    main()
