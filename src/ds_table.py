import csv
import pandas
import logging
from ds_util import ds_util # CUSTOM

class ds_table():

    def generate(cursor, connection):

        # ---> DROP TABLES
        cursor.execute("DROP TABLE IF EXISTS group_input")
        cursor.execute("DROP TABLE IF EXISTS user_input")
        cursor.execute("DROP TABLE IF EXISTS site_input")

        drop_statements = ds_util.drop_table_statements()
        for statement in drop_statements:
            cursor.execute(statement)

        # ---> RETRIEVE CSV DATA AND CREATE TABLES
        # First create the sites, underlying foundational and has no dependencies
        site_dataframe = pandas.read_csv('input/site_input.csv', dtype=ds_util.unpack_columns_to_str())
        site_dataframe.columns = site_dataframe.columns.str.strip().str.lower().str.replace(' ', '_') # convert spaces to underscores
        site_dataframe.to_sql('site_input', connection) # DROP CSV INFO INTO TABLE

        # Secondly create the users, there are dependencies to sites
        user_dataframe = pandas.read_csv('input/user_input.csv', dtype=ds_util.unpack_columns_to_str())
        user_dataframe.columns = user_dataframe.columns.str.strip().str.lower().str.replace(' ', '_') # convert spaces to underscores
        user_dataframe.to_sql('user_input', connection) # DROP CSV INFO INTO TABLE

        # Lastly create the groups, there are dependencies to users
        group_dataframe = pandas.read_csv('input/group_input.csv', dtype=ds_util.unpack_columns_to_str())
        group_dataframe.columns = group_dataframe.columns.str.strip().str.lower().str.replace(' ', '_') # convert spaces to underscores
        group_dataframe.to_sql('group_input', connection) # DROP CSV INFO INTO TABLE

        # NOW WE GO THROUGH AND CREATE ALL OF THE EPIC TABLES
        create_statements = ds_util.create_table_statements()
        for statement in create_statements:
            cursor.execute(statement)
