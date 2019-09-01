import modules.config as config


def translate_values(row):
    for i in range(len(config.item_numbers)):
        # get the dict corresponding to the item_number if existing
        item_number = config.form_dict.get(config.item_numbers[i], None)
        if item_number is not None:
            field_value = row[i]
            # get the translation of the field_value from the dict
            translation = item_number.get(field_value, None)
            if translation is not None:
                # set the translation
                row[i] = translation
            else:
                row[i] = "UNDEFINED (Original Value: {})".format(field_value)
        else:
            # stop the function as it's either there's a misconfiguration in the files,
            # or the next loops will just do nothing
            break

    return row
