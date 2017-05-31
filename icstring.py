import re


def format_text(dec, format_, label_text):
    """
    Format 'numerical text', will strip non numbers from string
    
    Parameters
    ----------         
    dec : int 
        number of decimal places for float_ and currency 
    format_ : str 
        format style
            - 'float'
            - '$' : currency
            - 'int' : integer, will drop all decimals if present
    label_text : str
        text to convert
    Returns
    -------
    Formatted text : str
    """
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
