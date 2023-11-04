from datetime import datetime
import re
from abc import ABC, abstractmethod


class Field(ABC):
    @abstractmethod
    def __getitem__(self):
        pass

    def __init__(self, value=None):
        self.value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def __getitem__(self, index):
        return self.value[index]

    def get_value(self):
        return self.value


# Concrete subclass of Name
class ConcreteName(Name):
    pass


# 15.10.23 Olga
class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)

    def get_value(self):
        return str(self.value)

    def set_value(self, value):
        validated_phone = self.validate_phone(value)
        if validated_phone is None:
            print("Invalid phone number format")
        else:
            self.value = validated_phone

    @staticmethod
    def validate_phone(phone):
        new_phone = (
            str(phone)
            .strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        if new_phone.startswith("38") and len(new_phone) == 12:
            return "+" + new_phone
        elif len(new_phone) == 10:
            return "+38" + new_phone
        else:
            return None

    def __getitem__(self):
        return self.value


# 15.10.23 Yulia


class EmailAddress(Field):
    def __init__(self, value=None):  # =None убрала 16.10 Olha
        super().__init__(value)
        self.value = value

    def __getitem__(self):
        pass

    def set_value(self, value):
        validated_email = self.validate_email(value)
        if isinstance(value, str) and self.validate_email(value):
            self.value = validated_email  # value
        else:
            print("Invalid email format")

    def get_value(self):
        return self.value

    @staticmethod
    def validate_email(email):  # 16.10.23
        pattern = r"[A-Za-z][A-Za-z0-9._]+@[A-Za-z]+\.[A-Za-z]{2,}\b"
        temp_email = re.findall(pattern, email)
        if temp_email:
            return "".join(temp_email)  # True
        else:
            return False


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)

    def set_value(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            try:
                # пытаемся прочитать дату в формате 'dd-mm-yy'
                datetime.strptime(value, "%d-%m-%y")
            except ValueError:
                print("Invalid date format. Please use 'dd.mm.yyyy'")
                return

        self.value = value

    def days_to_birthday(self):
        if not self.value:
            return None
        # print(f"Attempting to parse date: {self.value}")
        try:
            birth_date = datetime.strptime(self.value, "%d.%m.%Y").date()
        except ValueError as e:
            print(f"Error parsing date '{self.value}': {e}")
            return None

        current_date = datetime.now().date()  # Use only the date part

        # Calculate next birthday date
        next_birthday_year = current_date.year
        if (current_date.month, current_date.day) > (birth_date.month, birth_date.day):
            next_birthday_year += 1

        next_birthday_date = datetime(
            next_birthday_year, birth_date.month, birth_date.day
        ).date()

        difference = next_birthday_date - current_date
        days_until_birthday = difference.days

        return days_until_birthday

    def __getitem__(self):
        return self.value

    def get_value(self):
        return self.value


class Record:
    def __init__(self, name, birthday=None, email=None):
        self.email = None
        self.name = Name(name)
        self.phones = []
        self.emails = [] if email else [EmailAddress(email)]
        self.birthday = Birthday(birthday) if birthday else None

    def add_email(self, email):  # 16.10.23 Olha
        if isinstance(email, EmailAddress):
            self.emails.append(email)
        elif EmailAddress.validate_email(email):
            email_value = EmailAddress.validate_email(email)
            if email_value:
                self.emails.append(EmailAddress(email_value))
            else:
                print("Invalid email number format")
        else:
            self.emails.append(
                EmailAddress(None)
            )  # new - пофиксила баг с корректной перезаписью Email
            print("Invalid email number format")

    def get_emails(self):
        if hasattr(self, "emails"):
            return (
                [
                    email
                    for email in self.emails
                    if email and isinstance(email, EmailAddress)
                ]
                if self.emails
                else []
            )
        elif hasattr(self, "email"):
            return (
                [self.email]
                if self.email and isinstance(self.email, EmailAddress)
                else []
            )
        else:
            return []


    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    # 16.10.23  Olha
    def remove_email(self, email):
        self.emails = [p for p in self.emails if p.value != email]

    def edit_phone(self, phone, new_phone):
        for p in self.phones:
            if p.value == phone:
                p.set_value(new_phone)
                break
        else:
            raise ValueError("Phone number not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

    # 15.10.23 Yulia
    def get_email(self):
        return self.email.get_value() if self.email else None

    # 16.10.23 Olha
    def edit_email(self, email, new_email):
        for p in self.emails:
            if p.value == email:
                p.set_value(new_email)
                break
        else:
            raise ValueError("Email not found")
