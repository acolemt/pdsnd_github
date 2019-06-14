import time
import pandas as pd
import numpy as np
import pprint

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    input_city = ""
    input_time_filter = ""
    input_month = "all"
    input_day = "all"
    dir_month = {'jan':'january','feb':'february','mar':'march','apr':'april','may':'may','jun':'june', 'all':'all'}
    dir_day = {'m':'Monday','tu':'Tuesday','w':'Wednesday','th':'Thursday','f':'Friday','sa':'Saturday', 'su':'Sunday', 'all':'all'}

    while input_city == "":
        input_city = input("Would you like to see data for Chicago, New York or Washington?\n")
        try:
            input_city = input_city.lower()
            if input_city in ['chicago','new york','washington']:
                break
            else:
                print("\nPlease enter a valid city.")
                input_city = ""
        except ValueError:
            print("\nPlease enter a valid city.")
            input_city = ""

    # get user input for month (all, january, february, ... , june)
    while input_time_filter == "":
        input_time_filter = input("Would you like to filter by month, day, both or not at all? Type \"none\" for no filter\n")
        try:
            input_time_filter = input_time_filter.lower()
            if input_time_filter in ['month','day','both','none']:
                break
            else:
                print("\nPlease enter a valid filter option.")
                input_time_filter = ""
        except ValueError:
            print("\nPlease enter a valid filter option.")
            input_time_filter = ""
            
    if input_time_filter == "month" or input_time_filter == "both":
        while input_month == "all":
            input_month = input("Which month? Jan, Feb, Mar, Apr, May, Jun, All\n")
            try:
                input_month = input_month.lower()
                if input_month in dir_month.keys():
                    input_month = dir_month[str(input_month)]
                    break
                else:
                    print("\nPlease enter a valid Month.")
                    input_month = ""
            except ValueError:
                print("\nPlease enter a valid Month.")
                input_month = ""

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if input_time_filter == "day" or input_time_filter == "both":
        while input_day == "all":
            input_day = input("Which day? M, Tu, W, Th, F, Sa, Su, All\n")
            try:
                input_day = input_day.lower()
                if input_day in dir_day.keys():
                    input_day = dir_day[str(input_day)]
                    break
                else:
                    print("\nPlease enter a valid choice.")
                    input_day = ""
            except ValueError:
                print("\nPlease enter a valid choice.")
                input_day = ""

    print('-'*40)
    return input_city, input_month, input_day


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #df['Trip Duration'] = pd.to_timedelta(df['Trip Duration'], unit='s')

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    months = ['january', 'february', 'march', 'april', 'may', 'june']

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("\nMost travelled month\n", months[df['month'].mode()[0] - 1].title())

    # display the most common day of week
    print("\nMost travelled day of week\n", df['day_of_week'].mode()[0].title())

    # display the most common start hour
    t = time.strptime(str(df['hour'].mode()[0]) + ':00', "%H:%M")
    timevalue_12hour = time.strftime("%I %p", t)

    print("\nMost travelled hour\n", timevalue_12hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    input('\nPress enter to continue')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("\nMost travelled start station\n", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("\nMost travelled end station\n", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print("\nMost frequent trip from start to end")
    grouped_sorted = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    maxcount = grouped_sorted[0]
    print(grouped_sorted.loc[grouped_sorted == maxcount])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    input('\nPress enter to continue')

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    seconds = df['Trip Duration'].sum()
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    str_total_duration=''
    print('\nTotal Travel Time')
    if weeks > 0:
        str_total_duration = '{} Weeks '.format(int(weeks))
    if days > 0:
        str_total_duration += '{} Days '.format(int(days))
    if hours > 0:
        str_total_duration += '{} Hours '.format(int(hours))
    if minutes > 0:
        str_total_duration += '{} Minutes '.format(int(minutes))
    if seconds > 0:
        str_total_duration += '{} Seconds'. format(round(seconds,2))

    print(str_total_duration)

    # display mean travel time
    seconds = df['Trip Duration'].mean()
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    str_avg_duration = ''    
    print('\nAverage Travel Time')
    if hours > 0:
        str_avg_duration = '{} Hours '.format(int(hours))
    if minutes > 0:
        str_avg_duration += '{} Minutes '.format(int(minutes))
    if seconds > 0:
        str_avg_duration += '{} Seconds'. format(round(seconds,2))

    print(str_avg_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    input('\nPress enter to continue')


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nUser Type Breakdown')
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('\nGender Breakdown')
        print(gender)
    else:
        print('\nNo gender data to share\n')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_dob = int(df['Birth Year'].min())
        recent_dob = int(df['Birth Year'].max())
        common_dob = int(df['Birth Year'].mode()[0])

        print('\nOldest year of birth')
        print(earliest_dob)
        print('\nYoungest year of birth')
        print(recent_dob)
        print('\nMost popular year of birth')
        print(common_dob)
    else:
        print('\nNo birth year data to share\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_rawdata(dict_data):
    """Displays bikeshare data in 5 row increments
        Input: 
            Data as a dictionary 
        
        Used a dicitonary so we can print the column values with each row.
        used pprint to display data in a user friendly way
    """

    continue_rawdata = 'yes'
    current_line = 0
    print_count = 1
    pprint.sorted = lambda x, key=None: x

    while continue_rawdata == 'yes':
        while print_count <= 5:
            pprint.pprint(dict_data[current_line])
            print('')
            current_line += 1
            print_count += 1
        
        print_count = 1
        continue_rawdata = ''
        while continue_rawdata == '':
            try:
                continue_rawdata = input('\nWould you like to view individial trip data? Enter yes or no\n')
                if continue_rawdata.lower() in ['yes','no']:
                    break
                else:
                    print('\nPlease enter either yes or no')
                    continue_rawdata = ''

            except ValueError:
                print('\nPlease enter either yes or no\n')
                continue_rawdata = ''


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        rawdata = ''
        while rawdata == '':
            try:
                rawdata = input('\nWould you like to view individial trip data? Enter yes or no\n')
                if rawdata.lower() == 'yes':
                    print('Formatting individual trip data...')
                    df = df.drop(['month','day_of_week','hour'], axis = 1)
                    dict_data = df.to_dict('index')
                    display_rawdata(dict_data)
                elif rawdata.lower() == 'no':
                    break
                else:
                    print('\nPlease enter either yes or no')
                    rawdata = ''
            except ValueError:
                print('\nPlease enter either yes or no\n')
                rawdata = ''

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
