



list_dict = [{'question_index': 4, 'question_value': 0.2895298291908634, 'question': 'Why can the other participants not hear me when my microphone is active?', 'model_answer_value': 0.08778625726699829, 'model_answer': 'it is not sent from the server to other participants'},
  {'question_index': 101, 'question_value': 0.2518312311877714, 'question': 'Troubleshooting Web Bridge 2 connectivity issues', 'model_answer_value': 0.028694363310933113, 'model_answer': 'SSL certificate'}, 
  {'question_index': 106, 'question_value': 0.22777058977063025, 'question': 'Can I use the same certificate on two Meeting Server services?', 'model_answer_value': 0.00034752729698084295, 'model_answer': 'While it is possible to use the same certificates on two services'}]


text = ''

#print(list_dict)

for item in list_dict:
    print('')
    print(item)

    text += ' Question Value: ' + '%.2f' % item['question_value'] + ' Question: ' + item['question'] + '\n' \
        + ' Answer Value: ' + '%.2f' % item['model_answer_value'] + ' Answer: ' + item['model_answer'] + '\n' + '\n'

print('')
print(text)





'''
from time import sleep

num = 0

while 1 :
    print('process ONE ', num, ' seconds')
    num += 2
    sleep(2)
'''