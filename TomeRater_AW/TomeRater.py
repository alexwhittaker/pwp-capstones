# TomeRater - Program to keep track of users, books, and users' ratings of books

# Version log
# V1    2018-09-29  Initial version produced for submission


# Configuration settings

min_rating = 0  # Minimum rating a book can be given (inclusive)
max_rating = 4  # Maximum rating a book can be given (inclusive)



# Function to define if rating is valid
def is_valid_rating(rating):
    
    # Need to handle if rating isn't an integer (e.g. is None)
    try:
        return rating >= min_rating and rating <= max_rating
    except TypeError:
        return False


# Users can rate books
class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email=email
        self.books={}

    def get_email(self):
        return self.email

    def change(self, new_email):
        self.email = new_email
        print("Email for {user} has been changed to {email}.".format(user=self.name, email=self.email))

    def __repr__(self):
        return"<User - Name:{name}, Email:{email}, Books read:{books}>".format(name=self.name, email = self.email, books = len(self.books))

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email

    def read_book(self, book, rating=None):
        if is_valid_rating(rating) or rating == None:
            self.books[book] = rating
        else:
            print("Invalid rating {rating} for {book}".format(rating=rating, book=book))

    # Get average ratings from a user, ignoring "None"
    def get_average_rating(self):
        total_rating = 0
        count_ratings = 0
        for rating in self.books.values():
            if not rating == None:
                total_rating += rating
                count_ratings += 1
        return rating / count_ratings


# Books are rated by users
class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def __eq__(self, other_book):
        return self.name == other_book.name and self.isbn == other_book.isbn

    # Make objects of this class hashable, so we can use them as dict keys
    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return "{title} (not listed as fiction or non-fiction)".format(title = self.title)

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        print("ISBN for {book} has been changed from {old} to {new}.".format(book = self.title, old = self.isbn, new=new_isbn))
        self.isbn = new_isbn

    def add_rating(self, rating):
        if is_valid_rating(rating) or rating == None:
            self.ratings.append(rating)
        else:
            print("Invalid rating {rating} for {book}".format(rating=rating, book=self))

    # Get the average rating of a book, ignoring "none"
    def get_average_rating(self):
        total_rating = 0
        rating_count = 0
        for rating in self.ratings:
            if not rating == None:
                total_rating += rating
                rating_count += 1
        return rating / rating_count


# Fiction books additionally have an author
class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title = self.title, author = self.author)


# Non-fiction books additionally have a subject and level
class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title = self.title, level = self.level, subject = self.subject)


# Main application class to keep track of logic between books and users
class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def __repr__(self):
        return "<Instance of TomeRater with {usercount} users and {bookcount} books>".format(usercount = len(self.users), bookcount = len(self.books))

    # Consider two instances to be equal if they have the same books and users
    def __eq__(self, other):
        return self.users == other.users and self.books == other.books


    def create_book(self, title, isbn):
        # Check ISBN doesn't already exist
        for book in self.books:
            if book.get_isbn() == isbn:
                print("{title} already has the ISBN {isbn}!".format(title = book.get_title(), isbn = book.get_isbn()))
                return None

        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    # Add a reading of a book to a specific user
    def add_book_to_user(self, book, email, rating = None):
        if email in self.users:
            
            #Store the rating in both the user and book
            self.users[email].read_book(book, rating)
            book.add_rating(rating)

            # Store that one more user has read the book
            if book in self.books:
                self.books[book] += 1

            else:
                self.books[book] = 1

        else:
            print("No user with email {email}!".format(email = email))


    # Add a new user to the system, with optional list of books
    def add_user(self, name, email, user_books = None):
        
        if email in self.users:
            print("Error - user {email} already exists!".format(email = email))
            return None

        if not ("@" in email and (".com" in email or ".edu" in email or ".org" in email)):
            print("Error - \"{email}\" does not appear to be a valid email address!".format(email = email))
            
        self.users[email] = User(name, email)

        if not user_books == None:
            for book in user_books:
                self.add_book_to_user(book, email)


    # Analysis methods

    # Print a list of all books in the system
    def print_catalog(self):
        for book in self.books:
            print(book)

    # Print a list of all users in the system
    def print_users(self):
        for user in self.users:
            print(user)

    # Return total number of books read in the system
    def total_reads(self):
        total_reads = 0
        for book, reads in self.books.items():
            total_reads += reads
        return total_reads

    # Return the book that has been read the most
    def get_most_read_book(self):
        highest_reads = 0
        most_read_book = None
        for book, reads in self.books.items():
            if reads > highest_reads:
                most_read_book = book
                highest_reads = reads
        return most_read_book

    # Return the book that has the highest rating
    def highest_rated_book(self):
        highest_rating = 0
        highest_rated_book = None
        for book in self.books:
            if book.get_average_rating() > highest_rating:
                highest_rated_book = book
                highest_rating = book.get_average_rating()
        return highest_rated_book

    # Return the user with the highest average rating
    def most_positive_user(self):
        highest_rating = 0
        most_positive_user = None
        for email, user in self.users.items():
            if user.get_average_rating() > highest_rating:
                most_positive_user = user
                highest_rating = user.get_average_rating()
        return most_positive_user