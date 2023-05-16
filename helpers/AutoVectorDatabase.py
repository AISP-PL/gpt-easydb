'''
    Class creates automatically vector database from texts 
    in given directory.
'''
from dataclasses import field
import logging
import sys
import os
from llama_index import (
    GPTSimpleVectorIndex,
    GPTSimpleKeywordTableIndex,
    GPTListIndex,
    SimpleDirectoryReader
)

@dataclass
class AutoVectorDatabase:
    ''' 
        Class creates automatically vector database from texts 
        in given directory.
    '''
    # Database directory
    database: str = field(init=True, default="database/")
    # Acceptable file extensions
    extensions: list = field(init=True, default=[".txt", ".pdf"])
    # List of all acceptable files found in database directory
    files: list = field(init=False, repr=False, default_factory=list)

    def __post_init__(self):
        ''' 
            Initialize class.
        '''
        if (not os.path.exists(self.database)):
            raise Exception("Database directory does not exist.")

        # Database : Process all files in database directory
        self.ProcessPathFiles(self.database)

        # Database : Check every file embeddings exists

    
    def ProcessPathFiles(self, path: str):
        ''' Process all files in given path. '''
        # Files : Scann all files and directories in database directory
        for path in os.listdir(path):
            # File : Check if path is file
            if (os.path.isfile(os.path.join(self.database, path))):
                # Extension : Is Acceptable?
                if (os.path.splitext(path)[1] in self.extensions):
                    self.files.append(path)

            # Directory : Recursion
            elif (os.path.isdir(os.path.join(self.database, path))):
                self.ProcessPathFiles(os.path.join(self.database, path))
    
    def ProcessFilesEmbeddings(self):
        ''' Process all files embeddings. '''
        for filepath in self.files:
            embedingspath = os.path.splitext(filepath)[0]+".json"
            # File : Check if embeddings exists
            if (not os.path.exists(embedingspath)):
                # File : Create embeddings
                db_documents = SimpleDirectoryReader(datasetpath).load_data()
                db_index = GPTSimpleVectorIndex.from_documents(db_documents)
                db_index.save_to_disk(f"{datasetpath}.json")

                
    

