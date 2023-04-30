import os
import openai
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__,
            template_folder='templates'
            )

def generate_colors(message):
    print(message)
    prompt = f"""You are a color palette generating assistant that responds to text prompts for color palettes.
                You should generate color palettes that fit the theme, mood, or instructions in the prompt. Palettes should
                be between 4-6 colors. No need of new lines, it can be a continuous list of colors.
                Examples:
                Q: "The Apple Logo"
                A: [#000000, #C0C0C0, #808080, #FFFFFF]
                Desired Format: a JSON array of hexadecimal color codes
                Text: {message}"""

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user",
                                                                              "content": prompt}],
                                            max_tokens=300, temperature=0.2)
    print(response.choices[0].message.content)
    try:
        list_of_colors = json.loads(response.choices[0].message.content)
        return list_of_colors
    except json.JSONDecodeError:
        print("JSONDecodeError occurred. Returning default color palette.")
        return ['#000000', '#C0C0C0', '#808080', '#FFFFFF']


@app.route('/palette', methods=["POST"])
def prompt_to_palette():
    app.logger.info("Hit Post request route")
    query = request.form.get("query")
    colors = generate_colors(query)
    app.logger.info(colors)
    return jsonify({"colors": colors})


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
