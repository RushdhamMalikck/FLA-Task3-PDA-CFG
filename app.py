from flask import Flask, render_template, request
from validators import check_palindrome, check_html, check_blocks

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    selected = request.form.get("case", "palindrome")
    user_input = request.form.get("user_input", "")

    if request.method == "POST":
        if selected == "palindrome":
            result = check_palindrome(user_input)
        elif selected == "html":
            result = check_html(user_input)
        elif selected == "blocks":
            result = check_blocks(user_input)

    return render_template(
        "index.html",
        result=result,
        selected=selected,
        user_input=user_input
    )

if __name__ == "__main__":
    app.run(debug=True)
