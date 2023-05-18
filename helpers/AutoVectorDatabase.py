'''
    Class creates automatically vector database from texts
    in given directory.
'''
from dataclasses import field, dataclass
import logging
import os
from helpers.json import jsonRead, jsonWrite
from helpers.Response import Response
from typing import Any
from llama_index import (
    GPTVectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    download_loader
)


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
    # Dict of all acceptable files found in database directory
    files: dict = field(init=False, repr=False, default_factory=list)
    # Is database modified?
    isModified: bool = field(init=False, repr=False, default=False)

    def __post_init__(self):
        '''
            Initialize class.
        '''
        if (not os.path.exists(self.databasePath)):
            raise Exception('Database directory does not exist.')

        # Database : Load database
        self.Load()

        # Files : Get all files in directory
        newFiles = self.ProcessPathFiles(self.databasePath)

        # Check : If files are modified
        if (set(newFiles.keys()) != set(self.files.keys())):
            self.isModified = True

        # Database : If not exists then create.
        if (self.vectorDatabase is None):
            self.Create(files=newFiles)
        # Database : If modified then update.
        elif (self.isModified):
            self.Update(newFiles=newFiles)


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

    @property
    def docs_count(self) -> int:
        ''' Get documents count. '''
        if (self.vectorDatabase is None):
            return 0

        return len(self.vectorDatabase.docstore.docs)

    def ProcessPathFiles(self, path: str):
        ''' Process all files in given path. '''
        # Dict of processed files
        files = {}

        # Files : Scann all files and directories in database directory
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            # File : Check if path is file
            if (os.path.isfile(filepath)):
                # Extension : Is Acceptable?
                if (os.path.splitext(filename)[1] in self.extensions):
                    files[filepath] = None

            # Directory : Recursion
            elif (os.path.isdir(filepath)):
                filesRecursed = self.ProcessPathFiles(filepath)
                files = { **files, **filesRecursed}

        return files

        

    def FileToDocuments(self, filepath: str) -> str:
        ''' Convert file to document. '''
        # Documents : List of file documents
        documents = []
        # File : Get extension
        extension = os.path.splitext(filepath)[1]

        if (extension == '.txt'):
            documents = SimpleDirectoryReader(
                input_files=[filepath]).load_data()

        elif (extension == '.pdf'):
            documents = PDFReader().load_data(file=filepath)

        return documents

    def Create(self, files:dict):
        ''' Create vector database from found files. '''
        # Documents : Create documents list
        db_documents = []

        # Files : Convert files to documents
        for filepath in files:
            # File : To documents and update doc_id
            fileDocs = self.FileToDocuments(filepath)
            files[filepath] = fileDocs[0].doc_id

            # Documents : Add to list
            db_documents += fileDocs

        # Datavase : Create vector database and save
        logging.info(
            '(AutoVectorDatabase) Creating vector database from %u documents...', len(db_documents))
        self.vectorDatabase = GPTVectorStoreIndex.from_documents(db_documents)
        self.files = files
        
        # Database : Save
        self.Save()

    def Update(self, newFiles:list):
        ''' Update vector database from found files. '''
        logging.info('(AutoVectorDatabase) Database was modified. Updating!')

        # Files : Remove deleted files
        for filepath in self.files.copy():
            if (filepath not in newFiles):
                # Files : Get filepath existing doc_id
                doc_id = self.files[filepath]
                # Files : Remove document from database
                self.vectorDatabase.delete(doc_id)
                del self.files[filepath]


        # Files : Insert new files
        new_documents = []
        for filepath in newFiles:
            if (filepath not in self.files):
                # File : To documents and update doc_id
                fileDocs = self.FileToDocuments(filepath)
                self.files[filepath] = fileDocs[0].doc_id

                new_documents += fileDocs

        if (len(new_documents) > 0):
            self.vectorDatabase.refresh(new_documents)
            logging.info('(AutoVectorDatabase) Updated %u new documents.', len(new_documents))

        # Database : Save
        self.Save()

    def Load(self):
        ''' Load current database. '''
        # Files : Read previous files list
        self.files = {}
        if (os.path.exists(self.filesFilepath)):
            self.files = jsonRead(self.filesFilepath)

        # Database : Load previous database/storage version json.
        try:
            storage = StorageContext.from_defaults(persist_dir='storage')
            self.vectorDatabase = load_index_from_storage(storage)
        except ValueError:
            logging.warning(
                '(AutoVectorDatabase) Previous database version not found.')
            pass
        

    def Save(self):
        ''' Save current database. '''
        if (self.vectorDatabase is None):
            return 

        # Database : Save
        self.vectorDatabase.storage_context.persist()
        # Files : Save 
        jsonWrite(self.filesFilepath, self.files)

        # ModifiedFlag : Reset
        self.isModified = False

    def Query(self, text: str) -> Response:
        ''' Query database '''
        response = self.queryEngine.query(text)

        return Response(str(response), response.get_formatted_sources())


if __name__ == '__main__':
    # Database : Create
    database = AutoVectorDatabase(databasePath='database')
