import requests as req
import csv

def VT_Reputation_domain(domain):
    """
        curl --request GET --url https://www.virustotal.com/api/v3/domains/{domain} --header 'x-apikey: <your API key>'
    """

    header = {
        'x-apikey': '12e138dc562ddf2e485b3c45db338299da3e4bf974f3d17997fac382b51f296c'
    }

    res = req.get(f'https://www.virustotal.com/api/v3/domains/{domain}', headers=header)

    if res.status_code == 200:

        res_conv = res.json()

        mal = res_conv['data']['attributes']['last_analysis_stats']['malicious']
        sus = res_conv['data']['attributes']['last_analysis_stats']['suspicious']
    
        risk_score = mal + sus

    else:
        return -1

    return risk_score


def main():
    """
    1237 - phishing
    1198 - legit

    2435 - tot

    Alex        [0, 399]
    Ciccio      [400 - 799]
    Bruno       [800 - 1199]
    x           [1200 - 1599]
    y           [1600 - 1999]
    z           [2000 - 2399]
    last        [2400 - 2435]

    """

    dataset = 'dataset.csv'
    results = 'results.txt'

    limit_req = 400
    reputation_score = 0
    res = []

    with open(dataset, 'r') as rcsv:
        content = csv.reader(rcsv)

        for row in content:

            if limit_req == 0:
                return

            reputation_score = VT_Reputation_domain(row[2])

            res.append(row[0])
            res.append(reputation_score)

            with open(results, 'w') as wfile:
                wfile.write(str(res) + "\n")

            limit_req -= 1
        

if __name__ == '__main__':
    main()