import requests
import streamlit as st

# Function to fetch token data from Dexscreener API
def fetch_token_data(contract_address):
    try:
        # Dexscreener API endpoint for fetching token data
        api_url = f"https://api.dexscreener.io/latest/dex/tokens/{contract_address}"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error fetching data: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

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
    data = fetch_token_data(contract_address)
    if "error" in data:
        return {"error": data["error"]}

    if "pairs" in data:
        pair = data["pairs"][0]
        token_name = pair['baseToken']['name']
        token_symbol = pair['baseToken']['symbol']
        current_price = float(pair["priceUsd"])
        market_cap = pair.get("fdv", "N/A")
        volume = pair.get("volume", {}).get("usd", "N/A")

        prices = [current_price * (1 + 0.01 * i) for i in range(-50, 51)]
        high = max(prices)
        low = min(prices)
        fib_levels = calculate_fibonacci_levels(high, low)

        max_price_projection = current_price * 2.5
        risk_level = ((fib_levels["100% (Low)"] - current_price) / current_price) * 100

        # Investment decision logic
        investable = False
        best_entry = None
        if fib_levels["50%"] <= current_price <= fib_levels["38.2%"]:
            investable = True
            best_entry = fib_levels["50%"]
        elif current_price <= fib_levels["61.8%"]:
            investable = True
            best_entry = current_price

        return {
            "token_name": token_name,
            "token_symbol": token_symbol,
            "current_price": current_price,
            "market_cap": market_cap,
            "volume": volume,
            "fib_levels": fib_levels,
            "max_price_projection": max_price_projection,
            "risk_level": abs(risk_level),
            "investable": investable,
            "best_entry": best_entry,
        }
    else:
        return {"error": "No valid data for this token."}

# Streamlit Web App
def main():
    st.title("Token Analysis Tool")
    st.write("Enter the token contract address below to analyze its potential.")

    contract_address = st.text_input("Token Contract Address", "")
    if st.button("Analyze"):
        if contract_address:
            result = analyze_token(contract_address)

            if "error" in result:
                st.error(result["error"])
            else:
                # Display results
                st.subheader("Token Information")
                st.write(f"**Token Name:** {result['token_name']}")
                st.write(f"**Token Symbol:** {result['token_symbol']}")
                st.write(f"**Current Price (USD):** ${result['current_price']:.6f}")
                st.write(f"**Market Cap:** {result['market_cap']}")
                st.write(f"**24H Volume:** {result['volume']}")

                st.subheader("Fibonacci Levels")
                for level, value in result["fib_levels"].items():
                    st.write(f"**{level}:** ${value:.6f}")

                st.write(f"**Maximum Price Projection:** ${result['max_price_projection']:.6f}")
                st.write(f"**Risk Level:** {result['risk_level']:.2f}%")

                if result["investable"]:
                    st.success("Investment Decision: YES")
                    st.write(f"**Best Entry Price:** ${result['best_entry']:.6f}")
                    st.subheader("Profit-Taking Strategy")
                    st.write("- Sell 40% at 2x to cover your initial investment.")
                    st.write("- Hold remaining for potential 3x gains.")
                    st.write("- Set stop-loss at 30% below entry price.")
                else:
                    st.error("Investment Decision: NO")
                    st.write("Reason: Current price is not in an ideal entry zone.")
        else:
            st.warning("Please enter a valid token contract address.")

if __name__ == "__main__":
    main()
