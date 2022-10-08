
import tkinter as tk
from time import sleep
from tkinter import scrolledtext

#Creating a new window and configurations
window = tk.Tk()
window.title("Agent Assist")
#window.minsize(width=100, height=90)
window.geometry("1000x760+2300+50")

my_text = 'APN As described in Update considered harmful!!!'
# Title Label
text_received_L = tk.Label(window, 
        text = "Text Received",
        font = ("Clibri", 20))
text_received_L.grid(column = 0, pady = 2, padx = 10) 

text_received = scrolledtext.ScrolledText(window, 
                                      wrap = tk.WORD, 
                                      width = 100, 
                                      height = 10, 
                                      font = ("Times New Roman", 15))
text_received.grid(column = 0, pady = 0, padx = 0)


text_tokens_L = tk.Label(window, 
        text = "Tokens Received",
        font = ("Times New Roman", 20))
text_tokens_L.grid(column = 0, pady = 0, padx = 10)

text_tokens = scrolledtext.ScrolledText(window, 
                                      wrap =tk. WORD, 
                                      width = 100, 
                                      height = 3, 
                                      font = ("Times New Roman", 15))
text_tokens.grid(column = 0, pady = 0, padx = 10)


text_questions_L = tk.Label(window, 
        text = "FaQ candidate Question",
        font = ("Times New Roman", 20))
text_questions_L.grid(column = 0, pady = 0, padx = 10)

text_questions = scrolledtext.ScrolledText(window, 
                                      wrap = tk.WORD, 
                                      width = 100, 
                                      height = 14, 
                                      font = ("Times New Roman", 15))
text_questions.grid(column = 0, pady = 0, padx = 10)

def radio_used():
    print(radio_state.get())
    return radio_state.get()

#Variable to hold on to which radio button value is checked.
radio_state = tk.IntVar()
radiobutton1 = tk.Radiobutton(text="STOP", value=0, variable=radio_state, command=radio_used)
radiobutton2 = tk.Radiobutton(text="RUN", value=1, variable=radio_state, command=radio_used)
radiobutton1.grid(column = 0, pady = 0, padx = 10)
radiobutton2.grid(column = 0, pady = 0, padx = 10)

clear_text_bool = False
quit_session_bool = False

def clear_text():
    global clear_text_bool
    clear_text_bool = True

clear_text_button = tk.Button(window, text ="CLEAR TEXT", command = clear_text)
clear_text_button.grid(column = 0, pady = 1, padx = 10)

def quit_session():
    global quit_session_bool
    quit_session_bool = True

quit_session_button = tk.Button(window, text ="QUIT SESSION", command = quit_session)
quit_session_button.grid(column = 0, pady = 1, padx = 10)


number = 0

while number < 100:

    my_text = my_text + str(number)
    print(my_text)
    number += 1
    sleep(0.1)


    text_received.configure(state ='normal')
    text_received.delete(1.0, tk.END)
    text_received.insert(tk.INSERT, my_text)
    text_received.configure(state ='disabled')


    text_tokens.configure(state ='normal')
    text_tokens.delete(1.0, tk.END)
    text_tokens.insert(tk.INSERT, radio_used())
    text_tokens.update_idletasks()
    text_tokens.configure(state ='disabled')

    #text_area_b.configure(state ='normal')
    text_questions.insert(tk.INSERT, '''{'question_index': 0, 'question_value': 0.31715549850929403, 'question': "Why can't I choose a speaker from the browsers interface for WebRTC app?", 'model_answer_value': 0.0008141281432472169, 'model_answer': 'To ensure reliability'}

{'question_index': 81, 'question_value': 0.31715549850929403, 'question': "Why can't I choose a speaker from the browsers interface for WebRTC app?", 'model_answer_value': 0.0008141281432472169, 'model_answer': 'To ensure reliability'}

{'question_index': 83, 'question_value': 0.26775939077001903, 'question': 'How can I improve the video and presentation quality when using the WebRTC app with the Chrome browser?', 'model_answer_value': 0.09033406525850296, 'model_answer': 'SeeBest practices'}

{'question_index': 12, 'question_value': 0.24523271316568487, 'question': "I am trying to upgrade my Cisco Meeting App, but the older version of the app hasn't been completely removed?", 'model_answer_value': 0.0009241637890227139, 'model_answer': 'Windows “Pin to Taskbar'}

{'question_index': 348, 'question_value': 0.24151783221369705, 'question': 'What are the main differences between web app and WebRTC app (Cisco Meeting App for WebRTC)', 'model_answer_value': 0.00012572240666486323, 'model_answer': 'theCisco Meeting Server'}''')
    text_questions.update_idletasks()
    text_questions.configure(state ='disabled')

    if clear_text_bool:
        my_text = ''
        clear_text_bool = False

    if quit_session_bool:
        print('Bye Bye')
        break



    print('radio used: ', radio_used())

    #text.update()
    window.update()


sleep(2)
window.quit()
#window.mainloop()

