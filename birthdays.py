#!/usr/python

import argparse
import json
import os.path
import sys

from datetime import datetime, timedelta

class Person:
    def __init__(self, name, gender, birthday):
        self.name = name
        self.gender = gender
        self.birthday = birthday

    def get_name(self):
        return self.name

    def get_birthday_in_year(self, year):
        return datetime(year, self.birthday.month, self.birthday.day)

    def get_days_until_next_birthday(self):
        today = get_current_time_midnight()

        current_year_birthday = self.get_birthday_in_year(today.year)
        next_year_birthday = self.get_birthday_in_year(today.year + 1)

        days_until_current_year_birthday = (current_year_birthday - today).days
        days_until_next_year_birthday = (next_year_birthday - today).days

        if days_until_current_year_birthday >= 0:
            return days_until_current_year_birthday
        else:
            return days_until_next_year_birthday

    def get_next_birthday_age(self):
        if self.birthday.year == 1900:
            return None

        next_birthday = get_current_time_midnight() + timedelta(days=self.get_days_until_next_birthday())

        return next_birthday.year - self.birthday.year

    def get_personal_pronoun(self):
            if self.gender.lower() == 'male':
                return 'he'

            elif self.gender.lower() == 'female':
                return 'she'

            #TODO allow custom pronouns
            return 'they'

    def get_objective_pronoun(self):
            if self.gender.lower() == 'male':
                return 'him'

            elif self.gender.lower() == 'female':
                return 'her'

            #TODO allow custom pronouns
            return 'them'

    def get_possessive_pronoun(self):
            if self.gender.lower() == 'male':
                return 'his'

            elif self.gender.lower() == 'female':
                return 'her'

            #TODO allow custom pronouns
            return 'their'

    def get_days_until_birthday_string(self):
        time_specifier = ''
        age_specifier = ''
        days_until_next_birthday = self.get_days_until_next_birthday()
        next_birthday_age = self.get_next_birthday_age()

        if days_until_next_birthday == 0:
            time_specifier = 'today'
        elif days_until_next_birthday == 1:
            time_specifier = 'tomorrow'
        else:
            time_specifier = 'in {} days'.format(days_until_next_birthday)

        if next_birthday_age is not None:
            age_specifier = ' and {} will be {} years old'.format(self.get_personal_pronoun(), next_birthday_age)

        return '{}\'s birthday is {}{}'.format(self.name, time_specifier, age_specifier)

class UpcomingBirthday:
    def __init__(self, person):
        self.person = person
        self.days_until_next_birthday = self.person.get_days_until_next_birthday()

    def to_string(self):
        return self.person.get_days_until_birthday_string()

def process_args():
    global data_file

    parser = argparse.ArgumentParser()

    parser.add_argument('data_file')
    args = parser.parse_args()

    data_file = args.data_file

def get_json_data(json_file):
    data = None
    with open(json_file) as f:
        data = json.load(f)

    return data

def get_birthday(person):
    birthday_data = person['birthday']

    day = birthday_data['day']
    month = birthday_data['month']
    year = 1900

    try:
        year = birthday_data['year']
    except:
        pass

    return datetime(year, month, day)

def get_current_time_midnight():
    now = datetime.now()
    return datetime(now.year, now.month, now.day)

def get_days_until_next_future_birthday(person):
    today = get_current_time_midnight()

    previous_year_birthday = get_birthday_in_year(today.year - 1, person)
    current_year_birthday = get_birthday_in_year(today.year, person)
    next_year_birthday = get_birthday_in_year(today.year + 1, person)

    days_until_current_year_birthday = (current_year_birthday - today).days
    days_until_next_year_birthday = (next_year_birthday - today).days

    if days_until_current_year_birthday >= 0:
        return days_until_current_year_birthday
    else:
        return days_until_next_year_birthday

def get_alert_threshold_days(data):
    return data['birthday-alerts']['alert-threshold-days']

def print_upcoming_birthdays(upcoming_birthdays):
    upcoming_birthdays.sort(key=lambda x: x.days_until_next_birthday)
    for item in upcoming_birthdays:
        print('{}'.format(item.to_string()))

def process_file(data_file):
    data = get_json_data(data_file)
    now = datetime.now()

    upcoming_birthdays = []

    for person_data in data['people']:
        person = Person(person_data['name'], person_data['gender'], get_birthday(person_data))
        days_until_next_birthday = person.get_days_until_next_birthday()

        if days_until_next_birthday <= get_alert_threshold_days(data):
            upcoming_birthdays.append(UpcomingBirthday(person))
            
    print_upcoming_birthdays(upcoming_birthdays)

def main():
    global data_file

    process_args()
    process_file(data_file)

if __name__ == '__main__':
    main()
