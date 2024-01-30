import requests
import csv
 
def fetch_data(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        return None
 
def write_to_csv(items, file, is_header=False):
    writer = csv.writer(file)
    if is_header:
        writer.writerow(['Model', 'Status'])
    for item in items:
        model = item['name']
        status = 'Enabled' if item['enabled'] else 'Disabled'
        writer.writerow([model, status])
 
api_key = input("Please enter your API key: ")
 
url = "https://api.au.xdr.trendmicro.com//v3.0/dmm/models"
 
headers = {
    'Authorization': f'Bearer {api_key}'
}
 
with open('models_status.csv', 'w', newline='', encoding='utf-8') as file:
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