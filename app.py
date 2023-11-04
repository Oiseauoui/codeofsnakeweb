# app.py
from flask import Flask, render_template, request
from Bot import Bot, AddressBook

app = Flask(__name__)
address_book = AddressBook("address_book.dat")  # Create an instance of AddressBook
bot = Bot(address_book)


@app.route("/")
def home():
    return render_template("index.html")  # Create an HTML template for the interface


@app.route("/handle_command", methods=["POST"])
def handle_command():
    command = request.form["command"]
    response = bot.handle_command(address_book, command)
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
