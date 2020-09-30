from bs4 import BeautifulSoup as bs
import requests

def main():
  url = "https://contentzone.eurocontrol.int/aircraftperformance/default.aspx?"
  source = requests.get(url).text

  soup = bs(source, features="html.parser")

  art_one = soup.find_all('tr', {'class': 'ap-list-row'})
  art_two = soup.find_all('tr', {'class': 'ap-list-row-alternate'})

  for a in art_one:
    icao_designator = a.find('h3', {'class': 'ap-list-item-icao'}).findChild('a').string
    acft_names = a.find('p', {'class': 'ap-list-item-name'}).text.strip().split()
    acft_name = " ".join(acft_names)
    print(icao_designator)
    print(acft_name)

main()