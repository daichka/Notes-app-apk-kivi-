from ast import literal_eval
from kivy.app import App
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from kivy.core.window import Window


class firstwindow(Screen):
    def on_enter(self):
        self.label = Label(text='Заметки')
        self.buttonsandnotes = {}
        try:
            self.bd = eval('{' + open('bdnotes.txt').read().split('{')[1:][0])
            print(self.bd)
        except:
            self.bd = {'': ''}
            open('bdnotes.txt', 'w').write("{}")
        self.relativel = ScrollView()
        self.boxlayoutbuttons = BoxLayout(orientation='vertical',size_hint=[1,1], padding=10)
        self.createnote = Button(text='Create new note',size_hint_y=None, on_press=self.createnotepress)
        self.boxlayoutbuttons.add_widget(self.createnote)
        for key, value in self.bd.items():
            if key != '':
                self.buttons = Button(text=str(key),size_hint_y=None, on_press=self.notepress)
                self.buttonsandnotes[self.buttons] = {key: value}
                self.boxlayoutbuttons.add_widget(self.buttons)
        self.boxlayout0 = BoxLayout(orientation='vertical')
        self.labelboxlayout = BoxLayout(size_hint=[0.25, 0.05])
        self.labelboxlayout.add_widget(self.label)
        self.boxlayout0.add_widget(self.labelboxlayout)
        self.relativel.add_widget(self.boxlayoutbuttons)
        self.boxlayout0.add_widget(self.relativel)
        self.add_widget(self.boxlayout0)

    def on_leave(self):  # Будет вызвана в момент закрытия экрана

        self.boxlayout0.clear_widgets()  # очищаем список

    def createnotepress(self, widget, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'note'

    def notepress(self, widget, *args):

        l = open('bdnotes.txt').read().split('{')[1:]
        l = '{' + l[0]
        z = l + str(self.buttonsandnotes[widget])
        q = open('bdnotes.txt', 'w')
        q.write(z)
        q.close()
        self.manager.transition.direction = 'right'
        self.manager.current = 'note'


class secondwindow(Screen):
    def on_enter(self):
        self.l = open('bdnotes.txt').read().split('{')[1:]
        self.bd = '{' + self.l[0]
        self.bd = eval(self.bd)
        print(self.l)
        self.key = ''
        if len(self.l) > 1:
            for key, value in eval('{' + self.l[1]).items():
                self.key = key
                self.titlestr = key
                self.notestr = value
                file = open('bdnotes.txt', 'w')
                file.write('{' + self.l[0])
                file.close()
        else:
            self.titlestr = ''
            self.notestr = ''
        self.title = ''
        self.note = ''
        boxlayoutv = BoxLayout(orientation='vertical')
        boxlayouth= BoxLayout(orientation='horizontal',size_hint=[1,0.4])
        bututtrefactor = Button(text='Refactor')
        buttcancel = Button(text='Cancel')
        boxlayoutv.add_widget(Label(text='You have note, with this title!'))
        boxlayouth.add_widget(buttcancel)
        boxlayouth.add_widget(bututtrefactor)
        boxlayoutv.add_widget(boxlayouth)
        self.popup = Popup(title='Error',content=boxlayoutv,size_hint=[0.35,0.35], auto_dismiss=True)
        buttcancel.bind(on_press=self.popup.dismiss)
        bututtrefactor.bind(on_press=self.refactorsave)
        self.boxlayout = BoxLayout(orientation='vertical')
        self.gridlayout = GridLayout(cols=3, size_hint=[1, 0.06])
        self.backbutton = Button(text='Back', size_hint=[0.25, 1])
        self.savebutton = Button(text='Save', size_hint=[0.3, 1])
        self.titleinput = TextInput(hint_text='Title', multiline=False)
        self.noteinput = TextInput(hint_text='note', multiline=True)
        self.titleinput.bind(text=self.texttitle)
        self.noteinput.bind(text=self.textnote)
        self.backbutton.bind(on_press=self.backbuttonfunc)

        if len(self.l) > 1:
            print(self.notestr)
            self.titleinput.text = self.titlestr
            self.noteinput.text = self.notestr
            self.savebutton.bind(on_press=self.savebuttonfunc)
        else:
            self.savebutton.bind(on_press=self.savebuttonfunc)
        self.gridlayout.add_widget(self.backbutton)
        self.gridlayout.add_widget(self.titleinput)
        self.gridlayout.add_widget(self.savebutton)
        self.boxlayout.add_widget(self.gridlayout)
        self.boxlayout.add_widget(self.noteinput)

        self.add_widget(self.boxlayout)

    def on_leave(self):  # Будет вызвана в момент закрытия экрана

        self.boxlayout.clear_widgets()  # очищаем список

    def backbuttonfunc(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'notes'
        self.title = ''
        self.note = ''
        self.titleinput.text = ''
        self.noteinput.text = ''

    def savebuttonfunc(self, value, *args):
        if self.key != '':
            arr = list(self.bd)
            arr.remove(self.key)
            titles = arr
        else:
            titles = list(self.bd)
        print(titles)
        title = False
        for i in titles:
            print(i,'\n'+self.title)
            if self.title != '' and self.title == i:
                title = True

        print(title)

        if title == False:
            if self.key != '':
                del self.bd[self.key]
                self.bd[self.title] = self.note
            else:
                bd = dict(reversed(list(self.bd.items())))
                bd[self.title] = self.note
                self.bd = dict(reversed(list(bd.items())))
            file = open('bdnotes.txt', 'w')
            file.write(str(self.bd))
            file.close()
            self.title = ''
            self.note = ''
            self.titleinput.text = ''
            self.noteinput.text = ''
            self.manager.transition.direction = 'left'
            self.manager.current = 'notes'
        else:
            self.popup.open()
    def refactorsave(self,x):
        self.popup.dismiss()
        bd = dict(reversed(list(self.bd.items())))
        bd[self.title] = self.note
        self.bd = dict(reversed(list(bd.items())))

        file = open('bdnotes.txt', 'w')
        file.write(str(self.bd))
        file.close()
        self.title = ''
        self.note = ''
        self.titleinput.text = ''
        self.noteinput.text = ''
        self.manager.transition.direction = 'left'
        self.manager.current = 'notes'
    def texttitle(self, instance, value):
        self.title = str(value)

    def textnote(self, instance, value):
        self.note = str(value)


class notesApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(firstwindow(name='notes'))
        sm.add_widget(secondwindow(name='note'))
        return sm


if __name__ == '__main__':
    notesApp().run()'
            self.manager.transition.direction = 'left'
            self.manager.current = 'notes'
        else:
            self.popup.open()
    def refactorsave(self,x):
        self.popup.dismiss()
        bd = dict(reversed(list(self.bd.items())))
        bd[self.title] = self.note
        self.bd = dict(reversed(list(bd.items())))

        file = open('bdnotes.txt', 'w')
        file.write(str(self.bd))
        file.close()
        self.title = ''
        self.note = ''
        self.titleinput.text = ''
        self.noteinput.text = ''
        self.manager.transition.direction = 'left'
        self.manager.current = 'notes'
    def texttitle(self, instance, value):
        self.title = str(value)

    def textnote(self, instance, value):
        self.note = str(value)


class notesApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(firstwindow(name='notes'))
 
