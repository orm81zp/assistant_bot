from datetime import datetime
from ..constants import TEXT, DATE_OUTPUT_FORMAT
from ..utils import print_diff
from ..decorators import confirm_prompt
from .name import Name
from .phone import Phone
from .birthday import Birthday
from .email import Email
from .address import Address


class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def get_phones(self, delimeter=", ", no_data_message="") -> str:
        return delimeter.join([phone.value for phone in self.phones]) if len(self.phones) > 0 else no_data_message

    def get_phone(self, phone_number) -> Phone | None:
        for phone in self.phones:
            if str(phone) == phone_number:
                return phone

        return None

    def get_birthday_datetime(self) -> datetime | None:
        if self.birthday:
            day, month, year = str(self.birthday).split(".")
            birthday = datetime(year=int(year), month=int(month), day=int(day))
            return birthday
        return None

    def get_birthday(self):
        birthday_datetime = self.get_birthday_datetime()
        if birthday_datetime:
            return birthday_datetime.strftime(DATE_OUTPUT_FORMAT)
        return None

    def add_phone(self, phone_number):
        phone = self.get_phone(phone_number)
        if phone:
            print(TEXT["EXISTS"])
        else:
            self.phones.append(Phone(phone_number))
            print(TEXT["ADDED"])
            return True

    def add_birthday(self, birthday: str) -> bool:
        if self.birthday:
            old_birthday = str(self.birthday)
            self.birthday = Birthday(birthday)
            print(TEXT["UPDATED"])
            print_diff(old_birthday, birthday)
        else:
            self.birthday = Birthday(birthday)
            print(TEXT["ADDED"])

        return self.birthday is not None

    def add_email(self, email: str) -> bool:
        if self.email is not None:
            old_email = str(self.email)
            self.email.value = email
            print(TEXT["UPDATED"])
            print_diff(old_email, email)
        else:
            self.email = Email(email)
            print(TEXT["ADDED"])

        return self.email is not None

    def add_address(self, address: str):
        if self.address is not None:
            old_address = str(self.address)
            self.address.value = address
            print(TEXT["UPDATED"])
            print_diff(str(old_address), address)
        else:
            self.address = Address(address)
            print(TEXT["ADDED"])

        return  self.address is not None

    def show_birthday(self):
        if self.birthday:
            print(self.get_birthday())
        else:
            print(TEXT["NOT_FOUND"])

    def show_email(self):
        if (self.email):
            print(self.email)
        else:
            print(TEXT["NOT_FOUND"])

    def show_address(self):
        if self.address:
            print(self.address)
        else:
            print(TEXT["NOT_FOUND"])

    def show_phone(self):
        if len(self.phones) > 0:
            print(self.get_phones())
        else:
            print(TEXT["NOT_FOUND"])

    @confirm_prompt("Existing address will be deleted, continue?")
    def remove_address(self):
        if self.address:
            self.address = None
            print(TEXT["DELETED"])
        else:
            print(TEXT["NOT_FOUND"])

    @confirm_prompt("Existing email will be deleted, continue?")
    def remove_email(self):
        if self.email:
            self.email = None
            print(TEXT["DELETED"])
        else:
            print(TEXT["NOT_FOUND"])

    @confirm_prompt("Existing birthday will be deleted, continue?")
    def remove_birthday(self):
        if self.birthday:
            self.birthday = None
            print(TEXT["DELETED"])
        else:
            print(TEXT["NOT_FOUND"])

    @confirm_prompt("Existing phone number will be deleted, continue?")
    def remove_phone(self, phone_number):
        phone = self.get_phone(phone_number)
        if phone:
            self.phones = list(filter((lambda phone: str(phone) != phone_number), self.phones))
            print(TEXT["DELETED"])
            return True

        print(TEXT["NOT_FOUND"])

    @confirm_prompt("Existing name will be changed, continue?")
    def change_name(self, name, new_name):
        if name != new_name:
            self.name.value = new_name
            print(TEXT["UPDATED"])
            print_diff(name, new_name)
            return True

        print(TEXT["EQUAL"])
        return False

    @confirm_prompt("Existing phone number will be updated, continue?")
    def edit_phone(self, old_phone, new_phone):
        phone = self.get_phone(old_phone)
        if phone:
            phone.value = new_phone
            print(TEXT["UPDATED"])
            print_diff(old_phone, new_phone)
            return True

        print(TEXT["NOT_FOUND"])

    def __str__(self):
        birthday = f", birthday: {self.birthday}" if self.birthday else "-"
        email = f", email: {self.email}" if self.email else "-"
        address = f", address: {self.address}" if self.address else "-"
        phones = f", phones: {self.get_phones("; ", "-")}"
        return f"Contact name: {self.name}{phones}{birthday}{email}{address}"


__all__ = ["Record"]
