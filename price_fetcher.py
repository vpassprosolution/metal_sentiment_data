import requests

METALS_API_KEY = "cflqymfx6mzfe1pw3p4zgy13w9gj12z4aavokqd5xw4p8xeplzlwyh64fvrv"

def fetch_price(symbol, debug=False):
    url = f"https://metals-api.com/api/latest?access_key={METALS_API_KEY}&base=USD&symbols={symbol}"
    try:
        response = requests.get(url)
        data = response.json()
        if debug:
            print(f"🔍 API Response for {symbol}: {data}")
        key = f"USD{symbol}"
        if data.get("success") and "rates" in data and key in data["rates"]:
            return round(data["rates"][key], 2)
        else:
            if debug:
                print(f"❌ API error or missing {key}")
            return None
    except Exception as e:
        if debug:
            print(f"❌ Error fetching price for {symbol}: {e}")
        return None
