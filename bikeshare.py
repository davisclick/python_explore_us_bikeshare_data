import time
import pandas as pd
import numpy as np
import calendar as cal
import os
import style



print_style = style.Style()


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print(print_style.WHITE)
    # Get user input for city (chicago, new york city, washington).
    city = input("Please enter one of the following cities you want to see data for:\nChicago, New York, or Washington \U0000270F\n").lower().lstrip().rstrip()
    while city not in cities:
        city = input("Please enter one of the following cities you want to see data for:\nChicago, New York, or Washington \U0000270F\n").lower().lstrip().rstrip()

    # Get user input for month (all, january, february, ... , june)
    month = input("Please enter the month you want to explore. If you do not want a month filter enter 'all'. \nChoices: All, January, February, March, April, May, June \U0000270F\n").lower().lstrip().rstrip()
    while month not in months:
        month =  input("Please enter the month you want to explore. If you do not want a month filter enter 'all'. \nChoices: All, January, February, March, April, May, June \U0000270F\n").lower().lstrip().rstrip()

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter the day of the week you want to explore. If you do not want to apply a month filter enter 'all'. \nChoices: All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday \U0000270F\n").lower()
    while day not in days:
        day =  input("Please enter the day of the week you want to explore. If you do not want to apply a month filter enter 'all'. \nChoices: All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday \U0000270F\n").lower()


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.

     Args:
         (dataframe) df - Pandas DataFrame containing city data filtered by month and day
    """

    print(print_style.GREEN,'\nCalculating The Most Frequent Times of Travel...','\U0000231B')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['month'].mode()[0]
    most_common_month_name = cal.month_name[most_common_month]
    print(print_style.WHITE)
    print('Most common month is: ', most_common_month_name)

    # Display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most common day of week is: ', most_common_day)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('Most common start hour of day is: ', most_common_hour)

    print("\nThis took %s seconds." % round((time.time() - start_time), 4))
    print('-'*40,)

    display_data(df)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

     Args:
         (dataframe) df - Pandas DataFrame containing city data filtered by month and day
    """

    print(print_style.GREEN,'\nCalculating The Most Popular Stations and Trip...','\U0000231B')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(print_style.WHITE)
    print('Most common start station is: ', most_common_start_station)

    # Display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most common end station is: ', most_common_end_station)

    # Display most frequent combination of start station and end station trip
    df['start end station'] = df['Start Station'] + ' and ' + df['End Station'] 
    most_frequent_start_end_station = df['start end station'].mode()[0]
    print('Most frequent combination of start station and end station trip :', most_frequent_start_end_station)

    print("\nThis took %s seconds." %  round((time.time() - start_time),4))
    print('-'*40)

    display_data(df)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

     Args:
         (dataframe) df - Pandas DataFrame containing city data filtered by month and day
    """

    print(print_style.GREEN,'\nCalculating Trip Duration...', '\U0000231B')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(print_style.WHITE)
    print('Total travel time: ', round(total_travel_time/3600.0, 2), ' hours')

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time: ', round(mean_travel_time/60,2), ' minutes')

    print("\nThis took %s seconds." %  round((time.time() - start_time),4))
    print('-'*40)

    display_data(df)


def user_stats(df, city):
    """Displays statistics on bikeshare users.

     Args:
         (dataframe) df - Pandas DataFrame containing city data filtered by month and day
         (str) city - name of the city to analyze
    """

    print(print_style.GREEN,'\nCalculating User Stats...','\U0000231B')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(print_style.WHITE)
    print('Counts of user types:')
    print(user_types.to_string(), '\n')

    # 'Gender' and 'Birth Year' is only available for Chicago and New York City
    # Display counts of gender
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print('Counts of gender:')
        print(user_gender.to_string(), '\n')
    else:
        print('Sorry, no gender data available for {} City'.format(city.title()))
   
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        print('Earliest year is: ',int(earliest_year))

        most_recent_year = df['Birth Year'].max()
        print('Most recent year is: ',int(most_recent_year))

        most_common_year = df['Birth Year'].mode()[0]
        print('Most common year is: ',int(most_common_year))
    else:
        print('Sorry, no birth year data available for {} City'.format(city.title()))

    print("\nThis took %s seconds." %  round((time.time() - start_time),4))
    print('-'*40)

    display_data(df)

def display_data(df):
    """Displays data if the user wants it and if the user wants continue watching more rows of the dataframe

     Args:
         (dataframe) df - Pandas DataFrame containing city data filtered by month and day
    """

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no \U0000270F\n').lower().lstrip().rstrip()

    if view_data != 'yes':
        return
    
    start_loc = 0
    while (True):
        print(df.iloc[start_loc:start_loc + 5])

        start_loc += 5
        if start_loc > len(df.index):
            break

        view_data = input('Do you wish to continue? Enter yes or no \U0000270F\n ').lower().lstrip().rstrip()
        if view_data != 'yes':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart \U0001F603\U0001F6B2? Enter yes or no \U0000270F\n').lower().lstrip().rstrip()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
