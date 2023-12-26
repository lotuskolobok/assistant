from collections import UserDict
from datetime import datetime
from datetime import date

from pathlib import Path

import re
import pickle
import sort
import scan
import os
import notes


def validate_email(email):
    try:
        if re.match(r'^[\w]{1,}([\w.+-]{0,1}[\w]{1,}){0,}@[\w]{1,}([\w-]{0,1}[\w]{1,}){0,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$', email):
            return True
        else:
            raise ValueError
    except:
        print('Invalid email address! Please enter correct email')
        return False


def validate_phone(phone_number: str):
    
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


class Email(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return self.value


class Home(Field):
    @property
    def value(self):
        return self._Field__value

    @value.setter
    def value(self, value):
        self._Field__value = value

class Record:
    def __init__(self, name, birthday=None, home=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)
        self.emails = []
        self.home = Home(home)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, e-mails: {'; '.join(p.value for p in self.emails)}, address: {self.home}"

    
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
            return delta_days
        else:
            return ''
        
    def show_birthday(self):
        if self.birthday.value:
            return f"Contact name: {self.name.value}, birthday: {self.birthday.value}, left days: {self.days_to_birthday()}"
        else:
            return f"Contact name: {self.name.value}, birthday: {self.birthday.value}"
        

    def add_email(self, email: str):
        tmp = validate_email(email)
        if tmp:
            self.emails.append(Email(email))
        else:
            print(f'E-mail {email} is not valid.')
    
    def find_email(self, email: str):
        
        for e in self.emails:
            if e.value == email:
                return e

        return None
    
    def edit_email(self, old_email, new_email):
        email_obj = self.find_email(old_email)

        if email_obj:
            if validate_email(new_email):
                email_obj.value = new_email
            return True
        else:
            print(f'E-mail {old_email} not found.')
            return False
    

    def add_phone(self, phone_number: str):
        tmp = validate_phone(phone_number)
        if tmp:
            self.phones.append(Phone(tmp))
        else:
            print(f'Number {phone_number} is not valid.')

    def find_phone(self, phone_number: str):
        phone_number = validate_phone(phone_number)

        for phone in self.phones:
            if phone.value == phone_number:
                return phone

        return None

    def edit_phone(self, old_phone, new_phone):
        old_phone = validate_phone(old_phone)
        phone_obj = self.find_phone(old_phone)
        
        if phone_obj:
            new_phone = validate_phone(new_phone)
            phone_obj.value = new_phone
            return True
        else:
            print(f'Number {old_phone} not found.')
            return False

    def remove_phone(self, rem_phone):
        for phone in self.phones:
            if phone.value == rem_phone:
                self.phones.remove(phone)
    

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

    
    def find_record(self, part: str):
        result = {}

        for item, record in self.items():
            # пошук в phones
            for p in record.phones:
                if part in str(p):
                    result[item] = self.data[item]

            # пошук в name
            if part.lower() in item.lower():
                result[item] = self.data[item]
            
            # пошук в emails
            for e in record.emails:
                if part in str(e):
                    result[item] = self.data[item]

        return result
    
    # сериалізація адресної книги та запису її у файл
    def dump(self):
        with open('my_book.bin', 'wb') as file:
            if len(self.data) > 0:
                pickle.dump(self, file)
                return True

    # десериалізація адресної книги з файла
    def load(self):
        try:
            with open('my_book.bin', 'rb') as file:
                self.data = pickle.load(file)
        except:
            pass
           
    # сериалізація адресної книги при виході з програми
    def exit(self):
        result = self.dump()
        return result
        

# ----------------------------------------------------------------------------------------------------------


def assistant():

    my_book = None
    my_book = AddressBook()
    my_book.load()

    

    while True:
        
        result = False
        
        command = input('Input command or "?" for help: > ').lower().strip()
        print('*' * 20, f'{command}', '*' * 20)

        if command == "end" or command == "exit":
            my_book.exit()
            print ('Bye-Bye!')
            break
        
        elif command == 'add_contact':
            name = input('Input name for contact: ').strip()
            if name != '':
                birthday = input('Input bithday in format [yyyy-mm-dd]: ').strip()
                record = Record(name, birthday)

                my_book.add_record(record)
                
                result = True

            else:
                print("Name can't be empty. Try again.")
        
        elif command == 'del_contact':
            name = input('Input name for contact: ').strip()
            if name != '':
                my_book.delete(name)
                result = True

        elif command == 'add_address':
            name = input('Input contact name: ').strip()
            if name != '':
                record = my_book.find(name)
                if record:
                    home = input('Input address: ').strip()
                    record.home = home
                    result = True
                else:
                    print('Name not found.')

        elif command == 'add_birthday':
            name = input('Input contact name: ').strip()
            if name != '':
                record = my_book.find(name)
                if record:
                    birthday = input('Input birthday in format yyyy-mm-dd: ').strip()
                    record.birthday.value = birthday
                    result = True
                else:
                    print('Name not found.')

        elif command == 'add_email':
            name = input('Input contact name: ').strip()
            if name != '':
                record = my_book.find(name)
                if record:
                    email = input('Input email: ').strip()
                    record.add_email(email)
                    result = True
                else:
                    print('Name not found.')
        
        elif command == 'edit_email':
            name = input('Input contact name: ').strip()
            if name != '':
                record = my_book.find(name)
                if record:
                    old_email = input('Input old email: ').strip()
                    new_email = input('Input new email: ').strip()
                    record.edit_email(old_email, new_email)
                    result = True
                else:
                    print('Name not found.')
        
        elif command == 'add_phone':
            name = input('Input contact name: ').strip()
            if name != '':
                record = my_book.find(name)
                if record:
                    phone = input('Input phone number: ').strip()
                    record.add_phone(phone)
                    result = True
                else:
                    print('Name not found.')
        
        elif command == 'edit_phone':
            name = input('Input contact name: ').strip()
            if name != '':
                record = my_book.find(name)
                if record:
                    old_phone = input('Input old phone number: ').strip()
                    new_phone = input('Input new phone number: ').strip()
                    record.edit_phone(old_phone, new_phone)
                    result = True
                else:
                    print('Name not found.')

        elif command == 'find_record':
            find = input('Input symbols to search: ').strip()
            if find != '':
                records = my_book.find_record(find)
                if len(records):
                    print(f'-----Search by [{find}]--------')
                    for name, record in records.items():
                        print(record)
                    print('*' * 0)
                    result = True
                else:
                    print('Тo match found.')

        
        elif command.startswith('show_birthdays'):
            days = input('Input max days to birthdays: ')
            if days.isdigit():
                days = int(days)
                if my_book:
                    for name, record in my_book.data.items():
                        delta_days = record.days_to_birthday()
                        if delta_days:
                            if int(delta_days) < days:
                                print(record.show_birthday())
                    result = True
            else:
                print('Incorect value of days count')


        elif command == 'show_book':
            if my_book:
                for name, record in my_book.data.items():
                    print(record)
                    result = True
        
        elif command == 'scan_folder':
        
            folder = input('Input folder name for scaning: ') 

            if os.path.exists(folder):
                folder = Path(folder)
                scan.scan(folder)
                scan.scan_result()
                result = True
            else:
                print ('Folder not found')

        elif command == 'sort_folder':
            
            folder = input('Input folder name for sorting: ') 

            if os.path.exists(folder):
                folder = Path(folder)
                #sort.main(folder.resolve())
                sort.main(folder)
                result = True
            else:
                print('Error sorting files')

        elif command == 'notes':
            notes.main()

        elif command == "?":
            commands = []
            
            commands.append('- [end] or [exit] - quit program')
            
            commands.append('- [add_contact]    - adding contact to book')
            commands.append('- [del_contact]    - remove contact from book')
            commands.append('- [add_address]    - adding address to contact')
            commands.append('- [add_birthday]   - adding birthday to contact')
            commands.append('- [add_email]      - adding email to contact')
            commands.append('- [edit_email]     - edit email')
            commands.append('- [add_phone]      - adding phone number to contact')
            commands.append('- [edit_phone]     - edit phone number')
            commands.append('- [find_record]    - search contact by symbols')

            commands.append('- [show_birthdays] - show all birtdays in book')
            commands.append('- [show_book]      - show all contacts in book')
            
            commands.append('- [scan_folder]    - scan folder')
            commands.append('- [sort_folder]    - sort folder')
            commands.append('- [notes]          - case of notes')

            
            for c in commands:
                print(f'{c}')
        
        print('*' * 50)
        if result:
            print('Result: OK')
        print('*' * 50)


if __name__ == "__main__":
    assistant()

        


