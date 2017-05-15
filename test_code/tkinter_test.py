import tkinter
import tkinter_exp
import numpy as np
import pandas as pd
import time

main = tkinter.Tk()

ent = tkinter.Entry(main)
ent.grid(row=0, column=0, sticky='nsew')
# lbl = tkinter.Label(main)
# lbl.grid(row=0, column=0, sticky='nsew')
# lbl['text'] = 'test'
# lbl['font'] = ('arial', 24, 'bold')


print('------------------------------------------')
print('From dict:')


data_dict = {2014: ['00', '01', '02', '03'],
             2013: ['10', '11', '12', '13'],
             2012: ['20', '21', '22', '23'],
             2011: ['30', '31', '32', '33'],
             2010: ['40', '41', '42', '43'],
             2009: ['50.0', '51.0', '52.0', '53.0']}

table = tkinter_exp.TableFrame(main, row=4, data=data_dict, orient='index', columns=['Average', 'Min', 'Max', 'Count'])
table['Average'] = [12, 12, 12, 12, 12, 12]


# table.column_format('Average', 'float')
# table.column_format('Min', '$')
# table.column_format('Max', 'int')
table.draw_table()
# table.row_format(2014, 'float')
table.column_format('Min', fontstyle='bold', format_='float')
table.draw_table()

#table.row_format(2009, fontstyle='bold', format_='$')
#table.draw_table()
#table.header_format(fontstyle='bold', fontsize=16)
#table.draw_table()

for r in table._formattting.items():
    print(r)
print()
for r, v in table._label_dict_from_df().items():
    print(r, v)

main.mainloop()

