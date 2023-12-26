from main import AddressBook
from main import Record
from main import Birthday

def Examle():

    print('*' * 100)

    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John", "2000-10-05")

    john_record.add_email("bobik@dog.yes")
    john_record.add_email("murzik@cat.yes")

    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane", "200002-20")
    jane_record.add_email("dfdf")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Створення та додавання нового запису для Sara
    sara_record = Record("Sara")
    sara_record.add_phone("5566997711")
    book.add_record(sara_record)
    sara_record.birthday = Birthday("1976-07-14")

    # Виведення всіх записів у книзі
    for record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    # Знаходження та редагування email для John
    john = book.find("John")
    john.edit_email("bobik@dog.yes", "sharik@dog.yes")

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
    # book.delete("Jane")

    book.exit()

if __name__ == "__main__":
    Examle()