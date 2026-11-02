from flask import Flask, request, render_template
from flask_cors import CORS
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model_name = os.getenv("LAB_CHATBOT_MODEL_NAME",default="facebook/blenderbot-400M-distill")

# Load model (download on first run and reference local installation for subsequent runs)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
conversation_history =[]

app = Flask(__name__)
CORS(app)

  return response

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')
    
# @app.route('/')
# def home():
#     return 'Hello, World!'

@app.route('/bananas')
def bananas():
    return 'This page has bananas!'
	
@app.route('/bread')
def bread():
    return 'This page has bread!'

@app.route("/chatbot", methods=["POST"])
def handle_prompt():
  data = request.get_json()
  conversation_history = conversation_history[-6:]
  history_string = "\n".join(conversation_history)

  if not isinstance(data, dict) or not "prompt" in data:
    return ({"message":"Invalid input"},400)

  if not isinstance(data["prompt"], string) or data["prompt"].strip() == "":
    return ({"message":"Invalid input"},422)

  input_text = data["prompt"]

  prompt = history_string + f"\nUser: {input_text}\nBot:"

  inputs = tokenizer(
      prompt,
      return_tensors="pt",
      truncation=True,
      max_length=512
  )
  outputs = model.generate(
      **inputs,
      max_new_tokens=60,
      no_repeat_ngram_size=3,
      repetition_penalty=1.3,
      do_sample=True,
      temperature=0.6,
      top_p=0.85
  )
  ## Remove this print statement after testing
  #print(outputs)
  response = tokenizer.decode(
      outputs[0],
      skip_special_tokens=True
  ).strip()

  conversation_history.append(f"User: {input_text}")
  conversation_history.append(f"Bot: {response}")

if __name__ == '__main__':
    app.run()
