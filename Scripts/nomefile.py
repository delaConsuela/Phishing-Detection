import os
import csv

def main():

    with open('results.txt', 'r') as rcsv:
        content = csv.reader(rcsv)

        for row in content:
            new_row = row[1].split(",")

            renew =  new_row[0].split(']')
            row = renew[0]

            with open('AgeDomain.csv', 'a') as wcsv:
                csv_write = csv.writer(wcsv)
                csv_write.writerow(str(row))
           

    


    


if __name__ == '__main__':
    main()