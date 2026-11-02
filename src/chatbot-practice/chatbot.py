import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = os.getenv("LAB_CHATBOT_MODEL_NAME",default="facebook/blenderbot-400M-distill")

# Load model (download on first run and reference local installation for subsequent runs)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

conversation_history = []

print("Chatbot ready! (type 'exit' to quit)\n")
input_text = None
while True:
    conversation_history = conversation_history[-6:]
    history_string = "\n".join(conversation_history)

    input_text = input("> ")

    if input_text == "exit":
        break

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
    print("Bot:",response)

    conversation_history.append(f"User: {input_text}")
    conversation_history.append(f"Bot: {response}")

