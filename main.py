from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from model import predict

MY_TEXT = 'initial text '

app = FastAPI()

# pydantic models
class StockIn(BaseModel):
    text: str

class StockOut(BaseModel):  #StockIn
    forecast: list


@app.post("/predict", response_model=StockOut, status_code=200)
def get_prediction(payload: StockIn):

    my_text = MY_TEXT + payload.text
    #MY_TEXT = my_text

    prediction_list = predict(my_text)

    the_list = [{'question_index': my_text,
  'question_value': 0.22441239831115345,
  'question': 'Why is the message board chat not working for new Cisco Meeting Server deployments?',
  'model_answer_value': 0.11973859369754791,
  'model_answer': 'deployments which did not previously use chat'},
 {'question_index': 0,
  'question_value': 0.21549381887827723,
  'question': "Why can't I choose a speaker from the browsers interface for WebRTC app?",
  'model_answer_value': 0.0008141281432472169,
  'model_answer': 'To ensure reliability'},
 {'question_index': 81,
  'question_value': 0.21549381887827723,
  'question': "Why can't I choose a speaker from the browsers interface for WebRTC app?",
  'model_answer_value': 0.0008141281432472169,
  'model_answer': 'To ensure reliability'},
 {'question_index': 83,
  'question_value': 0.18900653615953697,
  'question': 'How can I improve the video and presentation quality when using the WebRTC app with the Chrome browser?',
  'model_answer_value': 0.09033406525850296,
  'model_answer': 'SeeBest practices'},
 {'question_index': 66,
  'question_value': 0.18509645657895185,
  'question': 'How is the active speaker indicated on video systems and web apps?',
  'model_answer_value': 0.21833552420139313,
  'model_answer': 'a blue line'}]

    if not prediction_list:
        raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {'text': prediction_list, 'forecast': the_list}   #, {'text': text, 'value': 2}
    return response_object
