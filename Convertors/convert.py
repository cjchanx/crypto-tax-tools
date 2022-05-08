# Python script to convert
import argparse
import time
import csv

exchange_to_id = {
    "blockfi" : 0,
    "celcius" : 1
}

def main(args):
    print('#\tPreparing conversion...')
    #convert_and_output(exchange_to_id.get(args.Exchange.lower()), args.file)
    convert_and_output(100, args.file)

def convert_and_output(exch_id, filepath):
    print(f'#\tConverting input file <{filepath}>')
    conversion_start_time = time.perf_counter()

    # Read file
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    header = data[0]


    errored_rows = []
    output_data = [['Date', 'Type', 'Received Currency', 'Received Amount', 'Received Net Worth', 'Sent Currency', 'Sent Amount',
      'Sent Net Worth', 'Fee Currency', 'Fee Amount', 'Fee Net Worth']]
    print(header)

    # Convert
    if(header == ['Cryptocurrency', 'Amount', 'Transaction Type', 'Confirmed At']): # BLOCKFI
        for i in range(1, len(data)):
            row = data[i]

            # BlockFi Data
            confirmed_at = row[3]
            transaction_type = row[2]
            amount = row[1]
            cryptocurrency = row[0]

            # CDC data
            date = ''
            type = ''
            received_curr = ''
            received_amount = ''
            received_net_worth = ''
            sent_currency = ''
            sent_amount = ''
            sent_net_worth = ''
            fee_currency = ''
            fee_amount = ''
            fee_net_worth = ''


            # Convert and interpret
            date = confirmed_at
            type = f"NOT-RECOGNIZED : {transaction_type}"
            if(transaction_type == "Interest Payment"):
                type = "reward"
                received_curr = cryptocurrency
                received_amount = amount
            elif(transaction_type == "BIA Withdraw"):
                continue # These are internal BlockFi transactions between BIA and BlockFi Wallet - Skip
            elif(transaction_type == "BIA Deposit"):
                continue # These are internal BlockFi transactions between BIA and BlockFi Wallet - Skip
            elif(transaction_type == "Crypto Transfer"):
                type = "mining" # Default type assumed to be mining TODO: Make this configurable
                received_curr = cryptocurrency
                received_amount = amount
            elif(transaction_type == "Withdrawal"):
                type = "transfer" # Default type assumed to be transferred TODO: Mark transacs as unknown sender if doesn't match another transac
                received_curr = cryptocurrency
                sent_currency = cryptocurrency
                received_amount = str(-float(amount))
                sent_amount = str(-float(amount))
                fee_amount = ""     # BlockFi fees are different rows
                fee_currency = ""   # BlockFi fees are different rows
            elif(transaction_type == "Withdrawal Fee"):
                type = "cost"
                sent_currency = cryptocurrency
                sent_amount = str(-float(amount))
            elif(transaction_type == "Bonus Payment"):
                type = "reward"
                received_curr = cryptocurrency
                received_amount = amount
            else:
                errored_rows.append(i)

            write_row = [date, type, received_curr, received_amount, received_net_worth, sent_currency, sent_amount, sent_net_worth, fee_currency, fee_amount, fee_net_worth]
            print(write_row)
            output_data.append(write_row)
    elif(header == ['Internal id', ' Date and time', ' Transaction type', ' Coin type', ' Coin amount', ' USD Value', ' Original Reward Coin', ' Reward Amount In Original Coin', ' Confirmed']): # CELCIUS
        for i in range(1, len(data)):
            row = data[i]

            # Celcius Data (important)
            cel_date = row[1]
            transaction_type = row[2]
            amount = row[4]
            cryptocurrency = row[3]

            # Convert necessary data
            from datetime import datetime
            cel_dt_object = datetime.strptime(cel_date, '%B %d, %Y %I:%M %p')
            cel_date = cel_dt_object.strftime("%m/%d/%Y %H:%M:%S")


            # CDC data
            date = ''
            type = ''
            received_curr = ''
            received_amount = ''
            received_net_worth = ''
            sent_currency = ''
            sent_amount = ''
            sent_net_worth = ''
            fee_currency = ''
            fee_amount = ''
            fee_net_worth = ''


            # Convert and interpret
            date = cel_date
            type = f"NOT-RECOGNIZED : {transaction_type}"
            if(transaction_type == "Reward"):
                type = "reward"
                received_curr = cryptocurrency
                received_amount = amount
            elif(transaction_type == "Referrer Award"):
                type = "reward"
                received_curr = cryptocurrency
                received_amount = amount
            elif(transaction_type == "Withdrawal"):
                type = "transfer" # Default type assumed to be transferred TODO: Mark transacs as unknown sent-to if doesn't match another transac
                received_curr = cryptocurrency
                sent_currency = cryptocurrency
                received_amount = str(-float(amount))
                sent_amount = str(-float(amount))
                fee_amount = ""
                fee_currency = ""
            elif(transaction_type == "Transfer"):
                type = "transfer" # Default type assumed to be transferred TODO: Mark transacs as unknown sender if doesn't match another transac
                received_curr = cryptocurrency
                sent_currency = cryptocurrency
                received_amount = amount
                sent_amount = amount
                fee_amount = ""
                fee_currency = ""
            elif(transaction_type == "Promo Code Reward"):
                type = "reward"
                received_curr = cryptocurrency
                received_amount = amount
            else:
                errored_rows.append(i)

            write_row = [date, type, received_curr, received_amount, received_net_worth, sent_currency, sent_amount, sent_net_worth, fee_currency, fee_amount, fee_net_worth]
            print(write_row)
            output_data.append(write_row)


    if(len(errored_rows) > 0):
        print(f'#\tERRORED ROWS: {errored_rows}')

    # Output to file
    print(f'#\tConversion took {(time.perf_counter()-conversion_start_time)*1000} ms')
    with open("output.csv", "w", newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        for row in range(0,len(output_data)):
            writer.writerow(output_data[row])

# Main function
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Conversion from provided exchange field to "
                                                 "tax.crypto.com CSV format as specified "
                                                 "here https://help.crypto.com/en/articles/5019792-data-import")
    #parser.add_argument("Exchange", help="Required exchange definition.")  Currently not being used, detection by the file header
    parser.add_argument("-f", "--file", "--path", default="data.csv",
                        help="Optional file path argument. Default reads data.csv")
    parser.add_argument("-o", "--output", "-ofile", default="output.csv",
                        help="Optional file path argument. Default outputs to output.csv")
    args = parser.parse_args()
    main(args)
