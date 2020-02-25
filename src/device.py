# https://github.com/google/libphonenumber
# https://pypi.org/project/pycountry/
import phonenumbers
import pycountry
import logging

class device():

    # first let's see if the number is valid E.164 format
    def is_valid_e164_number(number):
        valid = True
        try:
            phone_number = phonenumbers.parse(number, None) # this means +1 (plus and country code included)
            # logging.debug("National Number: " + str(phone_number.national_number) + " Country Code: " + str(phone_number.country_code))
            valid = phonenumbers.is_valid_number(phone_number)
            # logging.debug("Is Valid Number: " + str(valid))
        except Exception as e:
            # logging.debug('Exception occured while attempting to validate: ' + str(e))
            valid = False
        return valid

    # takes in a non E.164 formatted number and attempts to assign country code
    def assign_country_to_number(number, country_name):
        new_number = None
        try:
            country = pycountry.countries.get(name=country_name)
            # logging.debug("Retrieved Country Info: " + str(country))
            new_number = phonenumbers.parse(number, country.alpha_2)
            # logging.debug("Parse phone number with country : " + str(new_number))
            valid = phonenumbers.is_valid_number(new_number)
            # logging.debug('After parsing, new number is it valid?: ' + str(valid))
            if valid:
                new_number = phonenumbers.format_number(new_number, phonenumbers.PhoneNumberFormat.E164)
                # logging.debug('New number is valid!')
        except Exception as e:
            # logging.debug('Exception occured while attempting to parse: ' + str(e))
            new_number = None
        return new_number

    # MAIN Handler
    def format(number, country_name):
        formatted_number = None
        try:
            # CONSIDER IMPLEMENTING SELF ???
            valid = device.is_valid_e164_number(number)
            if valid:
                formatted_number = number
            else:
                new_number = device.assign_country_to_number(number, country_name)
                if new_number:
                    # logging.debug('We have a formatted number! ' + str(new_number))
                    formatted_number = new_number

        except Exception as e:
            # logging.debug('Exception occured while attempting to parse: ' + str(e))
            formatted_number = None

        return formatted_number
