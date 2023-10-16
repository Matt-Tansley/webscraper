import requests
from bs4 import BeautifulSoup

parties_xml = requests.get("https://interactives.stuff.co.nz/election-data/2023/xml/parties.xml")

soup = BeautifulSoup(parties_xml.content, "xml")

parties = soup.find_all("party")

for party in parties:
    print(party['p_no'])
