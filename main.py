'''
    This is the main file for the Auto Vector Database.
'''
from helpers.AutoVectorDatabase import AutoVectorDatabase
from dotenv import load_dotenv


def main():
    ''' Main function '''
    # Load .env file
    load_dotenv()

    # Database : Create
    database = AutoVectorDatabase(databasePath='database')

    # User input : get prompt
    prompt = input('Prompt database:')

    # Database : Query prompt
    response = database.Query(prompt)

    # Response : Print
    print(response)


if __name__ == '__main__':
    main()
