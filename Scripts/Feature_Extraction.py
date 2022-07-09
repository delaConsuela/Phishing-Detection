from operator import le
import re
from socket import SO_ERROR
from bs4 import BeautifulSoup
import proto 
import Snippet
from urllib.parse import urlparse
import requests as req
from requests.auth import HTTPBasicAuth
import whois
import datetime
import os
import csv

def URL_based_Features(url):

    output_vect = []

    output_vect.append(isEmbeddedDomain(url))
    output_vect.append(isIPAddress(url))
    output_vect.append(Count_dots(url))
    output_vect.append(isSuspiciousURL(url))
    output_vect.append(Sensitive_Words_in_URL(url))
    output_vect.append(TLD_Out_of_Position(url))

    return output_vect

def HTML_based_Features(filename, url):

    output_vect = []

    keywords = ['password', 'pass', 'passcode', 'pin', 'pincode', 'username', 'user', 'user_login',
        'pwd', 'user_pass', 'password-input', 'login', 'PASSWORD']

    with open(filename, encoding='UTF-8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    output_vect.append(Bad_Form(soup, url, keywords))
    output_vect.append(Bad_Action_Field(soup, url, keywords))
    output_vect.append(Non_matching_URL(soup, url))
    output_vect.append(Out_of_Position_Brand_Name(soup, url))
    output_vect.append(os.path.getsize(filename))

    return output_vect

def Web_based_Features(domain):

    output_vect = []

    output_vect.append(Age_Of_Domain(domain))
    # output_vect.append(Get_Page_Rank(domain))
    # output_vect.append(VT_Reputation_domain(domain))
    # output_vect.append(XForce_Reputation_domain(domain))

    return output_vect

# URL based features

def isEmbeddedDomain(url):
    """
        REGEX:
            Three constraints must be met for a dot-separated string to be eligible for an embedded domain:
                1) at least three segments must exist
                2) each segment must have two or more characters.
                3) each segment is composed of letters, numbers and underscores only.
            Example: "www.google.com"
            (([\w\n\_]){2,}\.){2,}([\w\n\_]){2,}
    """
    segments = url.split('.')

    num_segments = len(segments)
    flag_num_seg = num_segments > 2

    vect = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']

    flag_char = 1
    flag_char_only = 1

    for seg in segments:
        if len(seg) < 2:
            flag_char = 0
    

        for sing_char in seg:
            if sing_char.lower() not in vect:
                flag_char_only = 0


    if flag_num_seg and flag_char and flag_char_only:
        return 1

    return 0

def isIPAddress(url):
    match = re.search("^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}", url)
    if match != None:
        return 1
    
    return 0

def Count_dots(url):
    count = 0

    for i in range(0, len(url)):
        if url[i] == '.':
            count +=1
    
    return count

def isSuspiciousURL(url):
    for i in range(0, len(url)):
        if url[i] == '@' or url[i] == "-":
            return 1
    
    return 0

def Sensitive_Words_in_URL(url):
    sensitive_words = ["secure", "account", "webscr", "login", "ebayisapi", "signin", "banking", "confirm"]
    count = 0

    for word in sensitive_words:
        if word in url:
            count += 1

    return count

def TLD_Out_of_Position(url):
    TLD = ["com", "org", "net", "int", "edu", "gov" ,"mil"]

    no_dots_url = url.split('.')
    tld_position = no_dots_url[-1]
    num_elem = len(no_dots_url)

    for index in range(0, num_elem):
        if no_dots_url[index] in TLD:
            if index != num_elem-1:
                return 1

    return 0  

# HTML based features

def Bad_Form(soup, url, keywords):
    """
        1) an HTML form
        2) an <input> tag in the form
        3) keywords related to sensitive information like “password” and “credit card number” or no text at all but images only within the scope of the HTML form
        4) a non-https scheme in the URL in the action field or in the webpage URL when the action field is empty.
    """
    forms = soup.find_all('form')

    if forms:
        for index in range(0, len(forms)):
            childs_input = forms[index].find_all('input')

            if childs_input:
                if Snippet.opt_keyword_locally(childs_input, keywords):

                    if 'action' in forms[index].attrs.keys():
                        if 'https' not in forms[index]['action']:
                            return 1

                    else:
                        if 'https' not in url:
                            return 1
            else:
                return -1


    return 0
    
def Bad_Action_Field(soup, url, keywords):
    """
    Before doing a check on action, we must find form bad forms
        1) empty action,
        2) action refering to a file
        3) action refering to a different domain (cross site scripting)
    """

    forms = soup.find_all('form')

    if forms:
        for index in range(0, len(forms)):
            childs_input = forms[index].find_all('input')

            if childs_input:
                if Snippet.opt_keyword_locally(childs_input, keywords):

                    if 'action' in forms[index].attrs.keys():

                        action_content = forms[index]['action']
                        if re.search("(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", action_content) is None:
                            return 1

                        else:
                            
                            domain = urlparse(url).netloc
                            action_domain = urlparse(forms[index]['action']).netloc
                        
                            if domain != action_domain:
                                return 1

                    else:
                        return 1
            else:
                return -1

    return 0

def Special_Character(url):
    special_char = [
        ' ', '!', '"', '’', '(', ')', '[', ']', '{','}', '<', '>', '@', '|', '?', ';'
    ]

    for sing_char in url:
        if sing_char in special_char:
            return True
    
    return False

def Non_matching_URL(soup, page_url):

    """
        This feature examines all the links in the HTML and checks if the most frequent domain coincides with the page domain
        we count the percentage of highly-similar links** in the HTML, and set the value of this feature to 1 if any single pattern occurs more often than a threshold. In addition, we also count the percentage of empty or ill-formed links in the HTML, and apply thresholding to set corresponding feature values

        **Highly-similar links in this paper are defined to be those that are either identical or differ onlyin the fragment part of the URL
    """

    domains = []
    dom_dict = {}

    urls = re.findall(
        "(^https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
        , str(soup))

    urls = list(urls)

    if len(urls) == 0:
        return -1

    for elem in urls:
        if 'http' in elem or 'https' in elem:
            url = elem.split('"')
            if Special_Character(url[0]) is False:
                if url[0] is not None:
                    dom = urlparse(url[0]).netloc
                    domains.append(dom)
        
    for sing_dom in domains:
        if sing_dom != '':
            dom_dict[sing_dom] = 0

    # frequencies
    for sing_dom in domains:
        if sing_dom in dom_dict.keys():
            dom_dict[sing_dom] += 1
    
    # return key with the max value
    if len(dom_dict) > 0:
    
        val = dom_dict.values()
        max_val = max(val)


        for elem in dom_dict:
            if dom_dict[elem] == max_val:
                if elem in page_url:
                    return 0
    else:
        return -1

    return 1

def Out_of_Position_Brand_Name(soup, url):
    """
        Search for the most frequent value and set it as the potential brand name.
        Return 1 if it's in the wrong position.
        To be in the right position, it should be as in the second level domain.
    """
    domains = []
    dom_dict = {}
    most_freq_kywrd = ''

    urls = re.findall(
        "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
        , str(soup))

    urls = list(urls)

    if len(urls) == 0:
        return -1

    for elem in urls:
        if 'http' in elem or 'https' in elem:
            url = elem.split('"')
            if Special_Character(url[0]) is False:
                if url[0] is not None:
                    dom = urlparse(url[0]).netloc
                    domains.append(dom)
        
    for sing_dom in domains:
        if sing_dom != '':
            dom_dict[sing_dom] = 0

    # frequencies
    for sing_dom in domains:
        if sing_dom in dom_dict.keys():
            dom_dict[sing_dom] += 1
    
    # return key with the max value
    if len(dom_dict) > 0:
    
        val = dom_dict.values()
        max_val = max(val)

        for elem in dom_dict:
            if dom_dict[elem] == max_val:
                most_freq_kywrd = elem

    if most_freq_kywrd != '':

        if most_freq_kywrd in url:

            index = url.find(most_freq_kywrd)
            final_index = index + len(most_freq_kywrd)

            if final_index != len(url):
                return 1
    
    return 0

def Age_Of_Domain(domain):
    date = datetime.datetime.now()

    year_now = str(date.year)
    month_now = str(date.month)
    
    whois_ret = whois.whois(domain)

    if 'creation_date' in whois_ret.keys():

        date = str(whois_ret['creation_date']).split('-')

        if whois_ret['creation_date'] == None:
            return -1

        elif year_now == date[0]:
            month = int(month_now) - int(date[1])

            if month in range(0, 3):
                return 1
    else:
        return -1

    return 0

def Get_Page_Rank(domain):
    
    header = {
        'API-OPR': '-'
    }

    res = req.get(f'https://openpagerank.com/api/v1.0/getPageRank?domains%5B0%5D={domain}', headers=header)

    total_page_rank = 0

    if res.status_code == 200:

        res = res.json()

        list_response = res['response']

        for i in range(0, len(list_response)):
            total_page_rank += res['response'][i]['page_rank_integer']
    
    else:
        return -1

    return total_page_rank


def VT_Reputation_domain(domain):
    """
        curl --request GET --url https://www.virustotal.com/api/v3/domains/{domain} --header 'x-apikey: <your API key>'
    """
    header = {
        'x-apikey': '-'
    }

    res = req.get(f'https://www.virustotal.com/api/v3/domains/{domain}', headers=header)

    if res != 204 or res != 400 or res != 403:

        res_conv = res.json()

        mal = res_conv['data']['attributes']['last_analysis_stats']['malicious']
        sus = res_conv['data']['attributes']['last_analysis_stats']['suspicious']
    
        risk_score = mal + sus

    else:
        return -1

    return risk_score

def XForce_Reputation_domain(domain):
    """
        https://api.xforce.ibmcloud.com/url/host/early_warning
        key: -
        pw: -
    """
    key = '-'
    password = '-'

    header = {
        'accept': 'application/json',
        'Authorization': 'Basic Og=='
    }

    res = req.get(f'https://api.xforce.ibmcloud.com/url/{domain}', 
    headers=header, auth=HTTPBasicAuth(key, password))

    res_conv = res.json()

    if 'error' in res_conv.keys():
        print(res.text)
        return -1

    elif "cats" in res_conv["result"].keys():

        if "Phishing URLs" in res_conv["result"]["cats"].keys():

            if res_conv["result"]["score"] > 6:
                return 1

        elif res_conv["result"]["score"] > 8:
            return 1

    else:
        return -1    

    return 0

def main():
    filename = 'dataset.csv'
    ret_vect_URL = []
    ret_vect = []

    with open(filename, 'r') as rfile:
        content = csv.reader(rfile)

        for row in content:
            ret_vect_URL.append(URL_based_Features(row[1]))

            if int(row[0]) < 5000:
                os.chdir('PagineHTML')
                filename = row[0] + '.html'

                if filename in os.listdir():
                    ret_vect.append(HTML_based_Features(filename, row[1]))
                else:
                    ret_vect.append([-1,-1,-1,-1,0])
                os.chdir('..')

            else:
                os.chdir('PagineLecite')
                filename = row[2] + '.html'

                if filename in os.listdir():
                    ret_vect.append(HTML_based_Features(filename, row[1]))
                else:
                    ret_vect.append([-1,-1,-1,-1,0])
                os.chdir('..')

    final_vect = []

    for i in range(0, len(ret_vect)):

        final_vect.append(ret_vect_URL[i])
        final_vect.append(ret_vect[i])

        with open('URLAndHTML_feature.csv', 'a') as wcsv:
            csv_write = csv.writer(wcsv)
            csv_write.writerow(final_vect)
        
        final_vect = []

if __name__ == '__main__':
    main()