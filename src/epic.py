import xmatters
import sqlite3
import yaml
import logging

# CUSTOM
from ds_file import ds_file
from ds_user import ds_user
from ds_site import ds_site
from ds_group import ds_group
from ds_table import ds_table

def main():
    # ---> START TIMER
    time_util = xmatters.TimeCalc()
    start = time_util.getTimeNow()
    print('Starting Process: ' + time_util.formatDateTimeNow(start))

    # prep the package
    ds_file.prepare_the_sync()

    # ---> OBTAIN CONNECTION
    connection = sqlite3.connect('db/xMatters.db')
    connection.row_factory = sqlite3.Row # This allows for referencing via column name, i.e. row['First Name']
    cursor = connection.cursor()

    # Bulk of logic here...
    ds_table.generate(cursor, connection)
    ds_site.package(cursor)
    ds_user.package(cursor)
    ds_group.package(cursor)
    ds_file.output(connection)

    # ---> COMMIT AND CLOSE CONNECTION
    connection.commit()
    connection.close()

    # ZIP up the files and end the show
    ds_file.package_the_sync()

    # print the duration
    end = time_util.getTimeNow()
    print('Process Duration: ' + time_util.getDiff(end, start))

if __name__ == "__main__":
    main()

    """
    # TODO

      Validation
        - Output bad phone numbers to a csv file
        - Output unknown Sites assigned to users to an error file and also set the users to Default Site
        - Output group supervisors who don't exist in the input to an error file (this could be tricky.....)

      Current/Previous concept of database
      - Ensure that if the database exists to do a backup and reference of some sort to do a compare

      Role Sync
      - GET People by Roles now available this will finally provide the ability to add/remove
        - https://help.xmatters.com/xmapi/index.html#get-people
        - Incorporated into the EPIC sync (not standalone) probably the best and least expensive option since it will allow updates to be done via EPIC

     Dynamic Teams solution - (Lowest priority but would be cool)
      - Figure out how to build a re-usable concept for building dynamic teams

    """
