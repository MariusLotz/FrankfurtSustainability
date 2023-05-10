import requests
import pandas as pd


def main():
    ### Input:
    api_key = 'AIzaSyBJdpWQ8WkqgqlDeTyKuy4b25CDjYWW5_Y'
    location = '50.1109,8.6821'  # Frankfurt latitude and longitude
    radius = 9999  # 9999 meters radius
    keywords = ['bank', 'asset', 'versicherung', 'insurance', 'invest', 'fund', 'credit', 'börse', 'stock']
    ###

    results = []

    for keyword in keywords:
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&keyword={keyword}&key={api_key}'

        # Make a request to the Places API
        response = requests.get(url)
        data = response.json()

        # Process the API response
        if data['status'] == 'OK':
            places = data['results']
            for place in places:
                name = place['name']
                address = place['vicinity']
                results.append({'Name': name, 'Address': address, 'Keyword': keyword})
                print(f'Name: {name}', f'Address: {address}')
        else:
            # Print the error status and message
            error_status = data['status']
            error_message = data.get('error_message', '')
            print(f'Request failed with status: {error_status}')
            print(f'Error message: {error_message}')

    # Convert the results to a Pandas DataFrame
    df = pd.DataFrame(results)

    # Save the DataFrame to a CSV file
    df.to_csv('places1.csv', index=False)

if __name__=="__main__":
    main()