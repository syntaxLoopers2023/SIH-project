from flask import Flask, request, render_template, redirect, send_from_directory
import openai
import geeta
from flask.helpers import url_for
from flask.templating import render_template_string
from flask import Blueprint

import os

my_secret = os.environ['openAI_APIKey']

openai.api_key = my_secret
quote = geeta.random_quote

server = Flask(__name__)
server.config['STATIC_FOLDER'] = 'static'
static_bp = Blueprint('static',
                      __name__,
                      static_url_path='/static',
                      static_folder='static')
server.register_blueprint(static_bp)

messages = []

initiate_txt = "You are an ai bot named Garbage Bot made by Team Syntax Loopers, I will send Item names as promts you will give 3 ways how to recycle it. You are not able to do other things except this. Tell it is inappropriate if the promt is inappropriate.if the prompt is not a garbage then Respond accordingly as the prompt. \nNow recycle this:\n"


def send_gpt(prompt):
  try:
    response = openai.Completion.create(engine="text-davinci-003",
                                        prompt=initiate_txt + "\n" + prompt +
                                        "\nNOW ANSWER THE ABOVE PART.",
                                        max_tokens=300)

    return response

  except:
    return "Developer is lazy to resolve bugs... Comeback Later"


@server.route('/', methods=['GET', 'POST'])
def get_request_json():
  if request.method == 'POST':
    if len(request.form['question']) < 1:
      return render_template(
        'chat3.5.html',
        question=
        "I have nothing to recycle. Lend me some of your quotes regarding waste recycling",
        res=quote)
    question = request.form['question']
    print("======================================")
    print("Receive the question:", question)
    resp = send_gpt(question)
    res = resp["choices"][0]['text']
    n = res.find("\n") + 1
    res = res[n:]
    print("Q：\n", question)
    print("A：\n", resp)
    print("tokens used: ", tokens)

    return render_template('chat3.5.html', question=question, res=str(res))
  return render_template('chat3.5.html', question=0)


if __name__ == '__main__':
  server.run(debug=True, host='0.0.0.0', port=1025)
