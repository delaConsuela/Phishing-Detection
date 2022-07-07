import os
import csv
from urllib.parse import urlparse

# 791 tolto le ""


def main():


    # with open('phish_id.txt', 'r') as rfile:
    #     content = rfile.read()
    
    # for i in var:
    #     if str(i) in content:
    #         content = content.replace(str(i),'')
    
    # with open('new_phihs_id.txt', 'w') as wfile:
    #     wfile.write(content)


    with open('legittimissimi.csv', 'r') as rfile:
        spawn_reader = csv.reader(rfile)

        count = 5000

        for url in spawn_reader:
            if isinstance(url, list):

                print(f"{count},{url[0]},{urlparse(url[0]).netloc}")

            count += 1

    # domains = content.split('\n')

    # for sing_dom in domains:


    #     print(sing_dom)

        

    
        

    
        

if __name__ == '__main__':
    main()