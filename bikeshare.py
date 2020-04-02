import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            input_city = input("Do you want to know about Chicago, New York City, or Washington? ")
            if input_city.lower() in {'chicago', 'new york city', 'washington'}:
                city = input_city.lower()
                print("Okay, I'll tell you about {}.".format(city.title()))
                break
            print("I didn't catch that. Check your spelling, and try again.")
        except KeyboardInterrupt:
                print('No input taken.')
                break
        finally:
            print("")

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            input_month = input("Which month do you want to know about? Type 'all' to hear about all months. ")
            if input_month.lower() in {'january', 'february', 'march', 'april', 'may', 'june'}:
                month = input_month.lower()
                print("Okay, I'll tell you about {}.".format(month.title()))
                break
            elif input_month.lower() == 'all':
                month = input_month.lower()
                print("Okay, I'll tell you about all six months.")
                break
            print("I didn't catch that. Check your spelling, and try again.")
        except KeyboardInterrupt:
            print('No input taken.')
            break
        finally:
            print("")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            input_day = input("Which day(s) of the week do you want to know about? Type 'all' to hear about all days. ")
            if input_day.lower() in {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}:
                day = input_day.lower()
                print("Okay, I'll tell you about {}s in {} in {}.".format(day.title(), month.title(), city.title()))
                break
            elif input_day.lower() == 'all':
                day = input_day.lower()
                print("Okay, I'll tell you about all the days of the week.")
                break
            print("I didn't catch that. Check your spelling, and try again.")
        except KeyboardInterrupt:
            print('No input taken.')
            break
        finally:
            print("")


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
    #lookup the 'city' argument in the dictionary and use its dictionary entry as the filename to be loaded
    filename = CITY_DATA[city]

    # load data file into a dataframe
    df = pd.read_csv(filename)


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df["Start Time"].dt.month
    df['day_of_week'] = df["Start Time"].dt.weekday_name
    df['hour'] = df["Start Time"].dt.hour
    df['trip'] = 'from ' + df['Start Station'] + ' to ' +  df['End Station']


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        #have to add 1 so that january is month 1 not 0
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = 1+months.index(month)

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].value_counts().index.values[0]

    print('Most Frequent Month:', popular_month)


    # TO DO: display the most common day of week
    popular_day_of_week = df['day_of_week'].value_counts().index.values[0]

    print('Most Frequent Day of Week:', popular_day_of_week)


    # TO DO: display the most common start hour
    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].value_counts().index.values[0]

    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start = df['Start Station'].value_counts().index.values[0]
    print('Most Frequent Start Station:', popular_start)


    # TO DO: display most commonly used end station
    popular_end = df['End Station'].value_counts().index.values[0]
    print('Most Frequent End Station:', popular_end)

    # TO DO: display most frequent combination of start station and end station trip
    popular_trip = df['trip'].value_counts().index.values[0]
    print('Most Frequent Trip:', popular_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    trip_count = df.shape[0]
    print("There were a total of {} trips taken in the selected city and timeframe.".format(trip_count))
    print("\n")
    print("Total trip duration for the selected filters was {} seconds (rounded).".format(int(round(total_time, 0))))
    print("This is equivalent to {} minutes (rounded).".format(int(round(total_time / 60 , 0))))
    print("This is equivalent to {} hours (rounded).".format(int(round(total_time / (60*60) , 0))))

    # TO DO: display mean travel time
    mean_time = total_time / trip_count
    print("Mean trip duration for the selected filters was {} seconds (rounded).".format(int(round(mean_time, 0))))
    print("This is equivalent to {} minutes (rounded).".format(int(round(mean_time / 60 , 0))))
    print("This is equivalent to {} hours (rounded).".format(int(round(mean_time / (60*60) , 0))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    for i in range(len(df['Gender'].value_counts().index)):
        print(df['Gender'].value_counts().index.values[i], ":", df['Gender'].value_counts()[i])
    print("No gender provided : ", df["Gender"].isnull().sum())

    # TO DO: Display earliest, most recent, and most common year of birth
    earliest_yob = df['Birth Year'].min()
    print('Earliest Year of Birth:', int(earliest_yob))

    latest_yob = df['Birth Year'].max()
    print('Most Recent Year of Birth:', int(latest_yob))

    common_yob = df['Birth Year'].value_counts().index.values[0]
    print('Most Frequent Year of Birth:', int(common_yob))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data, N lines at a time (where N is chosen by the user), until user gives up or end of data reached"""
    input_command = input("Would you like to view the raw data? ")
    if input_command.lower() in {'yes', 'y'}:
        keep_going = 'yes'
        start_row = 0

        while keep_going not in {'no', 'n'}:
            try:
                chunksize = int(input("How many rows of data would you like to see at once? "))
                if chunksize == 0:
                    print("I can't do that!")
                elif chunksize != 0:
                    while keep_going not in {'no', 'n'}:
                        #print rows from (start_row) to (start_row+chunksize)
                        print(df.iloc[start_row:start_row+chunksize, : ])
                        #identify new starting row
                        start_row += chunksize
                        #ask again
                        keep_going = input("Keep going? ")
            except ValueError:
                print("That's not a valid number! Please enter an integer.")
    else:
           print("Okay, nevermind then!")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
