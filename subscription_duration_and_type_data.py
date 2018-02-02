'''The following script uses subscription data from 'subscription_report.csv' to
determine the subscription type and duration for each registered subscription
from Jan-1966 to Dec-2014.

Subscription data is grouped according to subscription id, and the subscription
type and duration are evaluated based on the transaction dates recorded for each
unique subscription id.  Subscription duration is reported based on the subscription
type (i.e. years for yearly subscriptions, months for monthly subscripion, and days
for daily subscripions)'''


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


def transactions_by_id():
    '''Return dictionary of subscription transaction dates for each id in data file.'''

    # call read_data function to read all the transaction data
    transaction_data = read_data("subscription_report.csv")

    # initialize an empty dictionary to store inidividual subscriber transaction data
    subscription_transactions_by_id = {}

    # store the date of every transaction recorded for each subscriber
    for index in range(len(transaction_data[3])):
        # the dictionary creates a key using subscription_id
        subscription_id = transaction_data[1][index]
        # store transaction date(s) for each subscriber by their subscription_id
        subscription_transaction_date = transaction_data[3][index]
        subscription_transactions_by_id.setdefault(subscription_id, []).append(subscription_transaction_date)

    return subscription_transactions_by_id


def type_and_duration_by_id():
    '''Return subscription type and duration for each subscription id'''

    # load dictionary of subscription transactions for each subscripion id
    subscription_transactions_by_id = transactions_by_id()
    print subscription_transactions_by_id

    # initialize empty dictionaries for storing subscription type and duration
    subscription_type_by_id = {}
    subscription_duration_by_id = {}

    # loop through each subscription_id to evaluate type and duration based on transaction dates
    for key in subscription_transactions_by_id:
        # check for subscription type 'one-off'
        # -- this type should have only one transaction
        # -- set duration to 1 day for type 'one-off'
        if len(subscription_transactions_by_id[key]) == 1:
            subscription_type = 'one-off'
            subscription_duration = 1
    	# check for other subscription types
        else:
            # determine transaction year for first and second transactions
            transaction_year_one = subscription_transactions_by_id[key][0][6:10]
            transaction_year_two = subscription_transactions_by_id[key][1][6:10]

            # determine transaction month for first and second transactions
            transaction_month_one = subscription_transactions_by_id[key][0][0:2]
            transaction_month_two = subscription_transactions_by_id[key][1][0:2]

            # check for transaction type 'yearly'
    		# -- this type should contain consective transaction dates with different year values
    		# -- set duration to the number of years between the first and last recorded transactions
            if transaction_year_one != transaction_year_two:
                subscription_type = 'yearly'
                subscription_duration = len(subscription_transactions_by_id[key])
    		# check for transaction type 'monthly'
    		# -- this type should contain consective transaction dates with different month values
    		# -- set duration to the number of months between the first and last recorded transactions
            elif transaction_month_one != transaction_month_two:
                subscription_type = 'monthly'
                subscription_duration = len(subscription_transactions_by_id[key])
            # check for transaction type 'daily'
            # -- return type 'daily' if conditions for the other types are not met
            # -- set duration to the number of days between the first and last recorded transactions
            else:
                subscription_type = 'daily'
                subscription_duration = len(subscription_transactions_by_id[key])

        subscription_type_by_id[key] = subscription_type
        subscription_duration_by_id[key] = subscription_duration

    return subscription_type_by_id, subscription_duration_by_id

#Execute
if __name__ == "__main__":
    type_and_duration_by_id()
