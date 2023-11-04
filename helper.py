import os
import logging
from Bot import Bot
from AddressBook import AddressBook

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ADDRESS_BOOK_PATH = os.path.join(BASE_DIR, "address_book.dat")

# Configure the logger
log_filename = os.path.join(BASE_DIR, "app.log")
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    # if __name__ == "__main__":
    filename = "address_book.dat"
    address_book = AddressBook(filename)
    address_book.read_from_file()

    print("Welcome to ContactBot!")
    bot = Bot()
    # Print the number of contacts loaded
    print(
        f"Address book loaded from {filename}. {len(address_book.data)} contacts found."
    )  # 15.10.23 modify Yulia

    # Yuliya 18.10.23
    # Словник для автодоповнення
    command_autocomplete = {
        "a": ["add"],
        "c": ["change", "celebration", "clean", "close"],
        "d": ["delete"],
        "e": ["exit"],
        "g": ["goodbye"],
        "f": ["find"],
        "h": ["helper"],
        "n": ["notebook"],
        "s": ["show all"],
        "p": ["phone"],
        # додайте інші літери за потребою
    }
    command_prompt = "Enter a command: "

    # Create a logger
    logger = logging.getLogger("ContactBot")

    # 16.10.23 Yulia - save data before exit
    while True:
        user_input = input(command_prompt).strip()

        if not user_input:
            if not user_input:
                print(
                    "Unknown command. Type 'helper' for a list of available commands."
                )
            continue  # If the user just pressed Enter, provide another chance to enter

        command = user_input[0]  # Take the first letter as the command

        # Check if the entered letter has autocomplete options
        autocomplete_options = command_autocomplete.get(command, [])
        if autocomplete_options and len(user_input) == 1:
            print("Available commands:", ", ".join(autocomplete_options))
            continue  # Wait for the user to input the complete command

        response = bot.handle_command(address_book, user_input)
        print(response)

        # Log the user's input and the bot's response
        logger.info(f"User input: {user_input}, Bot response: {response}")

        if user_input.lower() in ["goodbye", "close", "exit"]:
            address_book.save_to_file()
            logger.info("Application closed by user")
            break

# if __name__ == "__main__":
#     # main()  # Uncomment if you want to run the existing command-line interface
#     app.run(debug=True)
