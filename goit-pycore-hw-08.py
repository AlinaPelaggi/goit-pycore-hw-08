# Восьме завдання
from datetime import datetime, timedelta
from collections import UserDict
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if not isinstance(phone, Phone):
            raise ValueError("Phone must be an instance of the Phone class")
        self.phones.append(phone)

    def add_birthday(self, birthday):
        if not isinstance(birthday, Birthday):
            raise ValueError("Birthday must be an instance of the Birthday class")
        self.birthday = birthday

    def __str__(self):
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError("Record must be an instance of the Record class")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.now().date()
        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, '%d.%m.%Y').date().replace(year=today.year)
                if today <= birthday_date <= today + timedelta(days=7):
                    upcoming_birthdays.append(record)
        return upcoming_birthdays

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            error_message = {
                KeyError: "Please enter user name",
                ValueError: "Enter name and phone number please",
                IndexError: "Invalid index. Please try again"
            }
            print(error_message.get(type(e), "Error occurred. Please try again."))
    return wrapper

@input_error
def add_contact(args, book):
    name, phone = args
    record = Record(name)
    record.add_phone(Phone(phone))
    book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, book):
    name, new_phone = args
    record = book.find(name)
    if record:
        record.add_phone(Phone(new_phone))
        return "Phone number changed."
    else:
        return "Contact not found."

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return f"Phone number: {', '.join(str(p) for p in record.phones)}"
    else:
        return "Contact not found."

@input_error
def show_all(book):
    return "\n".join([str(record) for record in book.data.values()])

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(Birthday(birthday))
        return "Birthday added."
    else:
        return "Contact not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{record.name.value}'s birthday: {record.birthday.value}"
    else:
        return "Contact not found or birthday not set."

@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join([f"{record.name.value}'s birthday: {record.birthday.value}" for record in upcoming_birthdays])
    else:
        return "No upcoming birthdays in the next week."

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

def main():
    book = load_data()  # Завантаження даних при запуску програми
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)  # Збереження даних перед виходом
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()