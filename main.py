import codecs
import tkinter as tk
from pymsgbox import *

#TODO:Переделать под SQL
#TODO:Сделать отдельный клас User



class Journal():
    def __init__(self):
        self.build_main_window()

    def build_main_window(self):
        self.main_win = tk.Tk()
        self.main_win.title("Journal")
        self.main_win.geometry("570x110")
        zap_button = tk.Button(self.main_win, text="Заполнить журнал", command=self.entry_run)
        stat_button = tk.Button(self.main_win, text="Посмотреть статистику", command=self.stat_run)
        self.stat_var = tk.IntVar()
        self.stat_opt1 = tk.Radiobutton(self.main_win, text='За месяц', variable=self.stat_var, value=1)
        self.stat_opt2 = tk.Radiobutton(self.main_win, text='За семестр', variable=self.stat_var, value=2)
        self.month = tk.Entry(self.main_win)
        self.semestr = tk.Entry(self.main_win)
        Red_button=tk.Button(self.main_win,text="Редактировать журнал",command=self.Jurn_red)
        clear_stat_but=tk.Button(self.main_win,text="Очистить журнал",command=self.clear_jur)
        month_stat=tk.Button(self.main_win,text="Посмотреть месяц подневно",command=self.all_day_in_month)

        zap_button.grid(row=0, column=0, sticky='w')
        stat_button.grid(row=2, column=0,sticky='w')
        self.stat_opt1.grid(row=2, column=1)
        self.month.grid(row=2, column=2)
        self.stat_opt2.grid(row=3, column=1)
        self.semestr.grid(row=3, column=2)
        Red_button.grid(row=4,column=1)
        clear_stat_but.grid(row=0,column=4)
        month_stat.grid(row=4,column=0)

    def entry_run(self):
        Entry_window().run()

    def all_day_in_month(self):
        dop_znach = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        month = self.month.get()
        if not month in dop_znach:
            alert(title="Error", text='Не указан или не правильно указан месяц. Укажите число от 1-12 в поле за месяц')
            return
        All_day_show(month).run()


    def clear_jur(self):
        path = "data/"
        user = 0
        month = 0

        for us in range(1, 26):
            for mon in range(1, 13):
                for day in range(1, 32):
                    with open(f"{path}{str(us)}/{str(mon)}/{str(day)}.txt", 'w') as f:
                        f.write("0")
                        f.close()

    def Jurn_red(self):
        Journal_redactor().run()

    def stat_run(self):
        mode = ''
        col = ''
        dop_znach=[]
        if self.stat_var.get() == 1:
            dop_znach=['1','2','3','4','5','6','7','8','9','10','11','12']
            mode = "mon"
            col = self.month.get()
            if not col in dop_znach:
                alert(title="Error",text='Не указан или не правильно указан месяц. Укажите число от 1-12')
                return

        elif self.stat_var.get() == 2:
            dop_znach=['1','2']
            mode = "sem"
            col = self.semestr.get()
            if not col in dop_znach:
                alert(title="Error", text='Не указан или не правильно указан семестр. Укажите число от 1-2')
                return
        else:
            alert(title="Error",text="Не выбрана опция. Выберете За месяц или За семестр и укажите номер месяца или семестра")
            return
        Stat_window(mode, col).run()

    def run(self):
        self.main_win.mainloop()


class Entry_window():
    def __init__(self):
        self.entry_wimdow = tk.Tk()
        self.entry_wimdow.title("Заполнить журнал")
        self.entry_wimdow.geometry("500x240")
        self.user_list_box = tk.Listbox(self.entry_wimdow, selectmode=tk.EXTENDED)
        self.proguls_options_list = tk.Listbox(self.entry_wimdow, selectmode=tk.EXTENDED)
        user_list = []
        with codecs.open("data\\users.txt", 'r', 'utf_8_sig') as f:
            for user in f:
                user_list.append(user)
        #print(user_list)
        # for user in range(1,26):
        #     user_list.append(str(user))
        proguls_list = ["Прогул", 'Заболел', 'Уважительная']
        for i in proguls_list:
            self.proguls_options_list.insert(tk.END, i)
        for i in user_list:
            self.user_list_box.insert(tk.END, i)
        self.proguls = tk.Entry(self.entry_wimdow)
        Update_button = tk.Button(self.entry_wimdow, text='Отметить', command=self.Send_stat)
        self.day = tk.Entry(self.entry_wimdow)
        self.mounth = tk.Entry(self.entry_wimdow)
        list_lab = tk.Label(self.entry_wimdow, text="Список")
        prog_lab = tk.Label(self.entry_wimdow, text="Прогулы")
        prog_opt_lab = tk.Label(self.entry_wimdow, text="Причина прогула")
        day_lab = tk.Label(self.entry_wimdow, text="День")
        month_lab = tk.Label(self.entry_wimdow, text="Месяц")

        list_lab.grid(row=0, column=0);
        prog_lab.grid(row=0, column=1);
        prog_opt_lab.grid(row=0, column=2)
        self.user_list_box.grid(row=1, column=0)
        self.proguls.grid(row=1, column=1, sticky='n')
        self.proguls_options_list.grid(row=1, column=2)
        Update_button.grid(row=1, column=3, sticky="ns")
        day_lab.grid(row=2, column=0);
        month_lab.grid(row=2, column=1)
        self.day.grid(row=3, column=0)
        self.mounth.grid(row=3, column=1)

    def Send_stat(self):
        date = {"day": self.day.get(), "month": self.mounth.get()}
        user=''
        if self.user_list_box.get('active')[1]=="_":
            user = self.user_list_box.get('active')[0]
        else:
            user = self.user_list_box.get('active')[0:2]
            print(user)
        # print(user)
        prog_col = self.proguls.get()
        prog_opt = self.proguls_options_list.get("active")
        path = f"data\\{user}\\{date['month']}\\{date['day']}.txt"
        file_data = f"{prog_col},{prog_opt}"
        # print(file_data)
        with open(path, 'w') as f:
            f.write(file_data)
            f.close()

    def run(self):
        self.entry_wimdow.mainloop()


class Stat_window():
    def __init__(self, mode, col):
        self.mode = mode
        self.col = col
        self.stat_window = tk.Tk()
        self.stat_window.title("Статистика")
        self.stat_window.geometry("550x250")
        self.user_list_box = tk.Listbox(self.stat_window, selectmode=tk.EXTENDED)
        self.user_list_box.bind('<Button-1>', self.show_stat)
        user_list = []
        with codecs.open("data\\users.txt", 'r', 'utf_8_sig') as f:
            for user in f:
                user_list.append(user)
        for i in user_list:
            self.user_list_box.insert(tk.END, i)
        self.prog_lab = tk.Label(self.stat_window, text="Пргулы")
        self.uv_lab = tk.Label(self.stat_window, text="По уважительной")
        self.all_lab = tk.Label(self.stat_window, text="Всего")
        self.prog_col = tk.Entry(self.stat_window)
        self.uv_col = tk.Entry(self.stat_window)
        self.all_col = tk.Entry(self.stat_window)

        self.user_list_box.grid(row=0, column=0)
        self.prog_lab.grid(row=0, column=1, sticky='s')
        self.uv_lab.grid(row=0, column=2, sticky='s')
        self.all_lab.grid(row=0, column=3, sticky='s')
        self.prog_col.grid(row=1, column=1, sticky='n')
        self.uv_col.grid(row=1, column=2, sticky='n')
        self.all_col.grid(row=1, column=3, sticky='n')

    def show_stat(self, events):
        self.prog_col.delete(0, tk.END)
        self.uv_col.delete(0, tk.END)
        self.all_col.delete(0, tk.END)
        user_id=''
        if self.user_list_box.get('active')[1]=="_":
            user_id = self.user_list_box.get('active')[0]
        else:
            user_id = self.user_list_box.get('active')[0:2]
        if self.mode == "mon":
            month = self.col
            progul = 0
            uvag = 0
            all = 0
            path = f'data\\{user_id}\\{month}\\'
            for day in range(1, 32):
                with open(f'{path}{str(day)}.txt') as f:
                    file_data = []
                    file_data_str = f.read()
                    file_data = file_data_str.split(sep=',')
                    try:
                        if file_data[1] == "Прогул":
                            try:
                                progul += int(file_data[0])
                            except:
                                progul += 0
                        elif file_data[1] == "Заболел" or file_data[1] == "Уважительная":
                            try:
                                uvag += int(file_data[0])
                            except:
                                uvag += 0
                    except:
                        pass
            all = progul + uvag
            self.prog_col.insert(0, str(progul))
            self.uv_col.insert(0, str(uvag))
            self.all_col.insert(0, str(all))


        elif self.mode == "sem":
            ran = []
            progul = 0
            uvag = 0
            all = 0
            if self.col == "1":
                ran = [1, 7]
            elif self.col == "2":
                ran = [6, 13]
            path = f"data\\{user_id}\\"
            for month in range(ran[0], ran[1]):
                for day in range(1, 32):
                    with open(f'{path}{str(month)}\\{str(day)}.txt') as f:
                        file_data = []
                        file_data_str = f.read()
                        file_data = file_data_str.split(sep=',')
                        try:
                            if file_data[1] == "Прогул":
                                try:
                                    progul += int(file_data[0])
                                except:
                                    progul += 0
                            elif file_data[1] == "Заболел" or file_data[1] == "Уважительная":
                                try:
                                    uvag += int(file_data[0])
                                except:
                                    uvag += 0
                            else:
                                try:
                                    progul += int(file_data[0])
                                except:
                                    progul += 0
                        except:
                            pass
            all = progul + uvag
            self.prog_col.insert(0, str(progul))
            self.uv_col.insert(0, str(uvag))
            self.all_col.insert(0, str(all))

    def run(self):
        self.stat_window.mainloop()

class Journal_redactor():
    def __init__(self):
        self.entry_wimdow = tk.Tk()
        self.entry_wimdow.title("Заполнить журнал")
        self.entry_wimdow.geometry("500x240")
        self.user_list_box = tk.Listbox(self.entry_wimdow, selectmode=tk.EXTENDED)
        self.proguls_options_list = tk.Listbox(self.entry_wimdow, selectmode=tk.EXTENDED)
        user_list = []
        with codecs.open("data\\users.txt", 'r', 'utf_8_sig') as f:
            for user in f:
                user_list.append(user)
        #print(user_list)
        # for user in range(1,26):
        #     user_list.append(str(user))
        proguls_list = ['Заболел', 'Уважительная']
        for i in proguls_list:
            self.proguls_options_list.insert(tk.END, i)
        for i in user_list:
            self.user_list_box.insert(tk.END, i)
        #self.proguls = tk.Entry(self.entry_wimdow)
        Update_button = tk.Button(self.entry_wimdow, text='Исправить', command=self.Send_stat)
        self.day = tk.Entry(self.entry_wimdow)
        self.mounth = tk.Entry(self.entry_wimdow)
        list_lab = tk.Label(self.entry_wimdow, text="Список")
        #prog_lab = tk.Label(self.entry_wimdow, text="Часы")
        prog_opt_lab = tk.Label(self.entry_wimdow, text="Заменить прогул на")
        day_lab = tk.Label(self.entry_wimdow, text="День")
        month_lab = tk.Label(self.entry_wimdow, text="Месяц")

        list_lab.grid(row=0, column=0);
        #prog_lab.grid(row=0, column=1);
        prog_opt_lab.grid(row=0, column=2)
        self.user_list_box.grid(row=1, column=0)
        #self.proguls.grid(row=1, column=1, sticky='n')
        self.proguls_options_list.grid(row=1, column=2)
        Update_button.grid(row=1, column=3, sticky="ns")
        day_lab.grid(row=2, column=0);
        month_lab.grid(row=2, column=1)
        self.day.grid(row=3, column=0)
        self.mounth.grid(row=3, column=1)

    def Send_stat(self):
        date = {"day": self.day.get(), "month": self.mounth.get()}
        user =''
        if self.user_list_box.get('active')[1]=="_":
            user = self.user_list_box.get('active')[0]
        else:
            user = self.user_list_box.get('active')[0:2]
        prog_col =0
        prog_opt = self.proguls_options_list.get("active")
        path = f"data\\{user}\\{date['month']}\\{date['day']}.txt"
        with open(path,'r') as f:
            user_data=f.read()
            f.close()
        user_data_arr=user_data.split(sep=",")
        user_data_arr[1]=prog_opt
        file_data = f"{user_data_arr[0]},{user_data_arr[1]}"
        # print(file_data)
        with open(path, 'w') as f:
            f.write(file_data)
            f.close()

    def run(self):
        self.entry_wimdow.mainloop()

class All_day_show():
    def __init__(self,month):
        self.month=month
        self.main_win=tk.Tk()
        self.main_win.title("Просмотр месяца")
        self.main_win.geometry("500x500")
        self.user_list_box = tk.Listbox(self.main_win, selectmode=tk.EXTENDED)
        self.user_list_box.bind("<Button-1>",self.fill)
        user_list = []
        with codecs.open("data\\users.txt", 'r', 'utf_8_sig') as f:
            for user in f:
                user_list.append(user)

        for i in user_list:
            self.user_list_box.insert(tk.END, i)

        days_lab=[]
        for day in range(1,32):
            days_lab.append(tk.Label(self.main_win,text=str(day),bg="yellow",font="arial 14"))


        self.days=[]
        for day in range(1,32):
            self.days.append(tk.Label(self.main_win,font="arial 14"))

        self.user_list_box.grid(row=0,column=0)
        counter=0
        counter1=0
        for i in range(2,9):
            for k in range(10):
                if not i%2==0:
                    try:
                        self.days[counter].grid(row=i,column=k)
                    except:
                        break
                    else:
                        counter += 1
                else:
                    try:
                        days_lab[counter1].grid(row=i,column=k)
                    except:
                        break
                    else:
                        counter1+=1




    def fill(self,event):
        user_id = ''
        if self.user_list_box.get('active')[1]=="_":
            user_id = self.user_list_box.get('active')[0]
        else:
            user_id = self.user_list_box.get('active')[0:2]
        path=f'data/{user_id}/{self.month}/'
        file_data=""
        file_data_arr=[]
        proguls_list=[]
        for day in range(1,32):
            with open(f"{path}{str(day)}.txt",'r') as f:
                file_data=f.read()
                file_data_arr=file_data.split(sep=",")
                proguls_list.append(file_data_arr[0])
                f.close()

        counter=0
        for i in self.days:
            i['text']=proguls_list[counter]
            counter+=1

    def run(self):
        self.main_win.mainloop()


if __name__ == '__main__':
    Journal().run()
