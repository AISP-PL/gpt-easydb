'''
    Class creates automatically vector database from texts
    in given directory.
'''
from dataclasses import field, dataclass
import logging
import os
from typing import Any
from llama_index import (
    GPTVectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    download_loader
)

from helpers.Response import Response

# Llama hub : Download .pdf loader
PDFReader = download_loader('PDFReader')


@dataclass
class AutoVectorDatabase:
    '''
        Class creates automatically vector database from texts
        in given directory.
    '''
    # Vector database
    vectorDatabase: GPTVectorStoreIndex = field(
        init=False, repr=False, default=None)
    # Vector database query engine
    queryEngine: Any = field(init=False, repr=False, default=None)
    # Database directory
    databasePath: str = field(init=True, default='database')
    # Acceptable file extensions
    extensions: list = field(
        init=True, default_factory=lambda:  ['.txt', '.pdf'])
    # List of all acceptable files found in database directory
    files: list = field(init=False, repr=False, default_factory=list)
    # Is database modified?
    isModified: bool = field(init=False, repr=False, default=False)

    def __post_init__(self):
        '''
            Initialize class.
        '''
        if (not os.path.exists(self.databasePath)):
            raise Exception('Database directory does not exist.')

        # Files : Get all files in directory
        self.ProcessPathFiles(self.databasePath)

        # Files : Read previous files list
        previousFiles = []
        if (os.path.exists(self.filesFilepath)):
            with open(self.filesFilepath, 'r') as f:
                previousFiles = f.read().splitlines()

        # Files : Check if files list is changed
        if (set(previousFiles) != set(self.files)):
            self.isModified = True

        # Files : Save files list to file
        with open(self.filesFilepath, 'w') as f:
            for file in self.files:
                f.write(file+'\n')

        # Database : Load previous database version json.
        try:
            storage = StorageContext.from_defaults(persist_dir='storage')
            self.vectorDatabase = load_index_from_storage(storage)
        except ValueError:
            logging.warning(
                '(AutoVectorDatabase) Previous database version not found.')
            pass

        # Database : If not exists then create.
        if (self.vectorDatabase is None):
            self.Create()

        # Database : Create query context
        self.queryEngine = self.vectorDatabase.as_query_engine()

    @property
    def databaseFilepath(self) -> str:
        ''' Get database filepath. '''
        return f'{self.databasePath}/database.json'

    @property
    def filesFilepath(self) -> str:
        ''' Get files filepath. '''
        return f'{self.databasePath}/files.list'

    @property
    def files_count(self) -> int:
        ''' Get files count. '''
        return len(self.files)

    @property
    def files_txt_count(self) -> int:
        ''' Get files count. '''
        return len([file for file in self.files if os.path.splitext(file)[1] == '.txt'])

    @property
    def files_pdf_count(self) -> int:
        ''' Get files count. '''
        return len([file for file in self.files if os.path.splitext(file)[1] == '.pdf'])

    def ProcessPathFiles(self, path: str):
        ''' Process all files in given path. '''
        # Files : Scann all files and directories in database directory
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            # File : Check if path is file
            if (os.path.isfile(filepath)):
                # Extension : Is Acceptable?
                if (os.path.splitext(filename)[1] in self.extensions):
                    self.files.append(filepath)

            # Directory : Recursion
            elif (os.path.isdir(filepath)):
                self.ProcessPathFiles(filepath)

    def Create(self):
        ''' Create vector database from found files. '''
        # Documents : Create documents list
        db_documents = []

        for filepath in self.files:
            extension = os.path.splitext(filepath)[1]

            if (extension == '.txt'):
                documents = SimpleDirectoryReader(
                    input_files=[filepath]).load_data()
                db_documents += (documents)

            elif (extension == '.pdf'):
                documents = PDFReader().load_data(file=filepath)
                db_documents += (documents)

        # Datavase : Create vector database and save
        logging.info(
            '(AutoVectorDatabase) Creating vector database from %u documents...', len(db_documents))
        self.vectorDatabase = GPTVectorStoreIndex.from_documents(db_documents)
        self.vectorDatabase.storage_context.persist()

    def Query(self, text: str) -> Response:
        ''' Query database '''
        response = self.queryEngine.query(text)

        return Response(str(response), response.get_formatted_sources())


if __name__ == '__main__':
    # Database : Create
    database = AutoVectorDatabase(databasePath='database')
