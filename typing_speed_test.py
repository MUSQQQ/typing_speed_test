from tkinter import *
from timeit import default_timer as timer
import random
import from_file

# array for sentences from .txt file
phrases_array = from_file.read_phrases()

# 'menu' window
window = Tk()
window.geometry("1280x720")
 
x = 0
global_tries_counter = 0
global_session_average_accuracy = 0
global_session_average_time = 0
global_session_average_cps = 0  # characters per second
timer_started = False
return_clicked = True
can_return_refresh = False


def game():
    global x
    global can_return_refresh
    can_return_refresh = False
    # destroys 'menu' window
    if x == 0:
        from_file.read_phrases()
        window.destroy()
        x = x+1
 
    def check_result():
        global phrases_array
        global global_tries_counter
        global global_session_average_accuracy
        global global_session_average_time
        global global_session_average_cps
        global_tries_counter += 1
        entered_phrase = entry.get()
        smaller_length = min(len(entered_phrase), len(phrases_array[word]))
        if smaller_length == 0:
            a1 = Label(windows, text="Postaraj się jednak coś napisać", font="times 12")
            a1.place(relx=0.5, rely=0.5, anchor=CENTER)
        acc = 0
        time = timer() - game.start
        for i in range(smaller_length):
            if entered_phrase[i] == phrases_array[word][i]:
                acc+=1
        cps = len(entered_phrase)/time
        acc /= len(phrases_array[word])-1
        global_session_average_accuracy = ((global_tries_counter-1)*global_session_average_accuracy+acc)/global_tries_counter
        global_session_average_time = ((global_tries_counter-1)*global_session_average_time+time)/global_tries_counter
        global_session_average_cps = ((global_session_average_cps-1)*global_session_average_cps+cps)/global_tries_counter
        refresh_stats()
        show_current_try_stats(time, acc, cps)
 

    # random choice of phrase
    global phrases_array
    word = random.randint(0, (len(phrases_array)-1))

    # new window
    start = None
    windows = Tk()
    windows.geometry("1280x720")

    def refresh_stats(): 
        global phrases_array
        global global_tries_counter
        global global_session_average_accuracy
        global global_session_average_time
        global global_session_average_cps
        temp_global_time = round(global_session_average_time,2)
        temp_global_acc = round(global_session_average_accuracy*100, 2)
        temp_global_cps = round(global_session_average_cps, 2)
        
        # records and stats:
        a1 = Label(windows, text="Statystyki sesji", font="times 12")
        a1.place(relx=0.1, rely=0.7, anchor=CENTER)
        a2 = Label(windows, text="Liczba prób:", font="times 10")
        a2.place(relx=0.1, rely=0.75, anchor=CENTER)
        a3 = Label(windows, text=global_tries_counter, font="times 10")
        a3.place(relx=0.17, rely=0.75, anchor=CENTER)
        a4 = Label(windows, text="Średni czas:", font="times 10")
        a4.place(relx=0.1, rely=0.8, anchor=CENTER)
        a5 = Label(windows, text=str(temp_global_time)+" s", font="times 10")
        a5.place(relx=0.17, rely=0.8, anchor=CENTER)
        a6 = Label(windows, text="Średnia precyzja:", font="times 10")
        a6.place(relx=0.1, rely=0.85, anchor=CENTER)
        a7 = Label(windows, text=str(temp_global_acc)+" %", font="times 10")
        a7.place(relx=0.17, rely=0.85, anchor=CENTER)
        a8 = Label(windows, text="Średnia znaków/s:", font="times 10")
        a8.place(relx=0.1, rely=0.9, anchor=CENTER)
        a9 = Label(windows, text=str(temp_global_cps), font="times 10")
        a9.place(relx=0.17, rely=0.9, anchor=CENTER)

    refresh_stats()
    
    def show_current_try_stats(time, acc, cps):
        time = round(time, 2)
        temp_acc = round(acc*100, 2)
        cps = round(cps, 2)
        a1 = Label(windows, text="Wynik próby", font="times 12")
        a1.place(relx=0.8, rely=0.7, anchor=CENTER)
        a4 = Label(windows, text="Czas:", font="times 10")
        a4.place(relx=0.8, rely=0.75, anchor=CENTER)
        a5 = Label(windows, text=str(time)+" s", font="times 10")
        a5.place(relx=0.87, rely=0.75, anchor=CENTER)
        a6 = Label(windows, text="Precyzja:", font="times 10")
        a6.place(relx=0.8, rely=0.8, anchor=CENTER)
        a7 = Label(windows, text=str(temp_acc)+" %", font="times 10")
        a7.place(relx=0.87, rely=0.8, anchor=CENTER)
        a8 = Label(windows, text="Znaki na sekundę:", font="times 10")
        a8.place(relx=0.8, rely=0.85, anchor=CENTER)
        a9 = Label(windows, text=str(cps), font="times 10")
        a9.place(relx=0.87, rely=0.85, anchor=CENTER)
        

    def click(key):
        global timer_started
        global return_clicked
        if not timer_started:
            game.start = timer()
            timer_started = True
            return_clicked = False
            
    def click_return(Return):
        global timer_started
        global return_clicked
        global can_return_refresh
        if can_return_refresh:
            can_return_refresh = False
            reset()
            game()
        if not return_clicked:
            check_result()
            timer_started = False
            return_clicked = True
            can_return_refresh = True

 
    # labels
    x4 = Label(windows, text="Tekst do napisania:", font="times 15")
    x4.place(relx=0.5, rely=0.1, anchor=CENTER)
    x2 = Label(windows, text=phrases_array[word], font="times 15")
 
    x2.place(relx=0.5, rely=0.2, anchor=CENTER)
    x3 = Label(windows, text="Twoja odpowiedź:", font="times 15")
    x3.place(relx=0.5, rely=0.5, anchor=CENTER)
 
    entry = Entry(windows, width=200)
    entry.place(relx=0.5, rely=0.6, anchor=CENTER)
    entry.bind("<Key>", click)
    entry.bind("<Return>", click_return)
 
    b3 = Button(windows, text="Spróbuj ponownie",
                command=lambda:[reset(),game()], width=20, bg='grey')
    b3.place(relx=0.5, rely=0.8, anchor=CENTER)
        

    def reset():
        global timer_started
        timer_started = False
        windows.destroy()
    windows.mainloop()
 
 
x1 = Label(window, text="Przetestuj jak szybko piszesz", font="times 20")
x1.place(relx=0.5, rely=0.1, anchor=CENTER)
 
b1 = Button(window, text="Spróbuj", command=game, width=30, height=10, bg='grey', font="times 15")
b1.place(relx=0.5, rely=0.4, anchor=CENTER)

window.mainloop()