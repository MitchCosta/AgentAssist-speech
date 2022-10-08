from tkinter import *

from os import listdir, rename
#from tabnanny import verbose
import pandas as pd
from ast import literal_eval
import re

#from urllib import request
import requests
from collections import Counter

from utils import clean_tokenize, match_vocabulay
from sklearn.feature_extraction.text import TfidfVectorizer
import whisper

'''
st.set_page_config(layout="wide")
st.title('Text Received')
'''

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


data_path = './data/'
audio_path = './audio/'

model_name = "tiny"

print('model whisper ', model_name, 'is loading...')
model = whisper.load_model(model_name)
print('model loaded!!!')

stop1 = pd.read_csv(data_path + 'stop_words.csv', names=['word'])
stop_words = stop1['word'].values.tolist()

#print(stop_words)

# START/START  SAME CODE AS IN SPEECH - - generate questions vocabulary
cisco_data = pd.read_csv(data_path + 'cisco_faq_cleaned.csv')

#nltk.download('stopwords')
#from nltk.corpus import stopwords
#stop_words = stopwords.words('english')


# save the original question for use with the model
cisco_data['question_original'] = cisco_data['answer_title']

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

session_running = True

while session_running:

    files = listdir(audio_path)
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

        print('TOKENS from sentence_one: ', sentence_one)

        # SEND (CURL) SENTENCE TO FAQ_MODEL
        headers = {'Content-Type': 'application/json'}

        r = requests.post(url='http://0.0.0.0:8000/predict', json={'text': sentence_one})

        response_list = r.json()['forecast']


        for question in response_list:
            print(question)
            print(' ')


        # SHOW THE RESULTS IN A BEAUTIFULL NICE WAY

        # ------ NICE TO HAVE ------ 


        '''
        logtxtbox = st.empty()
        logtxt = 'start'
        logtxtbox.text_area("Logging: ",final_text, height = 500)
        '''



        # show final text in a window
        # show tokenized words from final text
        # show sentences_candidates and their values
        # allow for an extra window to exist showing the full answer when the agent clicks on the question (by https link)

