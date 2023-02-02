import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': '/Users/esthergroenert/Documents/Udacity/2022/Python Project/all-project-files/chicago.csv',
              'New York City': '/Users/esthergroenert/Documents/Udacity/2022/Python Project/all-project-files/new_york_city.csv',
              'Washington': '/Users/esthergroenert/Documents/Udacity/2022/Python Project/all-project-files/washington.csv' }


def get_filters():  
    # Asks user to specify a city, month, and day to analyze
    # Returns:
        # (str) city - name of the city to analyze
        # (str) month - name of the month to filter by, or "All" to apply no month filter
        # (str) day - name of the day of week to filter by, or "All" to apply no day filter
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city (Chicago, New York City, Washington) 
    city = ''
    while True:
        city = str(input('Please indicate the city you are interested in (Chicago, New York City or Washington): ').title())

        if city in ['Chicago', 'New York City', 'Washington']:
            print('You are interested in {}.'.format(city))
            break
        else:
            print('Your input is invalid.')
        continue

    # Get user input for month (All, January, February, ... , June)
    month = ''
    while True:
        month = str(input('Please indicate the month you are interested in (All, January, February, March, April, May or June): ').title())

        if month == 'All':
            print('You are interested in all months.')
            break
        if month in ['January', 'February', 'March', 'April', 'May', 'June']:
            print('You are interested in {}.'.format(month))
            break
        else:
            print('Your input is invalid.')
        continue

    # Get user input for day of week (All, Monday, Tuesday, ... Sunday)
    day = ''
    while True:
        day = str(input('Please indicate the day of the week you are interested in (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday): ').title())

        if day == 'All':
            print('You are interested in all days.')
            break
        if day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            print('You are interested in {}.'.format(day))
            break
        else:
            print('Your input is invalid.')
        continue

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    
    # Loads data for the specified city and filters by month and day if applicable
    # Args:
        # (str) city - name of the city to analyze
        #  (str) month - name of the month to filter by, or "all" to apply no month filter
        #(str) day - name of the day of week to filter by, or "all" to apply no day filter
    # Returns:
        # df - Pandas DataFrame containing city data filtered by month and day
    
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'All':
        df = df[df['Month'] == month.title()]

    # Filter by day of week if applicable
    if day != 'All':
        df = df[df['Day of Week'] == day.title()]
    
    return df


def time_stats(df, month, day):
    # Displays statistics on the most frequent times of travel

    print('\nCalculating the most frequent times of travel...\n')
    start_time = time.time()

    # Display the most common month
    if month == 'All': 
        popular_month = df['Month'].mode()[0]
        print('Most popular start month:', popular_month)

    # Display the most common day of week
    if day == 'All':
        popular_weekday = df['Day of Week'].mode()[0]
        print('Most popular day of week:', popular_weekday)

    # Display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Hour'].mode()[0]
    print('Most popular start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    # Displays statistics on the most popular stations and trip

    print('\nCalculating the most popular stations and trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most popular start station:', popular_start)

    # Display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most popular end station:', popular_end)

    # Display most frequent combination of start station and end station trip
    popular_trip = (df['Start Station'] + ' + ' + df['End Station']).mode()[0]
    print('Most popular combination of start and end station:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    # Displays statistics on the total and average trip duration

    print('\nCalculating trip duration...\n')
    start_time = time.time()

    # Display total travel time
    duration_total = df['Trip Duration'].sum()
    print('Total travel time:', duration_total, 'seconds')

    # Display mean travel time
    duration_mean = df['Trip Duration'].mean()
    print('Mean travel time:', duration_mean, 'seconds')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    # Displays statistics on bikeshare users

    print('\nCalculating user stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Breakdown by user type:')
    print(user_types,'\n')

    # Display counts of gender
    if city in ['Chicago', 'New York City']:
        gender = df['Gender'].value_counts()
        print('Breakdown by user gender:')
        print(gender, '\n')

    # Display earliest, most recent, and most common year of birth
    if city in ['Chicago', 'New York City']:
        earliest = df['Birth Year'].min()
        print('Earliest year of birth: ', earliest)
        most_recent = df['Birth Year'].max()
        print('Most recent year of birth: ', most_recent)
        most_common = df['Birth Year'].mode()[0]
        print('Most common year of birth ', most_common)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        # Get user input for raw data and display 5 rows of data if requested
        i = 0
        raw = str(input('Would you like to see some raw data? Enter Yes or No. ').title())

        while True:
            if raw == 'No':
                break

            if i >= len(df):
                print('There is no more data to display.')
                break

            print(df[i:i+5])	
            raw = str(input('Would you like to see some more raw data? Enter Yes or No. ').title())
            i += 5

        restart = str(input('\nWould you like to restart? Enter Yes or No.\n').title())
        if restart != 'Yes':
            break

if __name__ == "__main__":
	main()
    
