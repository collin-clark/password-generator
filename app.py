from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

# -------------------------
# Routes
# -------------------------

@app.route("/")
def home():
    return render_template("templates/home.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json or {}
    action = data.get("action")

    # -------------------------
    # Password Generation
    # -------------------------
    if action == "password":
        try:
            howmany = int(data.get("howmanypasswords", 25))
            length = int(data.get("length", 15))
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid number or length"}), 400

        lower_chars = list('qwertyupasdfghjkkzxcvbnm')
        upper_chars = list('QWERTYUPASDFGHJKLZXCVBNM')
        special_chars = list('!@#$^&*')
        number_chars = list('23456789')
        annoying_chars = list('iI1lL0oO')

        char_pool = lower_chars.copy()
        if data.get("uppercase"):
            char_pool.extend(upper_chars)
        if data.get("special"):
            char_pool.extend(special_chars)
        if data.get("numbers"):
            char_pool.extend(number_chars)
        if data.get("annoy"):
            char_pool.extend(annoying_chars)

        passwords = [''.join(random.choices(char_pool, k=length)) for _ in range(howmany)]
        return jsonify({"passwords": passwords})

    # -------------------------
    # Passkey Generation
    # -------------------------
    elif action == "passkey":
        key_chars = list('QW2ER4TY3UP5AS6DF7GH8JKL9ZXCVBNM')
        segments = [''.join(random.choices(key_chars, k=5)) for _ in range(5)]
        passkey = '-'.join(segments)
        return jsonify({"passkey": passkey})

    return jsonify({"error": "Invalid action"}), 400


# -------------------------
# Run the app
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)

