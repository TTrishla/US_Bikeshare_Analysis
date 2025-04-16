#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# In[2]:


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
    while True:
        city = input("enter name:").lower()
        if city in CITY_DATA:
            break
        else: 
            print("invalid")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter the month (all, january, february, ..., june): ").lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print("Invalid month. Please try again.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter the day of the week (all, monday, tuesday, ..., sunday): ").lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print("Invalid day. Please try again.")

    print('-'*40)
    return city, month, day


# In[3]:


def load_data(city, month, day):
    
    #load data 
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # create month and day column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    # Filter by month if needed
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months.index(month) + 1
        df = df[df['month'] == month_num]
    
    # Filter by day if needed
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df


# In[4]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
 
 # display the most common month
    common_month_num = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print(f"\nMost common month: {months[common_month_num-1].title()}")
 
 # display the most common day of week
    common_week_day = df['day_of_week'].mode()[0]
    print(f"\nMost common day: {common_week_day} ")
    
 # display the most common start hour
    common_hour_start = df['hour'].mode()[0]
    print(f"\nMost common day: {common_hour_start}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[6]:


#Main program flow
city, month, day = get_filters()
print(f"Filters selected: {city}, {month}, {day}")
df = load_data(city, month, day)
print(f"\nLoaded {len(df)} rows of filtered data")
df.head(5)
time_stats(df)


# In[8]:


df.head(5)


# In[16]:


df['Trip'] = df['Start Station'] + " to " + df['End Station']
print(f"\n {df['Trip']}")


# In[18]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    
    common_start = df['Start Station'].mode()[0]
    start_count = df['Start Station'].value_counts().max()
    print(f"\nMost common start station: {common_start} ({start_count} trips)")

    # display most commonly used end station
    
    common_end = df['End Station'].mode()[0]
    end_count = df['End Station'].value_counts().max()
    print(f"Most common end station: {common_end} ({end_count} trips)")


    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['Trip'].mode()[0]
    trip_count = df['Trip'].value_counts().max()
    print(f"Most common trip: {common_trip} ({trip_count} trips)")
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    


# In[19]:


#Main program flow
city, month, day = get_filters()
print(f"Filters selected: {city}, {month}, {day}")
df = load_data(city, month, day)
print(f"\nLoaded {len(df)} rows of filtered data")
df.head(5)
time_stats(df)
station_stats(df)


# In[20]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # Convert duration to minutes for more readable output
    total_seconds = df['Trip Duration'].sum()
    mean_seconds = df['Trip Duration'].mean()

    # Convert seconds to days, hours, minutes
    total_days = total_seconds // (24 * 3600)
    total_seconds %= (24 * 3600)
    total_hours = total_seconds // 3600
    total_seconds %= 3600
    total_mins = total_seconds // 60

    # Display total travel time
    print(f"Total travel time: {int(total_days)} days, {int(total_hours)} hours, {int(total_mins)} minutes")

    # Display mean travel time (in minutes and seconds)
    mean_mins = mean_seconds // 60
    mean_secs = mean_seconds % 60
    print(f"Average trip duration: {int(mean_mins)} minutes {int(mean_secs)} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[22]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # 1. Display counts of user types
    print("\nUser Type Breakdown:")
    print(df['User Type'].value_counts().to_string())

    # 2. Display counts of gender (if column exists)
    if 'Gender' in df.columns:
        print("\nGender Breakdown:")
        print(df['Gender'].value_counts().to_string())
    else:
        print("\nGender data not available for this city")

    # 3. Display birth year stats (if column exists)
    if 'Birth Year' in df.columns:
        print("\nBirth Year Statistics:")
        print(f"Earliest: {int(df['Birth Year'].min())}")
        print(f"Most recent: {int(df['Birth Year'].max())}")
        print(f"Most common: {int(df['Birth Year'].mode()[0])}")
    else:
        print("\nBirth year data not available for this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[23]:


#Main program flow
city, month, day = get_filters()
print(f"Filters selected: {city}, {month}, {day}")
df = load_data(city, month, day)
print(f"\nLoaded {len(df)} rows of filtered data")
df.head(5)
time_stats(df)
station_stats(df)
trip_duration_stats(df)
user_stats(df)


# In[ ]:




