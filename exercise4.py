import json
import sys
import re
from typing import TypedDict, List, Callable


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as err:
            return str(err)
        except ValueError as err:
            return str(err)
        except IndexError as err:
            return str(err)

    return inner


class ParameterRestrictions(TypedDict):
    required: bool
    help: str
    validator: Callable[[any], bool]


def name_validator(name: str) -> (bool, str):
    if len(name) < 3:
        return False, f"{name} is too short.\n Minimal length must be 3"

    if not re.match(r"^[a-zA-Z]+$", name):
        return False, f"{name} is not a valid Contact name.\n Only alphabetic characters are allowed"

    return True, name


def phone_validator(phone_number: str) -> (bool, str):
    if re.match(r"[^0-9\s\-+]", phone_number):
        return False, f"{phone_number} is not a valid phone number."

    phone_number_stripped = re.sub('[^0-9]', '', phone_number)
    if (len(phone_number_stripped) != 12) and (len(phone_number_stripped) != 10):
        return False, f"{phone_number} is not a valid phone number."

    return True, phone_number


def validate_parameters(
        parameters: list,
        restrictions: List[ParameterRestrictions],
        parameters_help: str = "Give me a list of parameters.") -> None:
    expected_length = len(restrictions)
    actual_length = len(parameters)
    if actual_length > expected_length:
        raise ValueError(f"Parameter list is longer than the restrictions list: "
                         f"expected {expected_length}, got {expected_length}.\n {parameters_help}")

    for idx, restriction in enumerate(restrictions):
        if restriction["required"] and actual_length < idx + 1:
            raise ValueError(f"Positional parameter #{idx + 1} is required: {restriction["help"]}")

        if restriction["validator"]:
            [is_valid, explanation] = restriction["validator"](parameters[idx])
            if not is_valid:
                raise ValueError(f"Parameter {restriction["help"]} is invalid: {explanation}")


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args: list, contacts: dict) -> str:
    validate_parameters(
        parameters=args,
        restrictions=[
            ParameterRestrictions(required=True, help="Contact name", validator=name_validator),
            ParameterRestrictions(required=True, help="Phone", validator=phone_validator),
        ],
        parameters_help="Add new contact with phone.",
    )
    name, phone = args
    if name in contacts:
        raise KeyError(f"Contact {name} already exists.")

    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: list, contacts: dict) -> str:
    validate_parameters(
        parameters=args,
        restrictions=[
            ParameterRestrictions(required=True, help="Contact name", validator=name_validator),
            ParameterRestrictions(required=True, help="Phone", validator=phone_validator),
        ],
        parameters_help="Update phone of existing contact.",
    )

    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        raise KeyError("Contact not found.")


@input_error
def phone_contact(args: list, contacts: dict) -> str:
    validate_parameters(
        parameters=args,
        restrictions=[ParameterRestrictions(required=True, help="Contact name", validator=name_validator)],
        parameters_help="Get phone number by name"
    )
    [name] = args
    if name in contacts:
        return contacts[name]
    else:
        raise KeyError("Contact not found.")


@input_error
def all_contacts(contacts: dict) -> str:
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
                raise ValueError("Invalid command.\n"
                                 "Available commands are: close, exit, hello, add, change, phone, all")
        except ValueError as error:
            sys.stderr.write(f'Invalid command.: {str(error)}\n')


if __name__ == "__main__":
    main()
