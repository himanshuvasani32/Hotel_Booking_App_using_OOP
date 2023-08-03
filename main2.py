import pandas

df = pandas.read_csv("hotels.csv", dtype={"id": str})
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_secure_card = pandas.read_csv("card_security.csv", dtype=str)

class Hotel:

    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book a hotel and change availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Checks the availability of a hotel"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class ReservationTicket:

    def __init__(self, customer_name, hotel):
        self.customer_name = customer_name
        self.hotel = hotel

    def generate(self):
        """Generates the reservation details of hotel booking."""
        content = f"""
        Thank you for the reservation!
        Here's your booking details:
        Name = {self.customer_name}
        Hotel = {self.hotel.name}
        """
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        """Checks the credit card details with database"""
        card_data = {"number": self.number, "expiration": expiration,
                     "holder": holder, "cvc": cvc}
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_secure_card.loc[df_secure_card["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


class BookSpaPackage:
    def __init__(self, customer_name, hotel):
        self.customer_name = customer_name
        self.hotel = hotel

    def bookspa(self):
        content = f"""
        Thank you for the reservation!
        Here's your booking details:
        Name = {self.customer_name}
        Hotel = {self.hotel.name}
        """
        return content


print(df)
hotel_ID = input("Enter the id of the hotel: ")
hotel = Hotel(hotel_id=hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard(number="1234")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(customer_name=name, hotel=hotel)
            print(reservation_ticket.generate())
            spa_choice = input("Do you want to book a spa package? ").lower()
            if spa_choice == "yes":
                book_spa_package = BookSpaPackage(customer_name=name, hotel=hotel)
                print(book_spa_package.bookspa())
            else:
                print("Enjoy your stay!")
        else:
            print("Credit card authentication failed.")
    else:
        print("Your credit card is not valid.")
else:
    print("Hotel is not available.")