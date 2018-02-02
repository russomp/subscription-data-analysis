'''The following script uses subscription data from 'subscription_report.csv' to
determine the annual revenue for each year between 1966 and 2014.

Subscription data is grouped according to transaction year, and the amount of
each transaction in a given year are summed to compute the annual revenue.'''

import matplotlib.pyplot as plt

def read_data(filename):
    '''Return all data values from read file.'''

    try:
        # try to open data file
        data_file = open(filename, "r")

        # read the file headers
        header = data_file.readline().split(",")

        # initialize a set of empty lists for storing all transaction data
        data_values = []
        for index in range(len(header)):
            data_values.append([])

        # loop through each line in the data file and store each data value
        for lines in data_file:
            # split the line data into a list of values
            line = lines.split(",")
            # loop through list of values and reach each data entry
            for index in range(len(header)):
                data_values[index].append(line[index])

        # return all data values as a set of lists
        return data_values

    except IOError:
        print "Error processing file."
        exit()

    finally:
        data_file.close()


def annual_revenue():
    '''Return dictionary of total revenues for each year in data file.'''

    # call read_data function to read all the transaction data
    transaction_data = read_data("subscription_report.csv")

    # initialize an empty dictionary to store subscription data
    transaction_amounts_by_year = {}

    # store the date of every transaction amount recorded for each year
    for index in range(len(transaction_data[3])):
        # the dictionary creates a key using transaction year
        transaction_year = int(transaction_data[3][index][6:10])
        # store transaction amount(s) for each transaction by transaction year
        subscription_amount = int(transaction_data[2][index])
        transaction_amounts_by_year.setdefault(transaction_year, []).append(subscription_amount)

    # initialize an empty dictionary to store annual revenue data
    revenue_per_year = {}

    # compute total yearly revenue and store in dictionary by year
    for key in transaction_amounts_by_year.keys():
        total_yearly_revenue = sum(transaction_amounts_by_year[key])
        revenue_per_year.setdefault(key, []).append(total_yearly_revenue)

    return revenue_per_year

def display_revenue_data():
    '''Plot annual revenue data.'''

    # store all revenue data
    revenue_data = annual_revenue()

    # create empty lists for storing years and revenues
    years = []
    revenues = []

    # sort dictionary by year, and store sorted keys and valaues in empty lists
    for key in sorted(revenue_data.keys()):
        total_yearly_revenue = sum(revenue_data[key])
        years.append(int(key))
        revenues.append(total_yearly_revenue/100000)

    plt.plot(years, revenues)
    plt.title('Subscription Annual Revenue between 1966 and 2014')
    plt.xlabel('Year')
    plt.ylabel('Annual Revenue [$100,000]')
    plt.show()

display_revenue_data()
