from dataclasses import dataclass

@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    phone_number: str

    def __str__(self):
        return self.customer_id