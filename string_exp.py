import re


def format_text(dec, format_, label_text):
    if 'float' in format_:
        fc = '{0:.' + str(dec) + 'f}'
        return fc.format(float(label_text))
    if '$' in format_:
        non_decimal = re.compile(r'[^\d.]+')  # regex to strip off non number info
        text = non_decimal.sub('', label_text)
        fc = '${0:.' + str(dec) + 'f}'
        return fc.format(float(text))
    if 'int' in format_:
        # noinspection
        non_decimal = re.compile(r'[^\d.]+')  # regex to strip off non number info
        text = non_decimal.sub('', label_text)
        return int(text)

    return label_text
