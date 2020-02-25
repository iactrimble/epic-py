import logging

class ds_group():

    def package(cursor):

        # SELECT/READ EXAMPLE
        select_count = cursor.execute('SELECT COUNT() FROM group_input')

        # get the count
        total = 0
        for row in select_count:
            total = row['COUNT()']

        # now let's paginate through this
        limit = 1000
        page_start = 1 # the first row starts at 1, not zero
        page_end = limit # initial page end is based on the limit

        while page_start <= total:

            # do our initial query....
            selectRows = cursor.execute('SELECT * FROM group_input WHERE rowid BETWEEN ' + str(page_start) + ' AND ' + str(page_end))
            groupRowList = []

            for row in selectRows:
                groupRowList.append((row['group_name'], row['group_name'], row['group_description'], 'ACTIVE', 'Y', 'US/EASTERN', 'DEFAULT SITE', 'Y', '', 'epic', 'N', 'Y', 'Y'))

            # EXECUTE MANY STATEMENTS
            cursor.executemany('INSERT INTO DS_GROUPS(EXTERNAL_KEY, GROUP_NAME, DESCRIPTION, STATUS, USE_DEFAULT_DEVICES, TIMEZONE, GROUP_SITE_NAME, OBSERVED_BY_ALL, OBSERVER_LIST, SUPERVISOR_LIST, ALLOW_DUPLICATES, IS_EXTERNALLY_OWNED, ACTION) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)', groupRowList)

            # increment page
            page_start = page_start + limit
            page_end = page_end + limit
