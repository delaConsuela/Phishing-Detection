import json
import requests as req # usato per scaricare il codice sorgente
import hashlib as hash # per calcolare l'hash
from bs4 import BeautifulSoup # per parsare la struttura l'html
import re
from urllib.parse import urlparse
import csv
import pandas as pd
import os

"""
    Fare richiesta sull'url malevolo per capire se è possibile contattarlo e poi metterlo all'interno del csv
"""

############ ALGORITMO 1 ############

def Get_data():
    """
        Opening the file and extracts info and put in a csv file
    """

    filename_json = 'phish_tank.json'
    filename = 'new_phish_id.txt'
    vect_ret = []

    with open(filename_json, encoding='UTF-8') as jfile:
        data = json.loads(jfile.read())
        # length = len(data)
        # Get_data_from_json(data)

    with open(filename, encoding='UTF-8') as rfile:
        content = rfile.read()

    element = content.split('\n')

    for i in element:

        # print(i)
        # print(data[int(i)]['url'])
        # print(urlparse(data[int(i)]['url']).netloc)

        vect_ret.append(str(i))
        vect_ret.append(data[int(i)]['url'])
        vect_ret.append(urlparse(data[int(i)]['url']).netloc)

        with open('phish_details.csv', 'a', encoding='UTF-8', newline='') as afile:

            spawnwriter = csv.writer(afile)
            spawnwriter.writerow(vect_ret)
            vect_ret = []



def Get_data_from_json(data, length = 5000):
    """
        Prints phish id, url and ip and returns the arry of urls
    """
    filename = 'phish_tank.csv'
    header = ["phish_id", "url", "domain", "ip_address", "target"]
    element_up = []

    for element in range(500, length):
        if element == 297 or element == 4706:
                continue

        try:
            
            print(f"element: {element}")
            res = req.get(data[element]['url'])

            if res.status_code == 200:
                # print(f"URL {data[element]['url']} - {res}")           
                # write_csv_phish(data, element, csvfile, spamwriter)
                element_up.append(element)
                    
        except Exception as e:
            print(e)
            continue

    with open(filename, 'w', encoding='UTF-8', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(header)

        for i in element_up:
            write_csv_phish(data, i, csvfile, spamwriter)

def write_csv_phish(data, element, csvfile, spamwriter):
    ip = ""
    single_row = []

    print("\nwriting on csv phish file\n")

    if data[element]['verified'] == 'yes' and data[element]['online'] == 'yes':

        for i in range(0, len(data[element]['details'])):
            ip = data[element]['details'][i]['ip_address']

            single_row.append(data[element]['phish_id'])
            single_row.append(data[element]['url'])
            single_row.append(urlparse(data[element]['url']).netloc)
            single_row.append(ip)
            single_row.append(data[element]['target'])
            
            spamwriter.writerow(single_row)
            csvfile.flush()

def Get_online_page():
    """
        Calculate the hash of the source code of a webpage
    """

    filename = 'phish_tank.json'
    element_up = []

    with open(filename, encoding='UTF-8') as jfile:
        data = json.loads(jfile.read())
        length = 5000

    for element in range(1300, length):
        if element == 586 or element == 4706:
                continue

        try:
            
            print(f"element: {element}")
            res = req.get(data[element]['url'])

            if res.status_code == 200:
                element_up.append(element)

        except Exception as e:
            print(e)
            continue

    with open('note.txt', 'w') as file:
        for line in element_up:
            file.write(str(line) + "\n")


def Save_page():

    # notes = 'note.txt'
    # filename = 'phish_tank.json'

    # with open(notes, "r") as file:
    #     element = file.read()

    # with open(filename, encoding='UTF-8') as jfile:
    #     data = json.loads(jfile.read())
        
    # elem =  element.split('\n')


    with open('legittimissimi.csv', encoding='UTF-8') as rcsv:
        csv_reader = csv.reader(rcsv)

        for i in csv_reader:

            print(f"{i} - {i[0]}")
    
    # for i in elem:
    #     if i != '\n':

            domain =  urlparse(i[0]).netloc

            try:
            
                res = req.get(i[0])
                os.chdir('./PagineLecite')
                new_filename = 'lecite_' + f'{domain}_.html'

                with open(new_filename, "w", encoding='UTF-8') as wfile:
                    wfile.write(str(res.text))

                Modify_HTML(new_filename)

            except Exception as e:
                print(e)
                continue



            # with open('hashes.txt', 'a', encoding='UTF-8') as hfile:
            #     hash = Modify_HTML(new_filename)
            #     hfile.write(f"{hash}\n")

def Modify_HTML(filename):
    """
        1) We first remove all spaces in the HTML.
        2) We also remove all default values in HTML input fields and replace them with empty strings.
        3) We then compute a SHA1 hash on the processed HTML, which is then compared against a pool of hash values of known phishing web pages. 
           Currently, we use PhishTank’s verified blacklist as our known list of phishing sites.
    """

    space = ' '
    
    with open(filename, encoding='UTF-8') as in_file:
        html_text = in_file.read()
        soup = BeautifulSoup(html_text,'html.parser')

    # TASK 1 - remove all spaces
    soup.get_text("|", strip=True)

    # TASK 2 - replace all value in inputs with an empty string
    all_inputs = soup.find_all('input')
        
    if all_inputs:
        for index_element in range(0, len(all_inputs)):
            attributes = all_inputs[index_element].attrs

            if attributes:
                for single_attr in attributes:
                    all_inputs[index_element][single_attr] = ''
            
    with open(filename, "w", encoding='UTF-8') as out_file:
        out_file.write(str(soup))

    # sha1_body = hash.sha1(str(soup).encode())
    # html_sha1 = sha1_body.hexdigest()

    os.chdir('..')

    # return html_sha1
        
def isContained(hash):
    """
        Returns true if the hash is contained in the DB of known phish hashes
    """
    print("Checking if the hash is contained")


############ QUA ALGORITMO 2 ############

"""
    if the elements contains the attribute class, it creates a list
    need to iterate the list to find the value
"""

def opt_keyword_locally(elements, keywords):
    """
        Takes all attribute of an elements and checks if contains a keyword
    """
    for index_element in range(0, len(elements)):
        for val in elements[index_element].attrs.values(): # for each input take all attributes (dictionary)
            if isinstance(val, list):
                for i in range(0, len(val)):
                    if val[i] in keywords:
                        return True

            elif val in keywords:
                return True

    return False

def isSerchForm(single_form):
    """
        Checks if the form is search form
    """
    keyword = 'search'
    for attribute in single_form.attrs.values():
        if attribute == 'search':
            return True

    return False

def seach_K_up(single_form, keywords):
    """
        Goes 2 levels up the tree and look for keyword
            1) exists
            2) not html or body
        problem: I wanted to re-use opt_keyword_locally() method
        Though by using .parent.parent the returned element is not a dictionary
        So, before calling the same function, I needed to call the find_all() function
    """    
    grand_parent = single_form.parent.parent
    if isSerchForm(grand_parent) is False:
        elements = grand_parent.find_all()
        if opt_keyword_locally(elements, keywords):
            return True

    return False

def isOnlyImages(single_elem, keywords):
    """ 
        Check the subtree rooted at f for text and images, and return true if no text is found and only images exist.
        Also search for keyword inside the image - feature added
            - text node <p> OKLESGO <p> => OKLESGO is the text node
            - \<\w+\>.+\<\/\w+\>
            - get_text used in the child to see if there's any text node
    """
    if single_elem.get_text() == '' or single_elem.get_text() != '\n':
        images = single_elem.find_all('img')
        if images:
            if opt_keyword_locally(images, keywords):
                return True
        else:
            print("no image found")

    return False

def Global_research(soup, keywords):
    all_ins = soup.find_all('input')
    all_img = soup.find_all('img')

    # in ex img ex
    # in ex im not ex
    # in not ex im ex
    # in not ex im not ex

    if all_ins or all_img:
        if opt_keyword_locally(all_ins, keywords) or opt_keyword_locally(all_img, keywords):
                return True

    return False

def Find_Forms(htmlfile):
    """
        Returns if FORM, INPUT and LOGIN keywords are found

        treat the tags as dictionaries:
            soup.<tag name>[<name attribute>]
                => soup.input['id']

         “secure”, “account”, “webscr”, “login”, “ebayisapi”, “signin”, “banking”, “confirm”
    """

    keywords = ['password', 'pass', 'passcode', 'pin', 'pincode', 'username', 'user', 'user_login',
        'pwd', 'user_pass', 'password-input', 'login', 'PASSWORD']

    with open(htmlfile, encoding='UTF-8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    all_forms = soup.find_all('form')

    if all_forms:   # form detected

        for index in range(0, len(all_forms)):
        
            childs_input = all_forms[index].find_all('input')

            if childs_input: #input detected

                if opt_keyword_locally(childs_input, keywords): # search for keyword in the scope of the attributes of the element
                    print("OPT")
                    return True
                
                elif isSerchForm(all_forms[index]) is False:
                    
                    if seach_K_up(all_forms[index], keywords):
                        print("K UP")
                        return True
                    elif isOnlyImages(all_forms[index], keywords):
                        return True
       
                else:
                    print("search form")
    else:
        print("no forms in the document")
        print("look for inputs and images in the whole DOM")

        if Global_research(soup, keywords):
            return True

    return False

def main():
    # Get_data(filename = 'phish_tank.json')
    # print(Modify_HTML(filename='Test3.html'))
    # Calculate_SHA1()
    # Save_page()
    # os.chdir('.\PagineHTML')
    # Get_online_page()
    # Save_page()
    Get_data()

if __name__ == '__main__':
    main()