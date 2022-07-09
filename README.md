# Phishing-Detection

### About the project
This project was an idea of a good friend of mine; we wanted to see if it were possible to create a machine learning algorithm to detect phishing sites.

We searched for papers that talked about this specific topic and we found [CANTINA+]( https://dl.acm.org/doi/10.1145/2019599.2019606). The whole project is heavily based on this paper, but we modified some of the features: the part about web-based feature were changed with OSINT features or reputation-based feature.

We relied on **VirusTotal** and **XForce** for domains reputation and used other sites to gather information about the PageRank and the whois of the domains.
Due to limited API calls a day, for each of these features we created separated scripts.

### Dataset
The malicious dataset was gathered from **PhishTank**'s online database, a platform where possible phishing sites can be submitted which are subsequently verified.

For benign dataset, my friend created a web scraper to get some benign domains from the website (https://botw.org/).

In total, we collected 2435 URLs:
- 1237 phishing.
- 1198 benign.

Then with all URLs we decided to download the HTML of each site. This decision was made because phishing sites, most of the time, have a short period of life. You can find the whole collection of HTMLs [here](https://drive.google.com/drive/folders/1c9DyVQxPiy-UAeIjxLMD3HzRGTRyrtiW).

### Functions and Filters
As I specified before, this work is based on CANTINA+, we implemented the content of their framework:
* Hash-based filter:
   - took a sample of 80 phishing URLs from PhishTank;
   - downloaded the HTML of the website;
   - calculated the hash of the given website.
* HTML based filter
   - the whole point of this filter is to find keywords inside input / form tags or even images.
* Feature extraction
   - three type of features:
      1. URL based features;
      2. HTML based features;
      3. Reputation based featues.
* Machine learning
   - we used a random forest to perform the detection.

A little note, we implemented every aspect of the framework, though we didn't really create the pipeline described in the paper.
For testing purposes, we went directly on the machine learning part after extracting the domains (both malicious and benign), the download of the HTMLs and the feature extraction.


### Project Status
Currently the project is on hold, meaning we've come up with ideas, but before moving forward we need to implement better some functionalities. The whole code in here, it's just a base of what we want to do in the future.

Also, I'm not an expert programmer, I would be very grateful if you could give me tips / tricks to make the code easier to read and understand.
