from flask import Flask, request, render_template
import secrets

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.form
    action = data.get("action")

    context = {
        "form": data  # remember last selections
    }

    # -------------------------
    # PASSWORD GENERATION
    # -------------------------
    if action == "password":
        try:
            count = int(data.get("howmanypasswords", 25))
            length = int(data.get("length", 15))
        except (ValueError, TypeError):
            context["error"] = "Invalid count or length"
            return render_template("home.html", **context)

        lower_chars = list("qwertyupasdfghjkkzxcvbnm")
        upper_chars = list("QWERTYUPASDFGHJKLZXCVBNM")
        number_chars = list("23456789")
        special_chars = list("!@#$^&*")
        annoying_chars = list("iI1lL0oO")

        char_pool = []
        required_chars = []

        if data.get("lowercase"):
            char_pool.extend(lower_chars)
            required_chars.append(secrets.choice(lower_chars))

        if data.get("uppercase"):
            char_pool.extend(upper_chars)
            required_chars.append(secrets.choice(upper_chars))

        if data.get("numbers"):
            char_pool.extend(number_chars)
            required_chars.append(secrets.choice(number_chars))

        if data.get("special"):
            char_pool.extend(special_chars)
            required_chars.append(secrets.choice(special_chars))

        if data.get("annoy"):
            char_pool.extend(annoying_chars)
            required_chars.append(secrets.choice(annoying_chars))

        if not char_pool:
            context["error"] = "Select at least one character set"
            return render_template("home.html", **context)

        if length < len(required_chars):
            context["error"] = "Length too short for selected character sets"
            return render_template("home.html", **context)

        results = []

        for _ in range(count):
            chars = required_chars.copy()
            chars.extend(secrets.choice(char_pool) for _ in range(length - len(chars)))
            secrets.SystemRandom().shuffle(chars)
            results.append("".join(chars))

        context.update({
            "result": "\n".join(results),
            "result_type": "Passwords"
        })
        return render_template("home.html", **context)

    # -------------------------
    # PASSKEY GENERATION
    # -------------------------
    elif action == "passkey":
        try:
            count = int(data.get("howmanypasswords", 10))
        except (ValueError, TypeError):
            context["error"] = "Invalid passkey count"
            return render_template("home.html", **context)

        key_chars = list("QW2ER4TY3UP5AS6DF7GH8JKL9ZXCVBNM")
        segment_size = 5
        segments_per_key = 4  # 20 chars

        results = []

        for _ in range(count):
            segments = [
                "".join(secrets.choice(key_chars) for _ in range(segment_size))
                for _ in range(segments_per_key)
            ]
            results.append("-".join(segments))

        context.update({
            "result": "\n".join(results),
            "result_type": "Passkeys"
        })
        return render_template("home.html", **context)

    context["error"] = "Invalid action"
    return render_template("home.html", **context)


if __name__ == "__main__":
    app.run(debug=True)

