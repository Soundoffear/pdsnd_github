import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

week_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

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
    city = input("Enter City Name (Chicago, New York City, Washington): ").lower()
    while city not in CITY_DATA:
        restart = input('\nWrong City name. Avaliable names: Chicago, New York City, Washington. \n Would you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        city = input("Enter City Name: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Enter Month (January, February, March, April, May, June, all): ").lower()
    while month not in months:
        restart = input('\nWrong month name. Avaliable months: January, February, March, April, May, June or all. \n Would you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        month = input("Enter Month (January, February, March, April, May, June, all): ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter Day (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, all): ").lower()
    while day not in week_days:
        restart = input('\nWrong day name. Avaliable days: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. \n Would you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        day = input("Enter Day (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, all): ").lower()

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
    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def most_common(df, column_name):
    return df.groupby(column_name)[column_name].count().sort_values(ascending=False).idxmax()


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = most_common(df,'month')
    print("Most common month to rent bike: " + str(most_common_month))

    # display the most common day of week
    most_common_day = most_common(df, 'day_of_week')
    print("Most common day to rent bike: " + str(most_common_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = most_common(df, 'hour')
    print("Most common hour to rent bike: " + str(most_common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used start start: " + str(most_common(df, 'Start Station')))

    # display most commonly used end station
    print("Most commonly used end station: " + str(most_common(df, 'End Station')))

    # display most frequent combination of start station and end station trip
    most_common_start_end = df.groupby(["Start Station", "End Station"]).size().nlargest(1)
    print("Most common combination of start and stop station is: ", most_common_start_end.idxmax()[0], " & ", most_common_start_end.idxmax()[1])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time: " + str(df["Trip Duration"].sum()))

    # display mean travel time
    print("Average travel time: " + str(round(df["Trip Duration"].mean(), 2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    types = df.groupby("User Type")['User Type'].count()
    print("Count of users based on user types: ")
    for i, type_i in enumerate(types):
        print(types.index[i], " - ", type_i)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df.groupby("Gender")["Gender"].count()
        print("Count of users based on user gender: ")
        for i, gen_i in enumerate(gender):
            print(gender.index[i], " - ", gen_i)
    else:
        print("No data for Gender in {}.".format('Washington'))

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest = df["Birth Year"].min()
        print("The earliest user birth date: " + str(int(earliest)))
        youngest = df["Birth Year"].max()
        print("The most recent user birth date: " + str(int(youngest)))
        common = most_common(df, "Birth Year")
        print("The most common user birth date: " + str(int(common)))
    else:
        print("No data for Birth Year in {}.".format("Washington"))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        print(df.head())

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        raw_display = input("Would you like to see raw data? Enter yes or no. \n")
        if raw_display == 'yes':
            start_idx = 0
            end_idx = 10
            row_count = len(df.index)
            while end_idx < row_count and raw_display == 'yes':
                print(df[start_idx:end_idx])
                start_idx += 10
                end_idx += 10
                raw_display = input("Would you like to see more data? Enter yes or no. \n")
        else:
            pass

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
                

if __name__ == "__main__":
	main()
