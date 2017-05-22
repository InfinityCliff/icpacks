import re


def format_text(dec, format_, label_text):
    non_decimal = re.compile(r'[^\d.]+')
    text = non_decimal.sub('', str(label_text))
    if text != '':
        if 'float' in format_:
            fc = '{0:.' + str(dec) + 'f}'
            return fc.format(float(text))
        if '$' in format_:
            fc = '${0:.' + str(dec) + 'f}'
            return fc.format(float(text))
        if 'int' in format_:
            return int(float(text))

    return label_text
