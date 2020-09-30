from bs4 import BeautifulSoup
import requests, json

def main():
  '''
  This is the main function, which coordinates and calls other functions
  '''
  eventTarget = ""
  eventArgument = ""
  viewState = ""
  viewStateGenerator = ""
  eventValidation = ""

  page_count = 3
  for i in range(1, page_count+1):
    print(i)
    data, viewState, viewStateGenerator, eventValidation = pageDataRetriever(i, eventTarget, eventArgument, viewState, viewStateGenerator, eventValidation)
    soup = BeautifulSoup(data, features="html.parser")
    art_one = soup.find_all('tr', {'class': 'ap-list-row'})
    for a in art_one:
      icao_designator = a.find('h3', {'class': 'ap-list-item-icao'}).findChild('a').string
      acft_names = a.find('p', {'class': 'ap-list-item-name'}).text.strip().split()
      acft_name = " ".join(acft_names)
      print(icao_designator)
      print(acft_name)

  pass

def pageDataRetriever(page_number, eT, eA, vS, vSG, eV):
  '''
  This function scrapes each page's data, using a token-based request process
  '''
  url = "https://contentzone.eurocontrol.int/aircraftperformance/"

  data = {
    '__EVENTTARGET': 'ctl00$MainContent$wsBasicSearchGridView',
    '__EVENTARGUMENT': f'Page${page_number}',
    '__VIEWSTATE': vS,
    '__VIEWSTATEGENERATOR': vSG,
    '__EVENTVALIDATION': eV,
  }

  response = requests.post(url, data=data).text
  # print(response)

  soup = BeautifulSoup(response, features="html.parser")
  new_vS = soup.find('input', {'name': '__VIEWSTATE'})['value']
  new_vSG = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
  new_eV = soup.find('input', {'name': '__EVENTVALIDATION'})['value']

  return response, new_vS, new_vSG, new_eV

def scraper(page_data):
  '''
  This function retrieves the necessary data with scraping from each page
  Data is fed to the function from the pageDataRetriever function above
  '''
  pass

main()