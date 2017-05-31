"""
**ictkinter**

**Functions:**
icon**
        returns image for use in menu icons
image_to_canvas**
        place graph image on canvas, and place canvas in subframe
create_menu**
        creates a menu from the provided dict in the provided window
create_sub_menu**
        returns sub menu to add to menu cascade
clear_subframe**
        clears and recreates subframe
populate_list_box**
        populates a list box in the GUI with the data provided

**class:**
TableFrame**
        creates a Dataframe linked to a tkinter frame
ListBoxController**
        creates a list box with specified control elements and a scroll bar
ScrollFrame**
        creates a canvas with scroll bar
CreateToolTip**
        create a tooltip for a given widget
"""

import tkinter
import os
from PIL import ImageTk, Image
import re
import numpy as np
import pandas as pd
import icstring

icons = {'bookmark': 'add_bookmark.png',
         'clear': 'clear.png',
         'fileopen': 'fileopen.png',
         'folder': 'folder.png',
         'minus': 'minus.png',
         'plus': 'plus.png',
         'theme': 'theme.png'
         }


def icon(icon_name, size=16):
    """returns image for use in menu icons

        :param icon_name:str: name of icon to retrieve in icons dict
        :param size:int: size of icon to be returned
        """
    filename = os.path.dirname(__file__) + '\\rsc\\' + icons[icon_name]
    img = Image.open(filename)
    if img.width > size:
        img = img.resize((size, size), Image.ANTIALIAS)

    return ImageTk.PhotoImage(img)


def image_to_canvas(subframe, photo, row=0, column=0, padx=2, pady=1, sticky='nsew', x1=0, y1=0, anchor='nw', canvas=None):
    """place graph image on canvas, and place canvas in subframe

        :param subframe:tkinter.Frame: frame to contain canvas(s)
        :param photo:pyimage: graph image to add to canvas
        :param row:int: grid row
        :param column:int: grid column
        :param padx:int: x padding for widget
        :param pady:int: y padding for widget
        :param sticky:str: grid sticky
        :param x1:int: x coordinate
        :param y1:int: y coordinate
        :param anchor:Str: image anchor location
        :param canvas:tkinter.Canvas: canvas to add image to, if none will create and add to subframe 
    """
    if canvas is None:
        canvas = tkinter.Canvas(subframe)
    canvas.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
    canvas.create_image(x1, y1, image=photo, anchor=anchor)

    return photo, canvas


def create_menu(window, menu_def):
    """creates a menu from the provided dict in the provided window

        :param window:tkinter.Tk: frame to contain menu
        :param menu_def:tuple: menu structure definition
        
    Menu Format:
    menu_format = (('', '', '', ''),   # Tuple of strings for top row items, for single item define as ('item',)
                                       # dict keys of items from first tuple, values are ('menu item', 'command') pairs
                                       # for single ('menu item', 'command') pair define as (('menu item', 'command'),)
                    ({'File': (('Save', '>save'), ('Export Price List', '>export'), ('Exit', self._menu_exit)),
                      'Edit': (('Undo', '>undo'), ('Redo', '>redo')),
                      'Settings': ('Theme',    # Use a string as first item in tuple to indicate a sub-menu
                                               # follow with ('menu item', 'command') pairs
                                   (('Default', '>def'), ('Flat', '>flat'), ('Dark', '>dark'))), 
                      'Help': (('VDOT Bid Tabs', '>tab'), ('About', '>about'))}))
                      
                      to add sperator: ('---', None)
    """
    # TODO - test for things like one top row item and one command pair item
    def create_sub_menu(submenu_def):
        """returns sub menu to add to menu cascade
        
            :param submenu_def:tuple: (('menu item', 'command'), () pairs, use str as first item in tuple to create
                        submenu cascade
        """
        sub_menu_ = tkinter.Menu(tearoff=0)
        for sub_menu_item in submenu_def:
            if type(sub_menu_item) is tuple:
                if sub_menu_item[0] == '---':
                    sub_menu_.add_separator()
                else:
                    try:
                        img = icon(sub_menu_item[2])
                        icon_list.append(img)
                    except IndexError:
                        img = None
                    sub_menu_.add_command(label=sub_menu_item[0], command=sub_menu_item[1], image=img,
                                          compound=tkinter.LEFT)
            else:
                sub_menu_b = create_sub_menu(submenu_def[1])
                sub_menu_.add_cascade(label=sub_menu_item, menu=sub_menu_b)
                return sub_menu_
        return sub_menu_

    icon_list = []
    top_menu = tkinter.Menu(window, tearoff=1)
    for top_menu_item in menu_def[0]:
        sub_menu = create_sub_menu(menu_def[1][top_menu_item])
        top_menu.add_cascade(label=top_menu_item, menu=sub_menu)

    window.config(menu=top_menu)


def clear_subframe(frame, subframe):
    """clears and recreates subframe

        :param frame:tkinter.Frame or LabelFrame: container for subframe
        :param subframe:tkinter.Frame or LabelFrame: containter for graphs
    """
    subframe.destroy()  # clear subframe
    subframe = tkinter.Frame(frame)
    subframe.grid(row=0, column=0, sticky='nsew')

    return subframe


def populate_list_box(listbox, data, select='keys'):
    """populates a list box in the GUI with the data provided.
    data can be of type 'dict or list'
    
        :param listbox:Tkinter.Listbox: list box to add data to
        :param data:dict or list: data to add to list box
        :param select:Str: 'keys' add dict keys - Default, 
                           'values' add dict values
    """
    if type(data) is dict and select == 'keys':
        items = sorted(data.keys())
    elif type(data) is dict and select == 'values':
        items = sorted(data.values())
    else:
        items = data

    for item in items:
        listbox.insert(tkinter.END, item)


class TableFrame(pd.DataFrame):
    """
    Create a table of tkinter.Label or tkinter.Button objects
    
    Usage notes:
        - after creating or altering the dataframe, need to call `show` to display changes in tkinter window
        - to change column data: 
            t3['Average'] = [12, 12, 12, 12, 12, 12]
                    is equivalent to
            t3.column('Average', [13, 13, 13, 13, 13, 13])
                    as self is derived from pd.DataFrame    
                    
    **METHODS:**
    
    **update** : Replaces data in table, does not alter index or column labels
        
    **hide_index** : send true to hide index column, false to show
        
    **hide_columns** : send true to hide column labels, false to show
        
    **add_label** : Adds label to subframe
        
    **show** : Display data table on subframe.
        
    **insert_row** : Inserts a row in the table at specified location
        
    **insert** : Inserts a column in the table at specified location
    
    **column_format** : Formats column in the table
    
    **header_format** : Formats the header (column titles)
    
    **index_format** : Formats the index column
    
    **row_format** : Formats row in the table
    
    **i_column** : Replaces specified column (index) with provided data
    
    **column** : Replaces specified column (label) with provided data
     
    **i_row** : Replaces specified row (index) with provided data
    
    **row** : Replaces specified row (label) with provided data
    
    **row_rename** : Rename row index  --*UNDER CONSTRUCTION*--
    
    **column_rename** : Rename column  --*UNDER CONSTRUCTION*-- 
    
    Parameters
    ----------  
    -- General parameters:             
    window : tkinter.Frame
        container for TableFrame
            
    -- Dataframe parameters:
    data : dict, list, or df
        data to be put in TableFrame
    index : list
        row labels (df index)
    column : list
        columns labels (df columns)
    orient : str
        The "orientation" of the data. If the keys of the passed dict
        should be the columns of the resulting DataFrame, pass 'columns'
        (default). Otherwise if the keys should be rows, pass 'index'.
                
    -- tkinter parameters:
    row : int
        row in window
    column : int
        column in window
    sticky : str
        tkinter.Frame resource
    columnspan : int
        columnspan in window
            
    -- formatting parameters:
    bold : tuple
        columns or rows to be bolded, 0 indexed with or without index/headers.
        Designate by: ('col0, 'col2', 'row1')
    currency : str 
        columns or rows to be formatted as currency '$0.00', 0 indexed with or without 
        index/headers.  Designate by: ('col0, 'col2', 'row1')
    float_ : str
        columns or rows to be formatted as float '0.00', 0 indexed with or without index/headers.
        Designate by: ('col0, 'col2', 'row1') # TODO be able to set precision
    int_ : str
        columns or rows to be formatted as int '0', 0 indexed with or without index/headers.
        Designate by: ('col0, 'col2', 'row1')  # TODO not working, need to code
          
                
    
    
    **=EXAMPLES===============================================================**
        print('------------------------------------------')
        print('From composite lists:')
        
        data_lst = [['00', '01', '02', '03'],
                    ['10', '11', '12', '13'],
                    ['20', '21', '22', '23'],
                    ['30', '31', '32', '33'],
                    ['40', '41', '42', '43'],
                    ['50', '51', '52', '53']]
        
        t1 = tkinter_exp.TableFrame(main, row=2, data=data_lst,
                                    index=[2014, 2013, 2012, 2011, 2010, 2009],
                                    columns=['Average', 'Min', 'Max', 'Count'])
        t1.draw_table()
        
        print('------------------------------------------')
        print('From DataFrame:')
        
        data_array = np.array([np.arange(6)]*4).T
        data_df = pd.DataFrame(data_array)
        t2 = tkinter_exp.TableFrame(main, row=3, data=data_df,
                                    index=[2014, 2013, 2012, 2011, 2010, 2009],
                                    columns=['Average', 'Min', 'Max', 'Count'])
        t2.draw_table()
        
        print('------------------------------------------')
        print('From dict:')
        
        data_dict = {2014: ['00', '01', '02', '03'],
                     2013: ['10', '11', '12', '13'],
                     2012: ['20', '21', '22', '23'],
                     2011: ['30', '31', '32', '33'],
                     2010: ['40', '41', '42', '43'],
                     2009: ['50', '51', '52', '53']}
        t3 = tkinter_exp.TableFrame(main, row=4, data=data_dict, orient='index', columns=['Average', 'Min',
                                    'Max', 'Count'])
        t3.draw_table() 
      
    **=RESULTS================================================================**
        ------------------------------------------
        From composite lists:
             Average Min Max Count
        2014      00  01  02    03
        2013      10  11  12    13
        2012      20  21  22    23
        2011      30  31  32    33
        2010      40  41  42    43
        2009      50  51  52    53
        ------------------------------------------
        From DataFrame:
              Average  Min  Max  Count
        2014        0    0    0      0
        2013        1    1    1      1
        2012        2    2    2      2
        2011        3    3    3      3
        2010        4    4    4      4
        2009        5    5    5      5
        ------------------------------------------
        From dict:
             Average Min Max Count
        2009      50  51  52    53
        2010      40  41  42    43
        2011      30  31  32    33
        2012      20  21  22    23
        2013      10  11  12    13
        2014      00  01  02    03 
    """
    def __init__(self, window, data=None, index=None, columns=None, orient='columns',
                 row=0, column=0, sticky='nsew', columnspan=1,
                 bold=None, currency=None, float_=None, int_=None, blank='--'):
        """
        creates a Dataframe linked to a tkinter frame
        """
        frame = tkinter.Frame(window)
        frame.grid(row=row, column=column, sticky=sticky, columnspan=columnspan)

        sub_frame = tkinter.Frame(frame)
        sub_frame.grid(row=0, column=0, sticky='nsew')

        if type(data) is pd.DataFrame:
            super_df = data.copy()
            if index is None:
                index = super_df.index.values
            if columns is None:
                columns = super_df.columns
            # super().__init__(data=data)
            # df.rename(columns=dict(zip(data.columns, columns)), inplace=True)
            # df.index = index
            # self.rename(columns=dict(zip(data.columns, columns)), inplace=True)
            # self.index = index
        else:
            # elif type(data) is dict:
            super_df = pd.DataFrame.from_dict(data=data, orient='index')
            super_df.rename(columns=dict(zip(super_df.columns, columns)), inplace=True)
            # self.rename(columns=dict(zip(df.columns, columns)), inplace=True)
        # else:
            # super().__init__(data=data, index=index, columns=columns)

        index, width = super_df.shape  # index x column
        default_font = ('arial', 10, 'normal')

        super_dict = {}
        for index in super_df.index.values:
            tup = ()
            for column in super_df.columns:
                tup = tup + ({'data': super_df[column][index],
                              'lbl': tkinter.Label(sub_frame, text=super_df[column][index]),
                              'font': default_font}, )
            super_dict[index] = tup
        super_df = pd.DataFrame.from_dict(super_dict, orient='index')
        super_df.columns = columns
        super().__init__(data=super_df)

        self.default_font = default_font

        self.frame = frame
        self.sub_frame = sub_frame
        self.cur_lbl = None

        self._formattting = {'index': {'font': self.default_font}, 'header': {'font': self.default_font}}

        self.visible_columns = True
        self.visible_index = True
        self.blank_cell = blank

    def update(self, other, join='left', overwrite=True, filter_func=None, raise_conflict=False):
        super().update(other, join='left', overwrite=True, filter_func=None, raise_conflict=False)

    def update_data(self, new_data):
        """
        Replaces data in table, does not alter index or column labels
        
        Parameters
        ----------
        new_data : df, dict, list
                should have same shape as existing df, not including the index and columns            
        """
        # TODO add exception for shape of new data not matching existing data frame, or trim/expand to fit
        if type(new_data) == np.ndarray:
            new_data = pd.DataFrame(new_data)
        elif type(new_data) == dict:
            new_data = pd.DataFrame.from_dict(new_data)
        elif type(new_data) == pd.DataFrame:
            pass
        else:
            return

        new_data.set_index(self.index.values, inplace=True)
        new_data.columns = self.columns
        for column in self.columns:
            self[column] = new_data[column]

    # TODO develop usage
    def hide_index(self, val=True):
        """
        Send true to hide index column, false to show
        
        Parameters
        ----------
        val : bool
        """
        self.visible_index = val

    # TODO develop usage
    def hide_columns(self, val=True):
        """
        Send true to hide column labels, false to show
                
        Parameters
        ----------
        val : bool
        """
        self.visible_columns = val

    def add_label(self, row, col, text, fontstyle='normal'):
        """
        Adds label to subframe
        
        Parameters
        ----------
        row : int
                row in subframe 
        col : int
                col in subframe
        text : str
                label text
        fontstyle : str
                label fontstyle
        """
        lbl = tkinter.Label(self.sub_frame, text=text, font=('arial', 10, fontstyle))
        lbl.grid(row=row, column=col, sticky='nsew')

        return lbl

    def show(self):
        """
        Display data table on subframe.  Must be called after table creation to display table
        """
        self.sub_frame = clear_subframe(self.frame, self.sub_frame)

        col = 0
        row = 1
        # add index to table
        if self.visible_index:
            for item in list(self.index.tolist()):
                lbl = tkinter.Label(self.sub_frame, text=item, font=self._formattting['index']['font'])
                lbl.grid(row=row, column=col, sticky='nsew')
                row += 1
            col += 1

        # add headers to table
        header_labels = list(self)
        row = 0
        if self.visible_columns:
            for col_label in header_labels:
                lbl = tkinter.Label(self.sub_frame, text=col_label, font=self._formattting['header']['font'])
                lbl.grid(row=row, column=col, sticky='nsew')
                col += 1

        col = 0 + self.visible_index
        for col_label in self.columns:
            row = 0 + self.visible_columns
            for index in self.index.values:
                self[col_label][index]['lbl'] = tkinter.Label(self.sub_frame,
                                                              text=self[col_label][index]['data'],
                                                              font=self[col_label][index]['font'])\
                    .grid(row=row, column=col, sticky='nsew')
                row += 1
            col += 1

        self.frame.update()
        # print(self)

    def insert_row(self, row, value, sort=None):
        """
        Inserts a row in the table at specified location
        
        Parameters
        ----------
        row : int
            row position to insert (zero based)
        value : list
            row values to insert
        sort : str, default=None
            sort direction after insertion
        """
        self.loc[row] = value
        if sort is not None:
            if sort.upper() in ['F', 'FORWARD', 'YES']:
                ascending = True
            elif sort.upper() in ['R', 'REVERSE', 'REVERSED', 'BACKWARDS']:
                ascending = False
            self.sort_index(inplace=True, ascending=ascending)

    def insert(self, loc, column, value, allow_duplicates=False):
        # TODO may not need, can probably just use the inherited method
        """
        Inserts a column in the table at specified location
        
        Parameters
        ----------
        loc : int 
            location to insert
        column : object
            column name
        value : int, Series, or array-like
            values to insert
        allow_duplicates : bool
        """
        super().insert(loc, column, value, allow_duplicates)
        # self.reindex()

    def column_format(self, col, format_='', dec=2, fontname=None, fontsize=None, fontstyle=None):
        """
        Formats column in the table
        
        Parameters
        ----------
        col : int
            column to be formatted
        format_ : str
            format code ('$', 'float', 'int')
        dec : int, default=2
            number of decimal places for 'float' and '$'
        fontname : str
            name of font to use
        fontsize : int
            font size
        fontstyle : str
            font style 
        """
        for index, value_dict in self[col].iteritems():
            text = icstring.format_text(dec, format_, value_dict['data'])
            value_dict['data'] = text
            font_tup = ()
            if fontname is not None:
                font_tup = font_tup + (fontname, )
            else:
                font_tup = font_tup + (value_dict['font'][0], )
            if fontsize is not None:
                font_tup = font_tup + (fontsize, )
            else:
                font_tup = font_tup + (value_dict['font'][1], )
            if fontstyle is not None:
                font_tup = font_tup + (fontstyle, )
            else:
                font_tup = font_tup + (value_dict['font'][2], )

            value_dict['font'] = font_tup

    def header_format(self, format_='', dec=2, fontname=None, fontsize=None, fontstyle=None):
        """
        Formats the header (column titles)
        
        Parameters
        ----------
        format_ : str 
            format style ('float', '$', 'int')    
        dec : int, default=2
            number of decimal places for 'float' and '$'
        fontname : str
            name of font to use
        fontsize : int
            font size
        fontstyle : str
            font style  
        
        """
        for header in self.columns:
            self.rename(columns={header: icstring.format_text(dec, format_, header)})
            font_tup = ()
            if fontname is not None:
                font_tup = font_tup + (fontname, )
            else:
                font_tup = font_tup + (self._formattting['header']['font'][0], )
            if fontsize is not None:
                font_tup = font_tup + (fontsize, )
            else:
                font_tup = font_tup + (self._formattting['header']['font'][1], )
            if fontstyle is not None:
                font_tup = font_tup + (fontstyle, )
            else:
                font_tup = font_tup + (self._formattting['header']['font'][2], )

            self._formattting['header']['font'] = font_tup

    def index_format(self, fontname=None, fontsize=None, fontstyle=None):
        """
        Formats the index column
        
        Parameters
        ----------
        fontname : str
            name of font to use
        fontsize : int
            font size
        fontstyle : str
            font style  
        """
        font_tup = ()
        if fontname is not None:
            font_tup = font_tup + (fontname, )
        else:
            font_tup = font_tup + (self._formattting['header']['font'][0], )
        if fontsize is not None:
            font_tup = font_tup + (fontsize, )
        else:
            font_tup = font_tup + (self._formattting['header']['font'][1], )
        if fontstyle is not None:
            font_tup = font_tup + (fontstyle, )
        else:
            font_tup = font_tup + (self._formattting['header']['font'][2], )

        self._formattting['index']['font'] = font_tup

    def row_format(self, row, format_='', dec=2, fontname=None, fontsize=None, fontstyle=None):
        """
        Formats row in the table
        
        Parameters
        ----------
        row : int
            row to be formatted
        format_ : str
            format code ('$', 'float', 'int')
        dec : int, default=2
            number of decimal places for 'float' and '$'
        fontname : str
            name of font to use
        fontsize : int
            font size
        fontstyle : str
            font style 
        """
        row_dict = self.loc[row]
        for value_dict in row_dict:
            text = icstring.format_text(dec, format_, value_dict['data'])
            value_dict['data'] = text
            font_tup = ()
            if fontname is not None:
                font_tup = font_tup + (fontname, )
            else:
                font_tup = font_tup + (value_dict['font'][0], )
            if fontsize is not None:
                font_tup = font_tup + (fontsize, )
            else:
                font_tup = font_tup + (value_dict['font'][1], )
            if fontstyle is not None:
                font_tup = font_tup + (fontstyle, )
            else:
                font_tup = font_tup + (value_dict['font'][2], )

            value_dict['font'] = font_tup

    def i_column(self, col, data):
        """
        Replaces specified column (index) with provided data
        
        Usage notes:
            t3['Average'] = [12, 12, 12, 12, 12, 12] is equivalent to
            t3.column('Average', [13, 13, 13, 13, 13, 13]), with exception as listed under data:
        
        Parameters
        ----------
        col : int
            column index
        data : list, series, array like
            data to replace in column, must be same length as number of rows, if data is longer then end of
            list will be truncated, if shorter blank items will be appended to end 
        """
        while len(data) > len(self):
            del data[-1]
        while len(data) < len(self):
            data.append(self.blank_cell)

        self.iloc[:, col] = data

    def column(self, col, data):
        """
        Replaces specified column (label) with provided data
        
        Usage notes:
            t3['Average'] = [12, 12, 12, 12, 12, 12] is equivalent to
            t3.column('Average', [13, 13, 13, 13, 13, 13]), with exception as listed under data:
        
        Parameters
        ----------
        col : str
            column label
        data : list, series, array like
            data to replace in column, must be same length as number of rows, if data is longer then end of
            list will be truncated, if shorter blank items will be appended to end 
        """
        while len(data) > len(self):
            del data[-1]
        while len(data) < len(self):
            data.append(self.blank_cell)

        iter_data = iter(data)
        for index, v in self.iterrows():
            v[col]['data'] = next(iter_data)

    def i_row(self, row, data):
        """
        Replaces specified row (index) with provided data
        
        Parameters
        ----------
        row : int
            row index
        data : (list, series, or array like) 
            data to replace in row, must be same length as number of columns, if data is longer then end of
            list will be truncated, if shorter blank items will be appended to end 
        """
        while len(data) > len(self.columns):
            del data[-1]
        while len(data) < len(self.columns):
            data.append(self.blank_cell)

    def row(self, row, data):
        """
        Replaces specified row (label) with provided data
        
        Parameters
        ----------
        row : int
            row index
        data : (list, series, or array like) 
            data to replace in row, must be same length as number of columns, if data is longer then end of
            list will be truncated, if shorter blank items will be appended to end 
        """
        while len(data) > len(self.columns):
            del data[-1]
        while len(data) < len(self.columns):
            data.append(self.blank_cell)

        iter_data = iter(data)
        for c, v in self.iteritems():
            v[row]['data'] = next(iter_data)

    def row_rename(self):
        """
        Rename row index  --*UNDER CONSTRUCTION*--
         
        """
        # TODO develop method
        pass

    def column_rename(self):
        """
        Rename column  --*UNDER CONSTRUCTION*--
 
        """
        # TODO develop method
        pass


class ListBoxController(tkinter.Listbox):
    """
    Creates a list box with specified control buttons and a scroll bar
        
    **METHODS:**
    
    **clear** : Clear items in list box
    
    **list_items** : Get list of items in list box
    
    **add_item** : Add item to list from linked widget
    
    **delete_item** : Delete item from list --*UNDER CONSTRUCTION*--
    
    Parameters
    ----------      
    window : tkinter.Frame
        object to contain controller
    row : int
        row in `window` to add `self.frame`
    column : int
        column in `window` to add `self.frame`
    sticky : str
        for grid
    buttons : str
        buttons to add to controller, order of string indicates order of buttons
            + = add
            - = delete
            c = clear
    duplicates : bool
        True to allow duplicates in list
    issorted : bool
        True if list to be always sorted
    widget_link : tkinter.widget
        widget providing information to add to list, must have a .get()
    """
    def __init__(self, window, row=0, column=0, sticky='nsew', buttons='+-c', duplicates=False, issorted=True,
                 widget_link=None):
        self.frame = tkinter.Frame(window)
        self.frame.grid(row=row, column=column, sticky=sticky)

        super().__init__(self.frame)
        super().grid(row=0, column=0, sticky='nsew', columnspan=4)

        self.widget_link = widget_link

        self.duplicates = duplicates
        self.issorted = issorted

        self.img_list = []
        self._create_buttons(buttons)

    def clear(self):
        """Clear items in list box"""
        self.delete(0, tkinter.END)

    def list_items(self):
        """
        Get list of items in list box
        
        Returns
        -------
        items in list box : list
        """
        return list(self.get(0, tkinter.END))

    def _create_buttons(self, but_type):
        """

        :param but_type: 
        :return: 
        """
        col = 4
        for b in reversed(but_type):
            if b == '-':
                icon_name = 'minus'
                col -= 1
                command = self.delete_item
            elif b == '+':
                icon_name = 'plus'
                col -= 1
                command = self.add_item
            elif b == 'c':
                icon_name = 'clear'
                col -= 1
                command = self.clear
            else:
                return None

            img = icon(icon_name)
            self.img_list.append(img)
            but = tkinter.Button(self.frame, command=command, image=img)
            but.grid(row=1, column=col, sticky='nsew')

    def add_item(self):
        """Add item to list from linked widget"""
        listbox_items = self.list_items()
        if not self.duplicates:
            if self.widget_link.get() not in listbox_items:
                self.insert(tkinter.END, self.widget_link.get())
                listbox_items.append(self.widget_link.get())
        else:
            self.insert(tkinter.END, self.widget_link.get())
            listbox_items.append(self.widget_link.get())

        if self.issorted:
            self.clear()
            for f in sorted(listbox_items):
                self.insert(tkinter.END, f)

    def delete_item(self):
        pass


class ScrollFrame(tkinter.Canvas):
    """ 
    Creates a canvas with scroll bar
    
    **METHODS:**
        
    **onframeconfigure** : Reset the scroll region to encompass the inner frame
    
    **scroll_frame** : Returns the frame on the canvas that is used to scroll, any widgets should be placed here
    
    Notes:
    ------
    Source : 
        http://stackoverflow.com/questions/16188420/python-tkinter-scrollbar-for-frame
    """

    def __init__(self, window):
        super().__init__(window)

        self.frame = tkinter.Frame(self)
        self.vsb = tkinter.Scrollbar(window, orient='vertical', command=self.yview)   # self.canvas.yview)

        self.grid(row=0, column=0, sticky='nsew')
        self.vsb.grid(row=0, column=1, sticky='ns')

        self.create_window((4, 4), window=self.frame, anchor='nw')

        self.frame.bind('<Configure>', lambda event, canvas=self:  self.onframeconfigure())

    def onframeconfigure(self):
        """
        Reset the scroll region to encompass the inner frame
        """
        self.configure(scrollregion=self.bbox("all"))

    def scroll_frame(self):
        """
        Returns the frame on the canvas that is used to scroll
        
        Returns
        -------
        scrolling frame : tkinter.Frame
        """
        return self.frame


class CreateToolTip(object):  # TODO not working, tooltip does not display on buttons, may only work on list boxes, etc
    """
    create a tooltip for a given widget
    link: http://stackoverflow.com/questions/3221956/what-is-the-simplest-way-to-make-tooltips-in-tkinter
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     # milliseconds
        self.wraplength = 180   # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def showtip(self, event=None):
        # x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a top level window
        self.tw = tkinter.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tkinter.Label(self.tw, text=self.text, justify='left',
                              background="#ffffff", relief='solid', borderwidth=1,
                              wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()

if __name__ == '__main__':
    main = tkinter.Tk()

    main.mainloop()
