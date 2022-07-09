# Phishing-Detection

This project was an idea of a good friend of mine; we wanted to see if it were possible to create a machine learning algorithm to detect phishing sites. 
We search for papers that talked about this specific topic and we found [CANTINA+]( https://dl.acm.org/doi/10.1145/2019599.2019606)
The whole project is heavily based on that paper, but we modified some of the features in it: the part about web-based feature were changed with OSINT features or reputation-based feature.
We relied on **VirusTotal** and **XForce** for domain reputation and used other sites to gather information about the PageRank and the whois of the domain.
Due to limited API calls a day, for each of these features we created separated scripts.

#### Dataset

[here](https://drive.google.com/drive/folders/1c9DyVQxPiy-UAeIjxLMD3HzRGTRyrtiW)
---
#### Prova



