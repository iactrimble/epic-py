import logging

class ds_site():

    def package(cursor):

        # SELECT/READ EXAMPLE
        select_count = cursor.execute('SELECT COUNT() FROM site_input')

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
            selectRows = cursor.execute('SELECT * FROM site_input WHERE rowid BETWEEN ' + str(page_start) + ' AND ' + str(page_end))
            siteRowList = []

            for row in selectRows:
                # HANDLE SITE
                siteRowList.append((row['site_name'], row['site_name'], 'ACTIVE', 'ENGLISH', 'SITE_TIMEZONE', row['address_1'], row['address_2'], row['city'], row['region'], row['country'], row['mail_code'], 'Y', 'Y'))

            # EXECUTE MANY STATEMENTS
            cursor.executemany('INSERT INTO DS_SITES(EXTERNAL_KEY, SITENAME, SITE_STATUS, SITE_LANGUAGE, SITE_TIMEZONE, SITE_ADDRESS_01, SITE_ADDRESS_02, SITE_CITY, SITE_COUNTRY, SITE_REGION_NAME, SITE_MAIL_CODE, IS_EXTERNALLY_OWNED, ACTION) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)', siteRowList)

            # increment page
            page_start = page_start + limit
            page_end = page_end + limit
