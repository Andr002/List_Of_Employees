import tkinter as tk         #Импорт необходимых библиотек и методов
from tkinter import ttk
import sqlite3


#Класс главного окна

class Main(tk.Frame):
    def __init__ (self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):                  #Метод, который отвечает за хранение и инизиализацию графических элементов
        toolbar = tk.Frame(bg = '#d7d8e0', bd = 2)
        toolbar.pack(side = tk.TOP, fill = tk.X)
        self.add_img = tk.PhotoImage(file = './img/add.png')
        btn_open_dialog = tk.Button(toolbar, bg = '#d7d8e0', bd = 0, image = self.add_img,  #Кнопка, которая вызывает метод open_dialog
                                    command = self.open_dialog)
        btn_open_dialog.pack(side = tk.LEFT)

        self.tree = ttk.Treeview(self, columns = ('ID', 'name', 'tel', 'email', 'pay'), height = 45,  #Создание таблицы
                                 show = 'headings')
        self.tree.column('ID', width = 30, anchor = tk.CENTER)
        self.tree.column('name', width = 300, anchor = tk.CENTER)
        self.tree.column('tel', width = 150, anchor = tk.CENTER)                  #Создание колонок
        self.tree.column('email', width = 150, anchor = tk.CENTER)
        self.tree.column('pay', width = 150, anchor = tk.CENTER)

        self.tree.heading('ID', text = 'ID')
        self.tree.heading('name', text = 'ФИО')
        self.tree.heading('tel', text = 'Телефон')         #Даем колонкам читаемые названия
        self.tree.heading('email', text = 'Почта')
        self.tree.heading('pay', text = 'Зарплата')

        self.tree.pack(side = tk.LEFT) #Отображение таблицы

        self.update_img = tk.PhotoImage(file = './img/update.png')

        btn_edit_dialog = tk.Button(toolbar, bg = '#d7d8e0', bd = 0, image = self.update_img, #Кнопка, которая вызывает метод open_update_dialog
                                    command = self.open_update_dialog)
        btn_edit_dialog.pack(side = tk.LEFT)

        self.delete_img = tk.PhotoImage(file = './img/delete.png')
        btn_delete = tk.Button(toolbar, bg = '#d7d8e0', bd = 0, image = self.delete_img, #Кнопка, которая вызывает метод delete_record
                               command = self.delete_record)
        btn_delete.pack(side = tk.LEFT)

        self.searcg_img = tk.PhotoImage(file = './img/search.png')
        btn_search = tk.Button(toolbar, bg = '#d7d8e0', bd = 0, image = self.searcg_img, #Кнопка, которая вызывает метод open_search_dialog
                               command = self.open_search_dialog)
        btn_search.pack(side = tk.LEFT)

        self.refresh_img = tk.PhotoImage(file = './img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg = '#d7d8e0', bd = 0, image = self.refresh_img, #Кнопка, которая вызывает метод view_records
                               command = self.view_records)
        btn_refresh.pack(side = tk.LEFT)



    def open_dialog(self):  #Метод, который открывает дочернее окно с добавлением сотрудника
        Child()

    def records(self, name, tel, email, pay): #Метод добавления данных в бд
        self.db.insert_data(name, tel, email, pay) #Вызывается дочерний метод и в него передаются данные
        self.view_records()

    def view_records(self): #Метод вывода данных из бд на главное окно
        self.db.cursor.execute('SELECT * FROM db')

        [self.tree.delete(i) for i in self.tree.get_children()]

        [self.tree.insert('', 'end', values = row) for row in self.db.cursor.fetchall()]

    def open_update_dialog(self): #Метод, который открывает дочернее окно с редактированием сотрудника
        Update()

    def update_record(self, name, tel, email, pay): #Метод редоктирования данных в бд
        self.db.cursor.execute('''UPDATE db 
                               SET name = ?, tel = ?, email = ?, pay = ? WHERE ID = ?''',
                               (name, tel, email, pay, self.tree.set(self.tree.selection() [0], '#1'),))
        self.db.connect.commit()
        self.view_records()

    def delete_record(self): #Метод удаления данных из бд
        for selection_item in self.tree.selection():
            self.db.cursor.execute('DELETE FROM db WHERE id = ?', (self.tree.set(selection_item,'#1'),))
        self.db.connect.commit()
        self.view_records()

    def open_search_dialog(self): #Метод, который открывает дочернее окно с поиском сотрудника
        Search()

    def search_record(self, name): #Метод поиска данных по имени в бд
        name = ('%' + name + '%',)
        self.db.cursor.execute('SELECT * FROM db WHERE name LIKE ?', (name))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values = row) for row in self.db.cursor.fetchall()]
        

        

#Дочерний класс окна с добавлением данных

class Child(tk.Toplevel):
    def __init__ (self):
        super().__init__(root)
        self.init_child()
        self.view = app
                                           #Окно с добавлением сотрудника
    def init_child(self):
        self.title('Добавить сотрудника') 
        self.geometry('400x240')
        self.resizable(False, False)
        self.grab_set()
        self.focus_get()

        #Создание формы добавления сотрудников

        label_name = tk.Label(self, text = 'ФИО')
        label_name.place(x = 50, y = 20)

        label_number = tk.Label(self, text = 'Телефон')
        label_number.place(x = 50, y = 70)
                                                            #Создание текста
        label_email = tk.Label(self, text = 'Почта')
        label_email.place(x = 50, y = 120)

        label_pay = tk.Label(self, text = 'Зарплата, p.')
        label_pay.place(x = 50, y = 170)



        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x = 200, y = 15)

        self.entry_numder = ttk.Entry(self)
        self.entry_numder.place(x = 200, y = 65)            #Создание поля ввода

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x = 200, y = 115)

        self.entry_pay = ttk.Entry(self)
        self.entry_pay.place(x = 200, y = 165)



        self.btn_cancel = ttk.Button(self, text = 'Закрыть', 
                                     command = self.destroy)
        self.btn_cancel.place(x = 300, y = 200)
                                                                        #Создание кнопок для добавления сотрудника и закрытия дочернего окна
        self.btn_ok = ttk.Button(self, text = 'Добавить')
        self.btn_ok.place(x = 210, y = 200)

        self.btn_ok.bind('<Button-1>', lambda event:
                         self.view.records(self.entry_name.get(),
                                           self.entry_numder.get(),
                                           self.entry_email.get(),
                                           self.entry_pay.get()))


#Дочерний класс редактирования
class Update(Child):
    def __init__(self):
        super().__init__()
        self.db = db
        self.view = app
        self.init_update()
        self.default_data()

    def init_update(self): #Окно и кнопка редактирования
        self.title('Редактировать контакт')
        btn_edit = tk.Button(self, text = 'Редактировать')
        btn_edit.place(x = 200, y = 200) 
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_record(self.entry_name.get(),
                                              self.entry_numder.get(),
                                              self.entry_email.get(),
                                              self.entry_pay.get()))
        btn_edit.bind('<Button-1>', lambda event:
                      self.destroy(), add = '+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.cursor.execute('SELECT * FROM db WHERE ID = ?', (self.view.tree.set(self.view.tree.selection() [0], '#1')))
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_numder.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_pay.insert(0, row[4])


#Дочерний класс поиска данных
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск контакта')
        self.geometry('300x200')
        self.resizable(False, False)

        label_search = tk.Label(self, text = 'Имя')
        label_search.place(x = 50, y = 20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x = 105, y = 20, width = 150)   #Дочернее окно и кнопки на окне

        btn_cancel = ttk.Button(self, text = 'Закрыть', command = self.destroy)
        btn_cancel.place(x = 185, y = 50)

        btn_search = ttk.Button(self, text = 'Найти')
        btn_search.place(x = 105, y = 50)
        btn_search.bind('<Button-1>', lambda event:
                        self.view.search_record(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event:
                        self.destroy(), add = '+')




#Класс базы данных
class DB:
    def __init__(self):             #Создание базы данных
        self.connect = sqlite3.connect('db.db')
        self.cursor = self.connect.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS db(
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            tel TEXT,
                            email TEXT,
                            pay INTEGER
        );
        ''')
        self.connect.commit()

    def insert_data(self, name, tel, email, pay):
        self.cursor.execute(
            'INSERT INTO db (name, tel, email, pay) VALUES (?, ?, ?, ?)', (name, tel, email, pay) #Дочерний метод добавления данных в бд
        )
        self.connect.commit()



if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников')               #Главное окно
    root.geometry('815x650')
    root.resizable(False, False)
    root.mainloop()
