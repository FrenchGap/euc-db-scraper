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

  final_list = []

  page_count = 2
  for i in range(1, page_count+1):
    print(i)
    data, viewState, viewStateGenerator, eventValidation = pageDataRetriever(i, eventTarget, eventArgument, viewState, viewStateGenerator, eventValidation)
    final_list = scraper(data, final_list)

  return final_list

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

def scraper(page_data, final_list):
  '''
  This function retrieves the necessary data with scraping from each page
  Data is fed to the function from the pageDataRetriever function above
  '''
  soup = BeautifulSoup(page_data, features="html.parser")
  art_one = soup.find_all('tr', {'class': 'ap-list-row'})
  art_two = soup.find_all('tr', {'class': 'ap-list-row-alternate'})

  for a in art_one:
    icao_designator = a.find('h3', {'class': 'ap-list-item-icao'}).findChild('a').string
    acft_names = a.find('p', {'class': 'ap-list-item-name'}).text.strip().split()
    acft_name = " ".join(acft_names)
    print(icao_designator)
    img_url = a.find('img', {'class': 'float-left ap-list-item-photo'})['src']

    first_row = a.find_all('div', {'class': 'col-3'})
    acft_type = first_row[0].findChild('p').text
    acft_wtc = first_row[1].findChild('p').text
    acft_recat = first_row[2].findChild('p').text
    acft_apc = first_row[3].findChild('p').text
    
    second_row = a.find_all('div', {'class': 'col'})
    for sr in second_row:
      if "Initial" in sr.find_all('p')[0].text:
        initial_data = {
          'ROC': sr.find_all('p')[1].text,
          'IAS': sr.find_all('p')[2].text,
        }
      if "150" in sr.find_all('p')[0].text:
        fl150_data = {
          'ROC': sr.find_all('p')[1].text,
          'IAS': sr.find_all('p')[2].text,
        }
      if "240" in sr.find_all('p')[0].text:
        fl240_data = {
          'ROC': sr.find_all('p')[1].text,
          'IAS': sr.find_all('p')[2].text,
        }
      if "Cruise" in sr.find_all('p')[0].text:
        cruise_data = {
          'ceiling': sr.find_all('p')[1].text,
          'ROC': sr.find_all('p')[2].text,
          'TAS': sr.find_all('p')[3].text,
          'mach': sr.find_all('p')[4].text,
        }
      if "Approach" in sr.find_all('p')[0].text:
        app_data = {
          'IAS': sr.find_all('p')[1].text,
          'MCS': sr.find_all('p')[2].text,
        }
    
    acft_data = {
      'designator': icao_designator,
      'name': acft_name,
      'type': acft_type,
      'wtc': acft_wtc,
      'recat': acft_recat,
      'apc': acft_apc,
      'initial_climb': initial_data,
      'climb_fl150': fl150_data,
      'climb_fl240': fl240_data,
      'cruise': cruise_data,
      'approach': app_data,
      'img_url': img_url,
    }
    final_list.append(acft_data)

  for a in art_two:
    icao_designator = a.find('h3', {'class': 'ap-list-item-icao'}).findChild('a').string
    acft_names = a.find('p', {'class': 'ap-list-item-name'}).text.strip().split()
    acft_name = " ".join(acft_names)
    print(icao_designator)
    img_url = a.find('img', {'class': 'float-left ap-list-item-photo'})['src']

    first_row = a.find_all('div', {'class': 'col-3'})
    acft_type = first_row[0].findChild('p').text
    acft_wtc = first_row[1].findChild('p').text
    acft_recat = first_row[2].findChild('p').text
    acft_apc = first_row[3].findChild('p').text
    
    second_row = a.find_all('div', {'class': 'col'})
    for sr in second_row:
      if "Initial" in sr.find_all('p')[0].text:
        initial_data = {
          'ROC': sr.find_all('p')[1].text,
          'IAS': sr.find_all('p')[2].text,
        }
      if "150" in sr.find_all('p')[0].text:
        fl150_data = {
          'ROC': sr.find_all('p')[1].text,
          'IAS': sr.find_all('p')[2].text,
        }
      if "240" in sr.find_all('p')[0].text:
        fl240_data = {
          'ROC': sr.find_all('p')[1].text,
          'IAS': sr.find_all('p')[2].text,
        }
      if "Cruise" in sr.find_all('p')[0].text:
        cruise_data = {
          'ceiling': sr.find_all('p')[1].text,
          'ROC': sr.find_all('p')[2].text,
          'TAS': sr.find_all('p')[3].text,
          'mach': sr.find_all('p')[4].text,
        }
      if "Approach" in sr.find_all('p')[0].text:
        app_data = {
          'IAS': sr.find_all('p')[1].text,
          'MCS': sr.find_all('p')[2].text,
        }
    
    acft_data = {
      'designator': icao_designator,
      'name': acft_name,
      'type': acft_type,
      'wtc': acft_wtc,
      'recat': acft_recat,
      'apc': acft_apc,
      'initial_climb': initial_data,
      'climb_fl150': fl150_data,
      'climb_fl240': fl240_data,
      'cruise': cruise_data,
      'approach': app_data,
      'img_url': img_url,
    }
    final_list.append(acft_data)
  
  return final_list

data = main()
print(data)