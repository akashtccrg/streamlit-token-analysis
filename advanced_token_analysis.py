import requests

# Function to fetch token data from Dexscreener API
def fetch_token_data(contract_address):
    try:
        # Dexscreener API endpoint for fetching token data
        api_url = f"https://api.dexscreener.io/latest/dex/tokens/{contract_address}"
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

# Function to analyze the token and apply all safety filters
def analyze_token(contract_address):
    # Fetch token data
    data = fetch_token_data(contract_address)
    if data and "pairs" in data:
        pair = data["pairs"][0]
        token_name = pair['baseToken']['name']
        token_symbol = pair['baseToken']['symbol']
        current_price = float(pair["priceUsd"])

        # Attempt to retrieve market cap and volume; handle missing data
        market_cap = pair.get("fdv", "N/A")
        volume = pair.get("volume", {}).get("usd", "N/A")

        # Display basic token info
        print(f"\nToken Name: {token_name}")
        print(f"Token Symbol: {token_symbol}")
        print(f"Current Price (USD): ${current_price:.6f}")
        print(f"Market Cap: {market_cap}")
        print(f"24H Volume: {volume}")

        # Ensure volume and market cap are numeric for safety checks
        if isinstance(market_cap, (int, float)) and isinstance(volume, (int, float)):
            # Safety filters
            if market_cap < 150000 or market_cap > 15000000:
                print("\n❌ Investment Decision: NO")
                print("Reason: Market cap is outside the optimal range (150k - 15M).")
                return
            if volume < market_cap * 0.05:
                print("\n❌ Investment Decision: NO")
                print("Reason: Trading volume is too low compared to market cap.")
                return

        # Simulate price history for Fibonacci calculation
        prices = [current_price * (1 + 0.01 * i) for i in range(-50, 51)]
        high = max(prices)
        low = min(prices)

        # Calculate Fibonacci levels
        fib_levels = calculate_fibonacci_levels(high, low)
        print("\nFibonacci Levels:")
        for level, value in fib_levels.items():
            print(f"{level}: ${value:.6f}")

        # Maximum price projection
        max_price_projection = current_price * 2.5  # Assume maximum 2.5x potential
        print(f"\nMaximum Price Projection: ${max_price_projection:.6f}")
        risk_level = ((fib_levels["100% (Low)"] - current_price) / current_price) * 100
        print(f"Risk Level (Drawdown from Current Price to Low): {abs(risk_level):.2f}%")

        # Profit-taking strategy
        investable = False
        best_entry = None
        if fib_levels["50%"] <= current_price <= fib_levels["38.2%"]:
            investable = True
            best_entry = fib_levels["50%"]
        elif current_price <= fib_levels["61.8%"]:
            investable = True
            best_entry = current_price

        if investable:
            print("\n✅ Investment Decision: YES")
            print(f"Best Entry Price: ${best_entry:.6f}")
            print("\n**Profit-Taking Strategy:**")
            print("- Sell 40% at 2x to cover your initial investment.")
            print("- Hold remaining for potential 3x gains.")
            print("- Set stop-loss at 30% below entry price.")
        else:
            print("\n❌ Investment Decision: NO")
            print("Reason: Current price is not in an ideal entry zone.")
    else:
        print("Error: Unable to fetch valid data for the token.")

# Main function
def main():
    # Prompt user for token contract address
    contract_address = input("Enter the token contract address: ")
    analyze_token(contract_address)

if __name__ == "__main__":
    main()
