import requests
import time

# Send a GET request to an IP API
response = requests.get('https://api.ipify.org?format=json')

# Parse the JSON response
data = response.json()

# Extract the IP address from the response
ip_address = data['ip']

# Print the IP address
print(f"Your IP address is: {ip_address}")

# Delay for 5 seconds
time.sleep(5)

# End of the code
print("Program finished.")
