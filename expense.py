class Expense():
    def __init__(self, title, amount, category, date, description):
        self.title = title
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def show_details(self):
        print(f"Title: {self.title}")
        print(f"Amount: {self.amount}")
        print(f"Category: {self.category}")
        print(f"Date: {self.date}")
        print(f"Description: {self.description}")

    def update_amount(self, amount):
        if amount > 0:
            self.amount = amount
        else:
            return "Amount must be greater than 0"

    def is_valid(self):
        if self.title != "" and self.amount > 0 and self.category != "":
            return True
        return False


expense1 = Expense(
    "Bills",
    2500,
    "expense",
    "23-04-2025",
    "This month bill"
)

expense1.update_amount(3000)

print(expense1.is_valid())

expense1.show_details()