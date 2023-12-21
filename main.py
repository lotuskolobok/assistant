from collections import UserDict
from datetime import datetime
from datetime import date

import re

def phone_validate(phone_number: str):
    
    try:
        phone_number = (phone_number.strip()
                        .replace('(', '')
                        .replace(')', '')
                        .replace('-', '')
                        .replace(' ', ''))
        
        if len(phone_number) == 13:
            if re.match('^\\+38\d{10}$', phone_number):
                return phone_number
            
        elif len(phone_number) == 12:
            if re.match('^\d{12}$', phone_number):
                phone_number = '+' + phone_number
                return phone_number
            
        elif len(phone_number) == 10:
            if re.match('^\d{10}$', phone_number):
                phone_number = '+38' + phone_number
                return phone_number
        else:
            raise ValueError    
            
    
    except:
        print (f'Number {phone_number} is not valid.')
        return None


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return self.value


class Birthday(Field):

    @property
    def value(self):
        return self._Field__value

    @value.setter
    def value(self, value):
        self._Field__value = self.validate(value)

    def validate(self, value):
        if value == None:
            return None

        try:
            datetime.strptime(value, '%Y-%m-%d')
            return value

        except ValueError:
            return None

class Record:
    def __init__(self, name, birthday=None, email=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)
        self.email = Email(email)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, email: {self.email.value}"

    def show_birthday(self):
        return f"Contact name: {self.name.value}, birthday: {self.birthday.value}"


    def days_to_birthday(self):
        if self.birthday.value is None:
            delta_days = 0
        else:
            try:
                this_date = date.today()
                birthday_date = date.fromisoformat(str(self.birthday.value))
                birthday_date = datetime(
                    year=this_date.year, month=birthday_date.month, day=birthday_date.day).date()

                delta_days = (birthday_date - this_date).days

                if delta_days < 0:
                    birthday_date = datetime(
                        year=this_date.year + 1, month=birthday_date.month, day=birthday_date.day).date()

                    delta_days = (birthday_date - this_date).days
            except:
                pass
        
        if delta_days > 0:
            return f'Birthday is coming in: {delta_days} days'
        else:
            return ''

    def add_phone(self, phone_number: str):
        tmp = phone_validate(phone_number)
        if tmp:
            self.phones.append(Phone(tmp))
        else:
            print(f'Number {phone_number} is not valid.')

    def find_phone(self, phone_number: str):
        phone_number = phone_validate(phone_number)

        for phone in self.phones:
            if phone.value == phone_number:
                return phone

        return None

    def edit_phone(self, old_phone, new_phone):
        old_phone = phone_validate(old_phone)
        phone_obj = self.find_phone(old_phone)
        
        if phone_obj:
            new_phone = phone_validate(new_phone)
            phone_obj.value = new_phone
            return True
        else:
            return False

    def remove_phone(self, rem_phone):
        for phone in self.phones:
            if phone.value == rem_phone:
                self.phones.remove(phone)


class Email(Field):
    def __str__(self):
        return self.value

    @property
    def email_value(self):
        return self._Field__value

    @email_value.setter
    def email_value(self, value):
        e = self.validate_email(value)
        if e:
            self._Field__value = value
        
    def validate_email(self, value):
        
        try:
            if re.match(r'^[\w]{1,}([\w.+-]{0,1}[\w]{1,}){0,}@[\w]{1,}([\w-]{0,1}[\w]{1,}){0,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$', self.value):
                return True
            else:
                raise ValueError
        except:
            print('Invalid email address! Please enter correct email')
            return False

class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    
    def find(self, name: str):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    # пошук записів за збігом в імені або номері телефона
    def find_record(self, part: str):
        result = {}

        for item, record in self.items():
            # пошук в номері телефона
            for p in record.phones:
                if part in str(p):
                    result[item] = self.data[item]

            # пошук в імені
            if part.lower() in item.lower():
                result[item] = self.data[item]

        return result
# ----------------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    print ('*' * 100)
    
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John", "2000-10-05", "bobik@dog.yes")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane", "200002-20")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Створення та додавання нового запису для Sara
    sara_record = Record("Sara")
    sara_record.add_phone("5566997711")
    book.add_record(sara_record)
    sara_record.birthday = Birthday("1976-07-14")

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Пошук за збігом в імені або номері телефона
    f = 'sa'
    print(f'-----Пошук за [{f}]--------')
    f = book.find_record(str(f))
    for name, record in f.items():
        print(record)
    print('-' * 30)

    # Виведення дати народження та кількості днів до дати народження
    print(jane_record.show_birthday(), jane_record.days_to_birthday())
    print(john_record.show_birthday(), john_record.days_to_birthday())
    print(sara_record.show_birthday(), sara_record.days_to_birthday())

    # Видалення запису Jane
    book.delete("Jane")
