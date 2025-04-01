from flask import Flask, render_template, request, redirect, jsonify
import google.generativeai as genai
import ollama

key = "ENTER YOUR API KEY HERE"
app = Flask(__name__)

genai.configure(api_key=key)

model = genai.GenerativeModel('gemini-1.5-flash')

google = model.start_chat(history = [])

@app.route("/", methods = ["GET","POST"])
def main():
    global google
    google = model.start_chat(history = [])
    return render_template("index.html")

@app.route("/ochat",methods = ["POST"])
def ochat():
    data = request.json
    ret = {}
    ret['prompt'] = data['prompt']
    ai_model=data['model']
    # reply = google.send_message(data['prompt'])
    response = ollama.chat(
        model=f'{ai_model}',
        messages=[
            {"role": "user", "content": data['prompt']},
            ],
        )
    ret['resp'] = response["message"]["content"]
    
    return jsonify(ret)

@app.route("/chat",methods = ["POST"])
def chat():
    
    data = request.json
    reply = google.send_message(data['prompt'])
    ret = {}
    ret['prompt'] = data['prompt']
    ret['resp'] = reply.text
    return jsonify(ret)

if __name__ == "__main__" :
    app.run(debug=True)