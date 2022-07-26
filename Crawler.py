import requests
import bs4
import json


def writeToFile(data, state):
    with open(f'{state}.json', 'w') as outfile:
        json.dump(data, outfile)


res = requests.get('https://www.simpliance.in/minimum-wages')

soup = bs4.BeautifulSoup(res.text, 'html.parser')

dropdown = soup.find('select', {'id': 'statefilter'})

numStates = len(dropdown.find_all('option'))

places = []

for i in range(1, numStates):
    places.append(dropdown.findChildren('option')[i].text)

finalData = {}

for place in places:
    place_res = requests.get(
        'https://www.simpliance.in/minimum-wages/' + place)
    place_soup = bs4.BeautifulSoup(place_res.text, 'html.parser')

    headers = []
    headers_len = len(place_soup.find_all('th'))
    for i in range(0, headers_len):
        headers.append(place_soup.findAll('th')[i].text)

    try:
        table = place_soup.find(
            "table", {"class": "table table-bordered table-condensed table-hover"})
        rows = table.findAll('tr')
        data = [[td.findChildren(text=True)
                for td in tr.findAll("td")] for tr in rows]
        data = [[u"".join(d).strip() for d in l] for l in data]
        data = data[1:]
    except:
        table = place_soup.find("table")
        rows = table.findAll('tr')
        data = [[td.findChildren(text=True)
                for td in tr.findAll("td")] for tr in rows]
        data = [[u"".join(d).strip() for d in l] for l in data]
        data = data[1:]
    finalData.update(
        {
            place: {
                "headers": headers,
                "data": data
            }
        }
    )
    writeToFile({
        place: {
                "headers": headers,
                "data": data
                }
    }, place)
