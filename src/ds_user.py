import logging
import re
from device import device # CUSTOM
from ds_util import ds_util # CUSTOM

class ds_user():

    def package(cursor):
        user_devices = ds_util.get_device_names()

        # SELECT/READ EXAMPLE
        select_count = cursor.execute('SELECT COUNT() FROM user_input')

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
            selectRows = cursor.execute('SELECT * FROM user_input WHERE rowid BETWEEN ' + str(page_start) + ' AND ' + str(page_end))

            userRowList = []
            voiceRowList = []
            textRowList = []
            emailRowList = []

            for row in selectRows:

                # HANDLE USER
                userRowList.append((row['user'], row['user'], row['first_name'], row['last_name'], 'ACTIVE', 'Standard User', row['site'], 'Y', 'Y'))

                # HANDLE VOICE DEVICES
                if user_devices['VOICE_DEVICES']:
                    for voice_device in user_devices['VOICE_DEVICES']:
                        voice_device = voice_device.strip().lower().replace(' ', '_') # remove spaces and force to lower case
                        if row[voice_device]:
                            valid_number = device.format(row[voice_device], 'United States')
                            if valid_number:
                                voiceRowList.append((row['user'], valid_number))

                # HANDLE TEXT DEVICES
                if user_devices['TEXT_DEVICES']:
                    for text_device in user_devices['TEXT_DEVICES']:
                        text_device = text_device.strip().lower().replace(' ', '_') # remove spaces and force to lower case
                        if row[text_device]:
                            valid_number = device.format(row[text_device], 'United States')
                            if valid_number:
                                textRowList.append((row['user'], valid_number))

                # HANDLE EMAIL DEVICES
                if user_devices['EMAIL_DEVICES']:
                    for email_device in user_devices['EMAIL_DEVICES']:
                        email_device = email_device.strip().lower().replace(' ', '_') # remove spaces and force to lower case
                        if row[email_device]:
                            email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
                            if email_regex.match(row[email_device]):
                                emailRowList.append((row['user'], row[email_device]))

            # EXECUTE MANY STATEMENTS
            cursor.executemany('INSERT INTO DS_USERS(EXTERNAL_KEY, USER_ID, FIRST_NAME, LAST_NAME, STATUS, ROLE_LIST, SITE_NAME, IS_EXTERNALLY_OWNED, ACTION) VALUES(?,?,?,?,?,?,?,?,?)', userRowList)
            cursor.executemany('INSERT INTO DS_VOICE_DEVICES(EXTERNAL_KEY, PHONE_NUMBER) VALUES(?,?)', voiceRowList)
            cursor.executemany('INSERT INTO DS_TEXT_PHONE_DEVICES(EXTERNAL_KEY, TARGET_NUMBER) VALUES(?,?)', textRowList)
            cursor.executemany('INSERT INTO DS_EMAIL_DEVICES(EXTERNAL_KEY, ADDRESS) VALUES(?,?)', emailRowList)

            # increment page
            page_start = page_start + limit
            page_end = page_end + limit
