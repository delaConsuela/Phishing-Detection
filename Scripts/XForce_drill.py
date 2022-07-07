import csv
import requests as req
from requests.auth import HTTPBasicAuth
import datetime

from Feature_Extraction import XForce_Reputation_domain


def Age_Of_Domain_2(domain):
    date = datetime.datetime.now()

    year_now = str(date.year)
    month_now = str(date.month)

    key = '055b108a-9ffc-4596-91e9-51debe316197'
    password = 'f4053e26-b414-495b-8c32-3153233bdca3'

    header = {
        'accept': 'application/json',
        'Authorization': 'Basic Og=='
    }

    res = req.get(f'https://api.xforce.ibmcloud.com/whois/{domain}', 
    headers = header, auth=HTTPBasicAuth(key, password))

    res_conv = res.json()

    if 'error' in res_conv.keys():
        return -1

    elif 'createdDate' in res_conv.keys():

            date = str(res_conv['createdDate']).split('-')

            if res_conv['createdDate'] == None:
                return -1

            elif year_now == date[0]:
                month = int(month_now) - int(date[1])

                if month in range(0, 6):
                    return 1

    return 0



def main():
    
    dataset = 'dataset2.csv'
    results = 'results.txt'

    limit_req = 400
    isJustCreated = 0
    res = []

    with open(dataset, 'r') as rcsv:
        content = csv.reader(rcsv)

        for row in content:

            if limit_req == 0:
                return

            isJustCreated = Age_Of_Domain_2(row[2])
            
            res.append(row[0])
            res.append(isJustCreated)

            with open(results, 'a') as wfile:
                wfile.write(str(res) + "\n")

            limit_req -= 1

            res = []
        

if __name__ == '__main__':
    main()