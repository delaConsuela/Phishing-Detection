import csv
import requests as req
from requests.auth import HTTPBasicAuth

def Get_Page_Rank(domain):
    
    header = {
        'API-OPR': 'wow8ws8s8ogwgggkg84w8w8wkwgk8ws8ws0os004'
    }

    res = req.get(f'https://openpagerank.com/api/v1.0/getPageRank?domains%5B0%5D={domain}', headers=header)

    total_page_rank = 0

    if res.status_code == 200:

        res = res.json()

        list_response = res['response']

        for i in range(0, len(list_response)):
            if res['response'][i]['page_rank_integer'] != '':
                total_page_rank += int(res['response'][i]['page_rank_integer'])
    
    else:
        return -1


    return total_page_rank


def main():
    
    dataset = 'PGRANK_200.csv'
    results = 'Results_PageRank.txt'

    limit_req = 500
    score_pgRank = 0
    res = []

    with open(dataset, 'r') as rcsv:
        content = csv.reader(rcsv)

        for row in content:

            if limit_req == 0:
                return

            score_pgRank = Get_Page_Rank(row[2])

            res.append(row[0])
            res.append(score_pgRank)

            with open(results, 'a') as wfile:
                wfile.write(str(res) + "\n")

            limit_req -= 1

            res = []
        

if __name__ == '__main__':
    main()