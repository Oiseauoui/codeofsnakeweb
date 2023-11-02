from datetime import datetime as dt, timedelta
from collections import UserDict
import pickle
from info import *


class AddressBook(UserDict):
    def __init__(self, filename):
        super().__init__()
        self.page_size = 5
        self.filename = filename

    def read_from_file(self):
        try:
            with open(self.filename, 'rb') as file:
                data = pickle.load(file)
                self.data = data
            print(f'Address book loaded from {self.filename}')
        except FileNotFoundError:
            print(f'File {self.filename} not found. Creating a new address book.')
        except Exception as e:
            print(f'Error reading from {self.filename}: {str(e)}')


    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self):
        records = list(self.data.values())
        for i in range(0, len(records), self.page_size):
            yield records[i:i + self.page_size]

    def save_to_file(self):
        try:
            with open(self.filename, 'wb') as file:
                pickle.dump(self.data, file)
            print(f'Address book saved to {self.filename}')
        except Exception as e:
            print(f'Error saving to {self.filename}: {str(e)}')

    
    def search(self, query):
        query = query.lower()
        results = []
        for record in self.data.values():
            if query in record.name.get_value().lower():
                results.append(record)
            for phone in record.phones:
                if query in phone.get_value():
                    results.append(record)
        return results
    

    #15.10.23 Yulia
    def delete_contact(self, name):
        """
        Delete a contact by name.
        """
        if name in self.data:
            del self.data[name]
            self.save_to_file()  # Save data after each deletion
            print(f"Contact {name} deleted from address_bot - saved.")
        else:
            print(f"Contact {name} not found.")

#Yuliya 18.10.23
    def iterator(self, page_number=None):
            records = list(self.data.values())

            if page_number:
                start_idx = (page_number - 1) * self.page_size
                end_idx = start_idx + self.page_size
                page_records = records[start_idx:end_idx]
            else:
                page_records = records

            return page_records
    
    def get_page(self, page_number):
        start_index = (page_number - 1) * self.page_size
        end_index = start_index + self.page_size
        records = list(self.data.values())[start_index:end_index]
        return records

    def get_total_pages(self):
        total_contacts = len(self.data)
        return (total_contacts + self.page_size - 1) // self.page_size