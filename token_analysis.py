import requests

# Function to fetch token data from Dexscreener API
def fetch_token_data(contract_address):
    try:
        # Dexscreener API endpoint for fetching token data
        api_url = f"https://api.dexscreener.io/latest/dex/tokens/{contract_address}"
        
        # Fetch the data
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching data:", response.status_code)
            return None
    except Exception as e:
        print("Error:", e)
        return None

# Function to calculate Fibonacci levels
def calculate_fibonacci_levels(high, low):
    levels = {
        "0% (High)": high,
        "23.6%": high - 0.236 * (high - low),
        "38.2%": high - 0.382 * (high - low),
        "50%": high - 0.5 * (high - low),
        "61.8%": high - 0.618 * (high - low),
        "100% (Low)": low,
    }
    return levels

# Function to analyze the token
def analyze_token(contract_address):
    # Fetch token data
    data = fetch_token_data(contract_address)
    if data and "pairs" in data:
        # Extract price data
        pair = data["pairs"][0]
        token_name = pair['baseToken']['name']
        token_symbol = pair['baseToken']['symbol']
        current_price = float(pair["priceUsd"])
        print(f"Token Name: {token_name}")
        print(f"Token Symbol: {token_symbol}")
        print(f"Current Price (USD): ${current_price:.6f}")

        # Simulate price history (replace with actual price data if available)
        prices = [current_price * (1 + 0.01 * i) for i in range(-50, 51)]  # Generate 100 prices around the current price
        high = max(prices)
        low = min(prices)

        # Calculate Fibonacci levels
        fib_levels = calculate_fibonacci_levels(high, low)
        print("\nFibonacci Levels:")
        for level, value in fib_levels.items():
            print(f"{level}: ${value:.6f}")

        # Investment decision
        investable = False
        best_entry = None
        if fib_levels["50%"] <= current_price <= fib_levels["38.2%"]:
            investable = True
            best_entry = fib_levels["50%"]  # Safe entry level is near 50% Fibonacci retracement
        elif current_price <= fib_levels["61.8%"]:
            investable = True
            best_entry = current_price  # Buy immediately if price is near or below 61.8%

        # Print investment decision
        if investable:
            print("\nInvestment Decision: YES")
            print(f"Best Entry Price: ${best_entry:.6f}")
        else:
            print("\nInvestment Decision: NO")
            print("Current price is not at an ideal entry level based on Fibonacci analysis.")
    else:
        print("Error: Unable to fetch valid data for the token.")

# Main function
def main():
    # Token contract address
    contract_address = "8AYpR27W1Y8WrW7yVyxB8AaM8qCTuCwMcB3HFmsFpump"
    
    # Analyze the token
    analyze_token(contract_address)

if __name__ == "__main__":
    main()
