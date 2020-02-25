import yaml
import logging

class ds_util:

    def create_table_statements():
        config = yaml.load(open('config/table.yaml'), Loader=yaml.FullLoader)
        create_statements = []
        for table_name in config:
            columns = []
            for field in config[table_name]:
                columns.append(field +' '+ config[table_name][field])
            create_statements.append("CREATE TABLE " + table_name + "("+', '.join(columns)+")")
        return create_statements

    def drop_table_statements():
        config = yaml.load(open('config/table.yaml'), Loader=yaml.FullLoader)
        drop_statements = []
        for table_name in config:
            drop_statements.append("DROP TABLE IF EXISTS " + table_name)
        return drop_statements

    def get_table_names():
        config = yaml.load(open('config/table.yaml'), Loader=yaml.FullLoader)
        table_names = []
        for table_name in config:
            table_names.append(table_name)
        return table_names

    def get_device_names():
        config = yaml.load(open('config/user.yaml'), Loader=yaml.FullLoader)
        data = {}
        if config['VOICE_DEVICES']:
            data['VOICE_DEVICES'] = []
            for value in config['VOICE_DEVICES']:
                data['VOICE_DEVICES'].append(value)

        if config['TEXT_DEVICES']:
            data['TEXT_DEVICES'] = []
            for value in config['TEXT_DEVICES']:
                data['TEXT_DEVICES'].append(value)

        if config['EMAIL_DEVICES']:
            data['EMAIL_DEVICES'] = []
            for value in config['EMAIL_DEVICES']:
                data['EMAIL_DEVICES'].append(value)

        return data

    def unpack_columns_to_str():
        config = yaml.load(open('config/user.yaml'), Loader=yaml.FullLoader)
        data = {}
        if config['USERS']:
            for value in config['USERS']:
                data[config['USERS'][value]] = str

        if config['EMAIL_DEVICES']:
            for value in config['EMAIL_DEVICES']:
                data[value] = str

        if config['VOICE_DEVICES']:
            for value in config['VOICE_DEVICES']:
                data[value] = str

        if config['TEXT_DEVICES']:
            for value in config['TEXT_DEVICES']:
                data[value] = str

        if config['CUSTOM_FIELDS']:
            for value in config['CUSTOM_FIELDS']:
                data[value] = str

        if config['CUSTOM_ATTRIBUTES']:
            for value in config['CUSTOM_ATTRIBUTES']:
                data[value] = str

        return data
