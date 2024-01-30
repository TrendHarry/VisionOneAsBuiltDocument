import requests
import csv

def get_roles_and_permissions(api_key):
    url = "https://api.au.xdr.trendmicro.com/v2.0/xdr/portal/roles"
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']['items']
    else:
        print(f"Error fetching data: {response.status_code}")
        return []

def check_permission(role_permissions, permission_path):
    current_level = role_permissions
    for key in permission_path:
        if key in current_level:
            current_level = current_level[key]
        else:
            return 'No'
    return 'Yes' if current_level == 1 else 'No'

def write_to_csv(roles, permission_mapping, filename='VisionOneRolesPermissions.csv'):
    fieldnames = ['Permission'] + [role['role'] for role in roles]
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for readable_perm, perm_path in permission_mapping.items():
            row = {'Permission': readable_perm}
            for role in roles:
                row[role['role']] = check_permission(role['permissions'], perm_path)
            writer.writerow(row)

    print(f"CSV file '{filename}' has been created.")

api_key = input("Please enter your API key: ")
roles = get_roles_and_permissions(api_key)

permission_mapping = {
    "ATTACK SURFACE RISK MANAGEMENT - Executive Dashboard - View": ["ciso", "view"],
    #"Another Permission - Subcategory - Action": ["categoryKey", "subcategoryKey", "actionKey"],
}

write_to_csv(roles, permission_mapping)
