import sys
import requests
from urllib.parse import quote_plus

if __name__ == "__main__":
    # Check if a search query was provided
    if len(sys.argv) < 2:
        print("Usage: python3 grocery.py <search-query>")
        sys.exit(1)

    # URL encode the search query
    query = quote_plus(sys.argv[1])


# Print the response in JSON format
# print(response.json())

def extract_relevant_data(response_data):
    # Extract the required fields from each item
    extracted_items = [
        {
            'id': item['id'],
            'name': item['name'],
            'displayName': item['displayName'],
            'type': item['type'],
            'subType': item['subType'],
            'unit': item['unit'],
            'unitQuantity': item['unitQuantity'],
            'price': item['price'],
        }
        for sublist in response_data['results']
        for item in sublist
    ]

    # Create a new dictionary for the new list
    new_list = {'items': extracted_items}
    
    return new_list

def groceries_search(query):
    # Define the URL and the necessary query parameters
    base_url = "https://partnersapi.gethomesome.com/product/search"
    query_string = f"search={query}&categoryorder=DiwaliSpecials%20GaneshChaturthi%20Specials%20CutVegetables%20FruitsVegetables%20DairyEggs%20Snacks%20Pulses%20Pantry%20MealKits%20RiceNoodles%20Flours%20Bakery%20Beverages%20Frozen%20HealthBeauty%20Household&item={query}"

    # Headers necessary for the API to authenticate the request
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Apikey": "BAB01330-662C-4A7E-883C-A9635792747B",
        "Authtoken": "7fc4286d-f45d-482e-abe9-0555e6002eb0",
        "Emailid": "vasanth.sabavat@gmail.com",
        "Location": "EC86C6F7-F8ED-4D0C-B74C-3B39028967CF",
        "Origin": "https://www.apnabazarstores.com",
        "Referer": "https://www.apnabazarstores.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69"
    }

    # Make the HTTP request and get the response
    response = requests.get(f"{base_url}?{query_string}", headers=headers)
    return extract_relevant_data(response.json())

