"""
**icdatetime**

Date and time functions

Functions:
----------
**day_to_int** 
    Converts a string of 'day of week' i.e. 'Mon', 'tues', etc to respective integer values, 1 is Sunday, etc.
**format_weekday**
    re-formats provided day into standard formats, full, abbreviation, int, or str(int)
"""


def day_to_int(days_to_conv):
    """
    Converts a string of 'day of week' i.e. 'Mon', 'tues', etc to respective integer values, 1 is Sunday, etc.
    
    Parameters
    ----------
    days_to_conv : list (str, int)
        list of days to convert 
    
    Returns
    -------
    Days converted to integers : list (int)
    
    Raises
    ------
    Value error if days_to_conv not a valid day of week
        ['SU', 'SUNDAY', 'SUNDAY', '1', 1], 
        ['M', 'MONDAY', 'MON', '2', 2],
        ['TU', 'TUESDAY', 'TUE', '3', 3],
        ['W', 'WEDNESDAY', 'WED', '4', 4],
        ['TH', 'THURSDAY', 'THUR', '5', 5],
        ['F', 'FRIDAY', 'FRI', '6', 6],
        ['SA', 'SATURDAY', 'SAT', '7', 7]
    """
    print(days_to_conv)
    if type(days_to_conv) is str:
        if days_to_conv.upper() in ['SU', 'SUNDAY', 'SUNDAY', '1', 1]:
            days_to_conv = [1]
        elif days_to_conv.upper() in ['M', 'MONDAY', 'MON', '2', 2]:
            days_to_conv = [2]
        elif days_to_conv.upper() in ['TU', 'TUESDAY', 'TUE', '3', 3]:
            days_to_conv = [3]
        elif days_to_conv.upper() in ['W', 'WEDNESDAY', 'WED', '4', 4]:
            days_to_conv = [4]
        elif days_to_conv.upper() in ['TH', 'THURSDAY', 'THUR', '5', 5]:
            days_to_conv = [5]
        elif days_to_conv.upper() in ['F', 'FRIDAY', 'FRI', '6', 6]:
            days_to_conv = [6]
        elif days_to_conv.upper() in ['SA', 'SATURDAY', 'SAT', '7', 7]:
            days_to_conv = [7]
        else:
            raise ValueError('{} is not a valid Day of Week'.format(days_to_conv))

    if type(days_to_conv) is list:
        for i, day in enumerate(days_to_conv):
            days_to_conv[i] = (days_to_conv[i])

    return days_to_conv


def format_weekday(day, format_='full'):
    """
    Re-formats provided day into standard formats, full, abbreviation, int, or str(int)
    
    Parameters
    ----------
    
    day : str or int
        day to convert
    format_ : str
        desired format
            - 'full' : full day spelled out
            - 'abbr' : three letter abbreviation
            - 'num' : number of day of week as string
            - 'int' : number of day of week as int
        
    Returns
    -------
    formatted weekday : str or int
    """
    if day in ['SU', 'SUNDAY', 'SUN', '1', 1]:
        if format_ == 'full':
            return 'Sunday'
        if format_ == 'abbr':
            return 'Sun'
        if format_ == 'num':
            return '1'
        if format_ == 'int':
            return 1
        raise ValueError("Invalid format: '{}'".format(format_))
    elif day in ['M', 'MONDAY', 'MON', '2', 2]:
        if format_ == 'full':
            return 'Monday'
        if format_ == 'abbr':
            return 'Mon'
        if format_ == 'num':
            return '2'
        if format_ == 'int':
            return 2
        raise ValueError("Invalid format: '{}'".format(format_))
    elif day in ['TU', 'TUESDAY', 'TUE', '3', 3]:
        if format_ == 'full':
            return 'Tuesday'
        if format_ == 'abbr':
            return 'Tue'
        if format_ == 'num':
            return '3'
        if format_ == 'int':
            return 3
        raise ValueError("Invalid format: '{}'".format(format_))
    elif day in ['W', 'WEDNESDAY', 'WED', '4', 4]:
        if format_ == 'full':
            return 'Wednesday'
        if format_ == 'abbr':
            return 'Wed'
        if format_ == 'num':
            return '4'
        if format_ == 'int':
            return 4
        raise ValueError("Invalid format: '{}'".format(format_))
    elif day in ['TH', 'THURSDAY', 'THUR', '5', 5]:
        if format_ == 'full':
            return 'Thursday'
        if format_ == 'abbr':
            return 'Thu'
        if format_ == 'num':
            return '5'
        if format_ == 'int':
            return 5
        raise ValueError("Invalid format: '{}'".format(format_))
    elif day in ['F', 'FRIDAY', 'FRI', '6', 6]:
        if format_ == 'full':
            return 'Friday'
        if format_ == 'abbr':
            return 'Fri'
        if format_ == 'num':
            return '6'
        if format_ == 'int':
            return 6
        raise ValueError("Invalid format: '{}'".format(format_))
    elif day in ['SA', 'SATURDAY', 'SAT', '7', 7]:
        if format_ == 'full':
            return 'Saturday'
        if format_ == 'abbr':
            return 'Sat'
        if format_ == 'num':
            return '7'
        if format_ == 'int':
            return 7
        raise ValueError("Invalid format: '{}'".format(format_))
    else:
        raise ValueError('{} is not a valid Day of Week'.format(day))

