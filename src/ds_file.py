import os
import zipfile
import shutil
import logging
import pandas
import csv
from ds_util import ds_util

class ds_file():

    def prepare_the_sync():

        # create the db directory
        if not os.path.exists('db/'):
            os.makedirs('db/')

        # create the output directory
        if not os.path.exists('output/'):
            os.makedirs('output/')

        # ---> First check to see if we need to execute a backup
        if os.path.exists('output/ETLZipSync.zip'):

            # ---> If previous sync file, let's create a backup
            newpath = 'output/backup/'
            if not os.path.exists(newpath):
                os.makedirs(newpath)

            # ---> If there's a previous backup, let's delete it
            backup = 'output/backup/ETLZipSync.zip'
            if os.path.exists(backup):
                os.remove(backup)

            # ---> Since there was a previous sync file, let's move it to the backup location
            for root, directories, files in os.walk('output/'):
                for filename in files:
                    if filename == 'ETLZipSync.zip':
                        filepath = os.path.join(root, filename)
                        if filepath != 'output/backup/ETLZipSync.zip':
                            shutil.move(filepath, 'output/backup/ETLZipSync.zip')

    def package_the_sync():

        # ---> Copy the manifest file:
        # https://stackabuse.com/how-to-copy-a-file-in-python/
        for root, directories, files in os.walk('config/'):
            for filename in files:
                if filename == 'manifest.xml':
                    filepath = os.path.join(root, filename)
                    shutil.copy(filepath, 'output/manifest.xml')

        # https://stackoverflow.com/questions/42055873/zip-only-contents-of-directory-exclude-parent-python
        zipf = zipfile.ZipFile('output/ETLZipSync.zip', 'w', zipfile.ZIP_DEFLATED)
        file_paths = []
        for root, directories, files in os.walk('output/'):
            for filename in files:
                if filename[:3] == "DS_" or filename == 'manifest.xml':
                    zipf.write(os.path.join(root, filename), filename)

        # ---> DELETE ALL FILES THAT BEGIN WITH DS_
        for root, directories, files in os.walk('output/'):
            for filename in files:
                # join the two strings in order to form the full filepath and only add if they begin with DS_
                if filename[:3] == "DS_" or filename == 'manifest.xml':
                    os.remove('output/'+filename)

    def output(connection):
            # ---> OUTPUT TO CSV
            table_names = ds_util.get_table_names()
            for table_name in table_names:
                dataframe = pandas.read_sql_query('SELECT * FROM ' + table_name, connection)
                dataframe.to_csv('output/'+table_name+'.csv', quoting=csv.QUOTE_ALL)
