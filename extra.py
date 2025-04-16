with open('data.json', 'w') as file:
    json.dump(response.json(), file, indent=4)