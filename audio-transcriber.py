import tkinter as tk
#from time import sleep
from tkinter import scrolledtext

from os import listdir, rename, remove
#from tabnanny import verbose
import pandas as pd
from ast import literal_eval
import re
from time import sleep

#from urllib import request
import requests
from collections import Counter

from utils import clean_tokenize, match_vocabulay
from sklearn.feature_extraction.text import TfidfVectorizer
import whisper


def transcribe_waves(wave_files: list, audio_path: str):

    wave_files.sort()
    print(wave_files)
    final_text = ''

    for wave_file in wave_files:
        if 'proc_' not in wave_file:

            audio = whisper.load_audio(audio_path + wave_file)
            audio = whisper.pad_or_trim(audio)

            mel = whisper.log_mel_spectrogram(audio).to(model.device)

            options = whisper.DecodingOptions(fp16=False, language='en') #, language='en'

            result = whisper.decode(model, mel, options)

            print(result.text)
            final_text = final_text + ' ' + result.text

            rename(audio_path + wave_file, audio_path + 'proc_' + wave_file)

    #print('  ')
    #print('Final Text:   ', final_text)
    return(final_text)


def update_tkinter_text():

    text_received.configure(state ='normal')
    text_received.delete(1.0, tk.END)
    text_received.insert(tk.INSERT, final_text)
    text_received.configure(state ='disabled')


    text_tokens.configure(state ='normal')
    text_tokens.delete(1.0, tk.END)
    text_tokens.insert(tk.INSERT, sentence_one)
    text_tokens.update_idletasks()
    text_tokens.configure(state ='disabled')

    text_questions.configure(state ='normal')
    text_questions.delete(1.0, tk.END)
    text_questions.insert(tk.INSERT, response_list_pretty)
    #text_questions.update_idletasks()
    text_questions.configure(state ='disabled')

    return

    
# START TKINTER MODULE 1 ---------------------------------------------------------
clear_text_bool = False
quit_session_bool = False

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

def pause_session():
    #print(radio_state.get())
    return radio_state.get()

#Variable to hold on to which radio button value is checked.
radio_state = tk.IntVar()
radiobutton1 = tk.Radiobutton(text="STOP", value=0, variable=radio_state, command=pause_session)
radiobutton2 = tk.Radiobutton(text="RUN", value=1, variable=radio_state, command=pause_session)
radiobutton1.grid(column = 0, pady = 0, padx = 10)
radiobutton2.grid(column = 0, pady = 0, padx = 10)


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

# END TKINTER MODULE 1 ---------------------------------------------------------



data_path = './data/'
audio_path = './audio/'

model_name = "tiny"  # tiny

print('model whisper ', model_name, 'is loading...')
model = whisper.load_model(model_name)
print('model loaded!!!')

stop1 = pd.read_csv(data_path + 'stop_words.csv', names=['word'])
stop_words = stop1['word'].values.tolist()

# START/START  SAME CODE AS IN SPEECH - - generate questions vocabulary
cisco_data = pd.read_csv(data_path + 'cisco_faq_cleaned.csv')

#nltk.download('stopwords')
#from nltk.corpus import stopwords
#stop_words = stopwords.words('english')


# save the original question for use with the model
cisco_data['question_original'] = cisco_data['answer_title']

cisco_data.drop_duplicates(subset=['answer_title'], inplace=True)
cisco_data = cisco_data.reset_index(drop=True)

# join the list of paragraphs in one string
cisco_data['answer_paragraphs'] = cisco_data['answer_paragraphs'].apply(literal_eval)
cisco_data['answer_paragraphs'] = cisco_data['answer_paragraphs'].apply(lambda x: ' '.join(x))
cisco_data['answer_paragraphs'] = cisco_data['answer_paragraphs'].apply(lambda x: x.replace('\xa0', ' '))

# prepare the questions for pre-process
cisco_data['answer_title'] = cisco_data['answer_title'].apply(lambda s:s.lower() if type(s) == str else s)
cisco_data['answer_title'] = cisco_data['answer_title'].apply(lambda x: re.sub('[^a-z0-9.]', ' ', x))
cisco_data['answer_title'] = cisco_data['answer_title'].apply(lambda x: ' '.join([w for w in x.split() if len(w) > 1]))

tokenized_questions = cisco_data['answer_title'].apply(lambda x: x.split(' '))
tokenized_questions = tokenized_questions.apply(lambda x:[word for word in x if not word in stop_words])

# tf-idf initializer
MAX_FEATURES = 1000
list_tokenized_questions = tokenized_questions.tolist()

outlst = [' '.join([str(c) for c in lst]) for lst in list_tokenized_questions]

tf_idf_vectorizer = TfidfVectorizer()
tf_idf_train = tf_idf_vectorizer.fit_transform(outlst)

tf_idf_array = tf_idf_train.toarray()
# END/END  SAME CODE AS IN SPEECH - - generate questions vocabulary

print('')
print('Ready to Rock!!!')
print('')
final_text = ''
sentence_one = ''
response_list = []
response_list_pretty = ''

session_running = True

while session_running:

    files = listdir(audio_path)

    # Check if session is paused, if paused delete all .wav files in audio folder
    if pause_session() == 0:
        # pyaudio-speech-recorder.py takes max 15ms to save a recording to file
        #(between open and close the file)
        # Wait 50ms before deleting
        sleep(0.05)


        for file in files:
            if '.wav' in file:
                # Delete file
                remove(audio_path + file)
                files.remove(file)

    wave_files = []
    for file in files:
        if ('.wav' in file) and ('proc_' not in file):
            wave_files.append(file)


    if len(wave_files) > 0:
        
        final_text = final_text + transcribe_waves(wave_files, audio_path)
        
        print('this is THE FINAL TEXT---->> ', final_text)

        if 'reset this session' in final_text.lower():
            final_text = ''

        if 'terminate this session' in final_text.lower():
            session_running = False

        # pre-process ALL TEXT

        #final_text = 'Hello to you. How is the weather in New York mate? speaker selection via browser was removed from webRTC app'

        tokenized_received = clean_tokenize(final_text, stop_words)
        tokenized_received = match_vocabulay(tokenized_received, tf_idf_vectorizer)

        print('ToKENS before dictionary', tokenized_received)

        # SESSION STARTS HERE
        session_dict = {}

        #   add token to current session
        for word in tokenized_received:
            if word not in session_dict:
                session_dict[word] = 1
            else:
                session_dict[word] += 1

        # create a sentence with the top 10 most frequent tokens ---- SUBJECT TO CHANGES
        # This is the sentence to be feed the tf-idf
        sentence_one = " ".join(dict(Counter(session_dict).most_common(10)))

        sentence_one = ''
        for (w, f) in Counter(tokenized_received).most_common(10):
            sentence_one += w + '(' + str(f) + ') '





        print('TOKENS from sentence_one: ', sentence_one)

        # if number of tokens greater than one -->>  SEND (CURL) SENTENCE TO FAQ_MODEL
        #headers = {'Content-Type': 'application/json'}

        if sentence_one.count(' ') > 1:
            
            try:
                r = requests.post(url='http://3.25.109.205:8000/predict', json={'text': sentence_one}, timeout=3.0)
                response_list = r.json()['forecast']

            except requests.exceptions.RequestException as e:
                sentence_one = 'Unable to connect to container. Please check if service is running'
                #raise SystemExit(e)



        else:
            response_list = []


        for question in response_list:
            print(question)
            print(' ')


        # SHOW THE RESULTS IN A BEAUTIFULL NICE WAY
        response_list_pretty = ''
        for item in response_list:
            print('')
            print(item)

            response_list_pretty += ' Question Value: ' + '%.2f' % item['question_value'] + ' Question: ' + item['question'] + '\n' \
                + ' Answer Value: ' + '%.2f' % item['model_answer_value'] + ' Answer: ' + item['model_answer'] + '\n' + '\n'


        # ------ NICE TO HAVE ------ 

        # START TKINTER MODULE 2 ---------------------------------------------------------

        update_tkinter_text()




    if clear_text_bool:
        final_text = ''
        sentence_one = ''
        response_list = []
        response_list_pretty = ''
        clear_text_bool = False
        update_tkinter_text()


    if quit_session_bool:
        print('Bye Bye')
        session_running = False



    #print('radio used: ', radio_used())

    #text.update()
    window.update()

#sleep(2)
window.quit()
#window.mainloop()
        # END TKINTER MODULE 2 -----------------------------------------------------------

        # show final text in a window
        # show tokenized words from final text
        # show sentences_candidates and their values
        # allow for an extra window to exist showing the full answer when the agent clicks on the question (by https link)

