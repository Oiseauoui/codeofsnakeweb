from sort import clean_folder_interface
from note import notebook_interface, Note
from AddressBook import AddressBook  # Make sure you import the relevant classes
from datetime import datetime
from info import Record
from info import Phone
from info import Birthday


class Bot:
    def __init__(
        self, filename="address_book.dat"
    ):  # Provide a default filename or pass it when creating an instance
        self.book = AddressBook(filename)

    def handle_command(self, address_book: object, command: object) -> object:
        # Розділити введену команду на частини
        parts = command.lower().split()

        # Перевірити, чи існують частини команди
        if not parts:
            print("Enter a command. Type 'helper' for a list of available commands.")
            return ""

        action, *args = parts

        # 15.10.23 Nazar
        if action == "add":
            if len(args) < 2:
                return "Invalid format for 'add' command. Please provide a name and at least one phone number."
            name = args[0]
            phones = []
            email = None
            birthday = None

            # Separate phones, email, and birthday
            for arg in args[1:]:
                if "@" in arg or any(
                    char.isalpha() for char in arg
                ):  # Check if arg is an email
                    email = arg
                elif len(arg.split(".")) == 3:
                    try:
                        datetime.strptime(arg, "%d.%m.%Y")
                        birthday = arg
                    except ValueError:
                        return "Invalid date format. Please use 'dd.mm.yyyy'."
                else:
                    phones.append(arg)

            record = Record(name, birthday, email)

            for phone in phones:
                phone_value = Phone.validate_phone(phone)
                if phone_value:
                    phone_obj = Phone(phone_value)
                    record.add_phone(phone_obj)
                else:
                    return "Invalid phone number format"

            # Add email if present
            if email:
                record.add_email(email)

            # Add only if the birthday is in the correct format
            if birthday:
                try:
                    datetime.strptime(birthday, "%d.%m.%Y")
                    record.birthday = Birthday(birthday)
                except ValueError:
                    return "Invalid date format. Please use 'dd.mm.yyyy'."

            # Add the record only if all data is valid
            address_book.add_record(record)

            # Save data immediately after adding
            address_book.save_to_file()

            phones_str = ", ".join([str(p.get_value()) for p in record.phones])
            email_str = ", ".join(
                [str(email.get_value()) for email in record.get_emails()]
            )
            birthday_str = record.birthday.get_value() if record.birthday else "None"

            response = (
                f"Contact {name} added with the following information:\n"
                f"Name: {record.name.get_value()}\n"
                f"Phone: {phones_str}\n"
                f"Email: {email_str if email else 'None'}\n"
                f"Birthday: {birthday_str if birthday else 'None'}"
            )

            # If birthday is present, calculate and append days until the next birthday
            if birthday:
                days_left = record.birthday.days_to_birthday()
                if days_left is not None:
                    response += f"\n{days_left} days left until the next birthday."

            # Custom message after adding any contact
            response += "\nContact saved!"

            return response

        # 15.10.23 Yulia
        elif action == "delete":
            if len(args) < 1:
                return "Invalid format for 'delete' command. Please provide a name."
            name = args[0]
            address_book.delete_contact(name)
            return ""

        # 14.10.23 Alex
        elif action == "notebook":
            notebook_interface()
            return "Work with notebook is completed."

        elif action == "birthday" and args[0]:
            if len(args) < 2:
                return "Invalid format for 'add birthday' command. Please provide a name and a birthday date."
            name = args[0]
            birthday = args[1]
            record = Record(name, birthday)
            address_book.add_record(record)
            response = f"Contact {name} added with birthday: {birthday}"
            days_left = record.birthday.days_to_birthday()
            if days_left is not None:
                response += f"\n{days_left} days left until the next birthday."
            return response

        # 15.10.23 Nazar , 16.10.23 modify Yuliya

        elif action == "change":
            if len(args) < 2:
                return "Invalid format for 'change' command. Please provide a name and either a new phone number, email, or birthday."

            name = args[0]
            record = address_book.find(name)
            if record:
                change_type = args[1].lower()

                if change_type == "phone" and len(args) >= 3:
                    new_phone = args[2]
                    try:
                        record.edit_phone(record.phones[0].get_value(), new_phone)
                        address_book.save_to_file()
                        # Empty string to suppress success message
                        return "" if Phone.validate_phone(new_phone) else ""
                    except ValueError:
                        return "Invalid phone number format"

                elif change_type == "email" and len(args) >= 3:
                    new_email = args[2]
                    try:
                        record.edit_email(record.emails[0].get_value(), new_email)
                        # Save only if email change is successful
                        address_book.save_to_file()
                        return ""  # Empty string to suppress success message
                    except ValueError:
                        return "Invalid email format"

                # modify Yuliya 18.10.23
                elif change_type == "birthday" and len(args) >= 3:
                    new_birthday = args[2]
                    try:
                        datetime.strptime(new_birthday, "%d.%m.%Y")
                        if record.birthday:
                            record.birthday.set_value(new_birthday)
                        else:
                            record.birthday = Birthday(new_birthday)
                        address_book.save_to_file()
                        return f"Contact {name} birthday changed to {new_birthday}"
                    except ValueError:
                        print("Invalid date format. Please use 'dd.mm.yyyy'")
                        return f"Contact {name} birthday didn't change. Invalid date format. Please use 'dd.mm.yyyy'"

        # 15.10.23 Nazar
        elif action == "find":
            if len(args) < 1:
                return (
                    "Invalid format for 'find' command. Please provide a search query."
                )
            search_query = " ".join(args)
            results = address_book.search(search_query)

            if results:
                contacts_info = []
                for record in results:
                    phones_str = ", ".join([p.get_value() for p in record.phones])
                    info = f"{record.name.get_value()}: {phones_str} | {record.birthday.get_value()}"

                    # Check if birthday is present
                    if record.birthday.get_value():
                        days_left = record.birthday.days_to_birthday()
                        birthday_info = (
                            f" | Birthday in {days_left} days"
                            if days_left is not None
                            else ""
                        )
                        info += birthday_info
                    contacts_info.append(info)
                return "\n".join(contacts_info)

            else:
                return f"No contacts found for '{search_query}'"

        # 15.10.23 Nazar
        elif action == "phone":
            if len(args) < 1:
                return "Invalid format for 'phone' command. Please provide a name."
            name = args[0]
            record = address_book.find(name)
            if record:
                phones_str = ", ".join([p.get_value() for p in record.phones])
                birthday_info = ""
                # Check if birthday is present
                if record.birthday.get_value():
                    days_left = record.birthday.days_to_birthday()
                    birthday_info = (
                        f" | Birthday in {days_left} days"
                        if days_left is not None
                        else ""
                    )
                return f"Phone number for {name}: {phones_str} | {record.birthday.get_value()} {birthday_info}"

            else:
                return f"Contact {name} not found"

            # add email 16.10.2023 Olha
        elif action == "email":
            if len(args) < 1:
                return "Invalid format for 'email' command. Please provide a name."
            name = args[0]
            record = address_book.find(name)

            if record:
                emails_list = []
                for i in record.emails:
                    if i is not None:
                        emails_list.append(str(i.get_value()))
                if emails_list:
                    emails_str = ", ".join(emails_list)
                else:
                    emails_str = "No emails"
                return f"Email for {name}: {emails_str}"
            else:
                return f"Contact {name} not found"

        # 14.10.23 Nazar / Yuliya pagination 18.10.23
        elif action == "show" and args and args[0] == "all":
            page_number = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
            total_pages = address_book.get_total_pages()

            if page_number < 1 or page_number > total_pages:
                return f"There are no contacts."

            page_records = address_book.iterator(page_number)

            if not page_records:
                return f"No contacts found on page {page_number}."

            contacts_info = []
            for record in page_records:
                phones_str = ", ".join([str(p.get_value()) for p in record.phones])
                email_str = ", ".join(
                    [str(email.get_value()) for email in record.get_emails()]
                )
                # Check if record.birthday is not None before accessing get_value()
                birthday_str = (
                    record.birthday.get_value() if record.birthday else "None"
                )

                info = f"{record.name.get_value()} | Phone: {phones_str or '-'} | Email: {email_str or '-'} | Birthday: {birthday_str or '-'}"

                # Check if record.birthday is not None before attempting to calculate the days until the next birthday
                if record.birthday:
                    days_left = record.birthday.days_to_birthday()
                    if days_left is not None:
                        info += f" | {days_left} days left until the next birthday."
                else:
                    info += " | No birthday information available."

                contacts_info.append(info)

            # Yuliya 18.10.23
            # Додамо опцію "наступна сторінка" та "попередня сторінка"
            prev_page = page_number - 1 if page_number > 1 else None
            next_page = page_number + 1 if page_number < total_pages else None
            pagination_info = f"\nPage {page_number} of {total_pages} |"
            if prev_page is not None:
                pagination_info += f" Previous: 'show all {prev_page}' |"
            if next_page is not None:
                pagination_info += f" Next: 'show all {next_page}' |"
            contacts_info.append(pagination_info)

            return "\n".join(contacts_info)

        elif action == "celebration" and args and args[0] == "in":
            if len(args) < 2 or not args[1].isdigit():
                return "Invalid format for 'celebration in' command. Please provide a valid number of days."

            days_until_celebration = int(args[1])
            upcoming_birthdays = []
            for record in address_book.data.values():
                if record.birthday.get_value():
                    days_left = record.birthday.days_to_birthday()
                    if days_left is not None and days_left <= days_until_celebration:
                        phones_str = ", ".join([p.get_value() for p in record.phones])
                        upcoming_birthdays.append(
                            f"{record.name.get_value()}: {phones_str} | {record.birthday.get_value()}. Don't forget to greet!"
                        )

            if upcoming_birthdays:
                return (
                    f"Upcoming birthdays in the next {days_until_celebration} days:\n"
                    + "\n".join(upcoming_birthdays)
                )
            else:
                return (
                    f"No upcoming birthdays in the next {days_until_celebration} days."
                )

        # 14.10.23 Nazar
        elif action == "helper":
            return (
                "Available commands:\n"
                "  - add [name] [phone][birthday] [emai]: Add a new contact with optional phones and birthday.\n"
                "  - show all: Display all contacts with phones and optional days until the next birthday.\n"
                "  - celebration in [days]: Show upcoming birthdays in the next [days] days with names and phones.\n"
                "  - helper: Display available commands and their descriptions.\n"
                "  - find [letter] or [number]: Display all contacts with letter or number, which you saied about.\n"
                "  - change [name] [phone] or [birthday]: Changes contact, which you want.\n"
                "  - phone [name]: phoning person you want.\n"
                "  - delete [name]: Delete a contact by name.\n"  # 15.10.23 Yuliya
                "  - goodbye, close, exit: Save the address book to a file and exit the program.\n"
                "  - clean: Open sorter.\n"  # 15.10.23 Alex
                "  - notebook: Open notes.\n"  # 15.10.23 Alex
                "  - email [name]: Shows all emails for a contact "  # 16.10.23 Olha
            )

        elif action == "unknown":
            print("Unknown command. Type 'helper' for a list of available commands.")
            return "Unknown command"

        elif action == "hello":
            return "How can I help you?"

        elif action in ["goodbye", "close", "exit"]:
            return "Good bye! Have a nice day"

        elif action == "clean":
            clean_folder_interface()
            return "Cleaning process finished."
        else:
            return "Unknown command"
