from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
# import csv
import main_fail

def rgb_hack(rgb):
    return "#%02x%02x%02x" % rgb
#main_color = rgb_hack((198, 232,238))
main_color = rgb_hack((218, 232, 252))

class Login():

    def __init__(self):
        self.root = Tk()
        #self.root.geometry("300x150")
        self.root.geometry('600x400')
        self.root.title("Приложение для выгрузки данных из СПАРК")
        self.root.config(bg=main_color)
        self.root.resizable(False, False)

        self.heading = Label(self.root, text="Введите данные для входа в систему СПАРК", bg=main_color)
        self.heading.pack()

        self.username = Label(self.root, text="Логин", bg=main_color)
        self.username.pack()

        self.username_entry = Entry(self.root, width=30)
        self.username_entry.pack()

        self.password = Label(self.root, text="Пароль", bg=main_color)
        self.password.pack()

        self.password_entry = Entry(self.root, width=30, show="*")
        self.password_entry.pack()

        self.login_button = Button(self.root, text="Войти", command=self.login)
        self.login_button.pack(pady=10)

        self.root.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            self.root.destroy()
            SearchApp(username, password)
        else:
            messagebox.showerror("Вход", "Ошибка входа. Проверьте логин и пароль.")


class FileSearchTab():

    def __init__(self, parent, login, password):
        self.parent = parent
        self.login = login
        self.password = password

        self.file_label = Label(self.parent, text="Выберите файл формата CSV / XLS / XLSX", bg=main_color)
        self.file_label.pack()

        self.file_label_errors = Label(self.parent,
                                       text="Вы также можете выбрать файл errors.txt, находящийся в одной папке с программой",
                                       bg=main_color)
        self.file_label_errors.pack()

        self.file_button = Button(self.parent, text="Выбор файла", command=self.get_file)
        self.file_button.pack(pady=10)

        self.column_label = Label(self.parent, text="Укажите название столбца", bg=main_color)
        self.column_label.pack()

        self.column_entry = Entry(self.parent, width=30)
        self.column_entry.pack()

        self.result_file_label = Label(self.parent, text="Укажите название файла, для вывода информации(используйте английский язык)", bg=main_color)
        self.result_file_label.pack()

        self.result_file_entry = Entry(self.parent, width=30)
        self.result_file_entry.pack()

        self.search_button = Button(self.parent, text="Поиск", command=self.search)
        self.search_button.pack(pady=10)

    def get_file(self):
        self.filename = filedialog.askopenfilename(initialdir="/",
                                                   title="Выберите файл",
                                                   filetypes=(("Excel files", "*.xls*"),
                                                              ("CSV files", "*.csv"),
                                                              ("Text files", "*.txt*")))
        self.file_label.config(text="Выбран файл: " + self.filename)

    def search(self):
        column_name = self.column_entry.get()
        result_file_name = self.result_file_entry.get()
        if not column_name:
            messagebox.showerror("Ошибка", "Введите название столбца")
            return
        if not result_file_name:
            messagebox.showerror("Ошибка", "Введите название файла")
            return
        if not self.filename:
            messagebox.showerror("Ошибка", "Выберите файл")
            return
        try:
            # передаем путь к файлу и имя столбца в функцию main в файле main.py
            main_fail.main(self.filename, column_name, self.login, self.password, self.result_file_entry)
            messagebox.showinfo("Поиск", "Поиск выполнен")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка открытия файла: {e}")

class CompanySearchTab():

    def __init__(self, parent, login, password):
        self.parent = parent
        self.login = login
        self.password = password

        self.company_label = Label(self.parent, text="Введите название компании", bg=main_color)
        self.company_label.pack()

        self.company_entry = Entry(self.parent, width=30)
        self.company_entry.pack()

        self.result_file_label = Label(self.parent, text="Укажите название файла, для вывода информации(используйте английский язык)", bg=main_color)
        self.result_file_label.pack()

        self.result_file_entry = Entry(self.parent, width=30)
        self.result_file_entry.pack()

        self.search_button = Button(self.parent, text="Поиск", command=self.search)
        self.search_button.pack(pady=10)

    def search(self):
        company = self.company_entry.get()
        result_file_name = self.result_file_entry.get()
        if not company:
            messagebox.showerror("Ошибка", "Введите название компании")
            return
        if not result_file_name:
            messagebox.showerror("Ошибка", "Введите название файла")
            return
        # передаем название компании в функцию main в файле main.py
        main_fail.main(company, self.login, self.password, self.result_file_entry)
        messagebox.showinfo("Поиск", "Поиск выполнен")

class SearchApp():

    def __init__(self, login, password):
        self.root = Tk()
        # self.root.geometry("400x300")
        self.root.geometry('600x400')
        self.root.title("Приложение для выгрузки данных из СПАРК")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background=main_color)

        self.notebook = ttk.Notebook(self.root)

        self.tab1 = ttk.Frame(self.notebook, style="BW.TLabel")
        self.file_search_tab = FileSearchTab(self.tab1, login, password)
        self.notebook.add(self.tab1, text="Загрузка через фаил")

        self.tab2 = ttk.Frame(self.notebook, style="BW.TLabel")
        self.company_search_tab = CompanySearchTab(self.tab2, login, password)
        self.notebook.add(self.tab2, text="Ручной ввод")

        self.notebook.pack(expand=True, fill=BOTH)

        self.root.mainloop()


if __name__ == "__main__":
    Login()