from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown


class DropDownBut(Button):

    def __init__(self, item_list=None, **kwargs):
        if item_list is None:
            item_list = ['Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item6']
        super(DropDownBut, self).__init__(**kwargs)
        self.drop_list = None
        self.drop_list = DropDown()

        for i in item_list:
            btn = Button(text=i, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn: self.drop_list.select(btn.text))

            self.drop_list.add_widget(btn)

        self.bind(on_release=self.drop_list.open)
        self.drop_list.bind(on_select=lambda instance, x: setattr(self, 'text', x))
