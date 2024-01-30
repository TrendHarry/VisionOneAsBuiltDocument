import requests
import csv

def fetch_data(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        return None

def process_criteria(criteria):
    if not criteria:
        return 'ALL'
    
    formatted_criteria = []
    for criterion in criteria:
        values = ', '.join(criterion['fieldValues'])
        formatted_criteria.append(f'{criterion["fieldName"]}:{values}')
    return ' AND '.join(formatted_criteria)

def format_targets(targets):
    if not targets:
        return 'ALL'
    
    formatted_targets = []
    for key, value in targets.items():
        formatted_targets.append(f'{key}:{("|").join(value)}')
    return ', '.join(formatted_targets)

def write_to_csv(items, file, is_header=False):
    writer = csv.writer(file)
    if is_header:
        writer.writerow(['Exception ID', 'Name', 'Targets', 'Event Source / Filter', 'Match Criteria'])

    for item in items:
        exception_id = item['displayId']
        name = item['name']
        targets = format_targets(item.get('targetEntities', {}))
        filter_names = set(f['filterName'] for f in item['scope']['filters'])
        filters = ', '.join(filter_names)
        criteria = process_criteria(item.get('criteria', []))
        writer.writerow([exception_id, name, targets, filters, criteria])

api_key = input("Please enter your API key: ")

url = "https://api.au.xdr.trendmicro.com/v3.0/dmm/exceptions"

headers = {
    'Authorization': f'Bearer {api_key}'
}

with open('FSSI Exceptions Details.csv', 'w', newline='', encoding='utf-8') as file:
    first_page = True
    while url:
        data = fetch_data(url, headers)
        if data:
            if first_page:
                write_to_csv(data['items'], file, is_header=True)
                first_page = False
            else:
                write_to_csv(data['items'], file)

            url = data.get('nextLink', None)
        else:
            break

print("CSV file 'exceptions_report.csv' has been created successfully.")
