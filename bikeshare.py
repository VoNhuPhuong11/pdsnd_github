import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

city_list = ['chicago', 'new york city', 'washington']
month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_valid_input(prompt, valid_options):
    """
    Prompts the user for input and ensures it's within a list of valid options.

    Args:
        prompt (str): The message displayed to the user to request input.
        valid_options (list): A list of valid input options.

    Returns:
        str: The user's valid input in lowercase.
    """
    while True:
            user_input = input(prompt).lower()
            if user_input in valid_options:
                return user_input
            else:
                print(f"Invalid input. Please choose from: {', '.join(valid_options)}")

def get_filters():
    """
    Prompts the user for a city, month, and day to filter bikeshare data.

    Returns:
        tuple: A tuple containing the following string values:
            * city (str): The name of the selected city.
            * month (str): The name of the selected month, or "all" for no filter.
            * day (str): The name of the selected day of the week, or "all" for no filter.
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = get_valid_input('Please enter the city name: ', city_list)
        if city in city_list:
            break
        else:
            print('Invalid city name. Please enter a valid city name.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = get_valid_input('Please enter the month name: ', month_list)
        if month in month_list:
            break
        else:
            print('Invalid month name. Please enter a valid month name.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = get_valid_input('Please enter the day name: ', day_list)
        if day in day_list:
            break
        else:
            print('Invalid day name. Please enter a valid day name.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads bikeshare data for the specified city and filters by month and day.

    Args:
        city (str): The name of the city to analyze.
        month (str): The name of the month to filter by, or "all" for no filter.
        day (str): The name of the day of the week to filter by, or "all" for no filter.

    Returns:
        pandas.DataFrame: A DataFrame containing the filtered bikeshare data.
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.day_name()

    if month != 'all':
        month = month_list.index(month) + 1
        df = df[df['Month'] == month]
    
    if day != 'all':
        df = df[df['Day'] == day.title()]

    return df


def time_stats(df):
    """
    Calculates and prints statistics related to the most frequent times of travel.

    Args:
        df (pandas.DataFrame): The DataFrame containing the bikeshare data.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Month'].mode()[0]
    print('The most common month is: '.format(common_month))

    # display the most common day of week
    common_day = df['Day'].mode()[0]
    print('The most common day is: '.format(common_day))

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    print('The most common hour is: '.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Calculates and prints statistics related to the most popular stations and trip.

    Args:
        df (pandas.DataFrame): The DataFrame containing the bikeshare data.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is: '.format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common end station is: '.format(common_end_station))

    # display most frequent combination of start station and end station trip
    df['Start End Station'] = df['Start Station'] + ' to ' + df['End Station']
    common_start_end_station = df['Start End Station'].mode()[0]
    print('The most common start and end station is: '.format(common_start_end_station))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Calculates and prints statistics related to the total and average trip duration.

    Args:
        df (pandas.DataFrame): The DataFrame containing the bikeshare data.
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is: '.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is: '.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Calculates and prints statistics related to bikeshare users.

    Args:
        df (pandas.DataFrame): The DataFrame containing the bikeshare data.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print('The counts of user types are: '.format(user_counts))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('These are the counts of gender: \n'.format(gender_counts))
    else:
        print('There is no gender data available for this city.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        print('The earliest birth year is: '.format(earliest_birth_year))

        most_recent_birth_year = df['Birth Year'].max()
        print('The most recent birth year is: '.format(most_recent_birth_year))

        common_birth_year = df['Birth Year'].mode()[0]
        print('The most common birth year is: '.format(common_birth_year))
    else:
        print('There is no birth year data available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df, start_loc=0):
    """
    Displays 5 rows of data and prompts the user if they want to see more.

    Args:
        df (pandas.DataFrame): The DataFrame containing the bikeshare data.
        start_loc (int, optional): The starting row to display. Defaults to 0.
    """
    end_loc = start_loc + 5
    show_more = input("Do you want to see the next 5 rows of data? (yes/no): ")

    while show_more.lower() == 'yes':
        print(df.iloc[start_loc:end_loc])
        start_loc = end_loc 
        end_loc += 5

        if end_loc > len(df): 
            print("No more data to display.")
            break

        show_more = input("Do you want to see the next 5 rows of data? (yes/no): ")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()