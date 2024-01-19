import csv
import hashlib
import os
from datetime import datetime


class UserDataManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserDataManager, cls).__new__(cls)
            cls._instance.users = {}
            cls._instance.load_data()
        return cls._instance

    def load_data(self):
        if os.path.exists("user_data.csv"):
            with open("user_data.csv", mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    username, hashed_password = row
                    self.users[username] = hashed_password

    def save_data(self):
        with open("user_data.csv", mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "HashedPassword"])
            for username, hashed_password in self.users.items():
                writer.writerow([username, hashed_password])

    def register_user(self, username, password):
        if username not in self.users:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.users[username] = hashed_password
            self.save_data()
            return True
        return False

    def authenticate_user(self, username, password):
        hashed_password = self.users.get(username)
        if hashed_password:
            if hashed_password == hashlib.sha256(password.encode()).hexdigest():
                return True
        return False


class UserCalendarManager:
    def __init__(self, manager):
        self.user_data_manager = manager
        self.calendars = {}

    def create_calendar(self, username):
        if username in self.user_data_manager.users:
            self.calendars[username] = Calendar(user=username)
            return True
        return False

    def get_user_calendar(self, username):
        return self.calendars.get(username)


class Calendar:
    def __init__(self, user):
        self.user = user
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def remove_event(self, event):
        if event in self.events:
            self.events.remove(event)

    def get_events_in_range(self, start_date, end_date):
        result_events = []
        for event in self.events:
            if start_date <= event.start_date <= end_date:
                result_events.append(event)
        return result_events

    def process_events(self):
        pass


class Event:
    def __init__(self, description, start_date):
        self.participants = None
        self.description = description
        self.start_date = start_date

    def add_participant(self, param):
        pass

    def remove_participant(self, param):
        pass


if __name__ == "__main__":
    user_data_manager = UserDataManager()
    user_calendar_manager = UserCalendarManager(user_data_manager)

    user_data_manager.register_user("john_doe", "password123")

    if user_data_manager.authenticate_user("john_doe", "password123"):
        print("Authentication successful.")
    else:
        print("Authentication failed.")

    user_calendar_manager.create_calendar("john_doe")

    user_calendar = user_calendar_manager.get_user_calendar("john_doe")

    event = Event(description="Meeting with client", start_date=datetime(2023, 1, 10, 14, 0))
    user_calendar.add_event(event)

    user_calendar.process_events()

    start_date_range = datetime(2023, 1, 1)
    end_date_range = datetime(2023, 1, 20)
    events_in_range = user_calendar.get_events_in_range(start_date_range, end_date_range)

    print(f"Events for {user_calendar.user} in the range {start_date_range} to {end_date_range}:")
    for event in events_in_range:
        print(f"{event.start_date}: {event.description}")
