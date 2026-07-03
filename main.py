import csv

"""
Read Data from csv file
"""

def readMessagesFromCSVFile(filename):

    try:

        with open(filename) as file:

            rows = csv.reader(file)

            messages = list()
            for row in rows:
                messages.append(row[0])

        return messages


        

    except FileNotFoundError as e:
        print(e)



def main():

    API_KEY = "?"

    messages = readMessagesFromCSVFile("input_data.csv")

if __name__ == "__main__":
    main()
