import json
import sys


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Give me name and phone please."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Give me name and phone please."

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        return "Contact not found."


@input_error
def phone_contact(args, contacts):
    [name] = args
    if name in contacts:
        return contacts[name]
    else:
        return "Contact not found."


@input_error
def all_contacts(contacts):
    return json.dumps(contacts, sort_keys=True, indent=4)


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, contacts))
            elif command == "change":
                print(change_contact(args, contacts))
            elif command == "phone":
                print(phone_contact(args, contacts))
            elif command == "all":
                print(all_contacts(contacts))
            else:
                print("Invalid command.")
        except ValueError as error:
            sys.stderr.write(f'Invalid command.: {str(error)}\n')


if __name__ == "__main__":
    main()
