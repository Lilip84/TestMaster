from faker import Faker
import random
import string

class DataGenerator:
    def __init__(self, locale='ru_RU'):
        self.fake = Faker(locale)
    
    def generate(self, data_type, **params):
        generators = {
            'email': self.fake.email,
            'name': self.fake.name,
            'phone': self.fake.phone_number,
            'text': lambda: self.fake.text(max_nb_chars=params.get('length', 200)),
            'date': self.fake.date,
            'address': self.fake.address,
            'string': lambda: ''.join(random.choices(string.ascii_letters + string.digits, k=params.get('length', 10))),
            'number': lambda: random.randint(params.get('min', 0), params.get('max', 100))
        }
        
        if data_type in generators:
            return generators[data_type]()
        else:
            raise ValueError(f"Unsupported data type: {data_type}")