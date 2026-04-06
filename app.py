import requests
import streamlit as st

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"


@st.cache_data(ttl=3600)
def fetch_rates(url: str) -> dict:
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.json()


def convert_currency(rates: dict, from_currency: str, to_currency: str, amount: float) -> float:
    if from_currency not in rates:
        raise ValueError("Invalid from_currency")
    if to_currency not in rates:
        raise ValueError("Invalid to_currency")

    if from_currency != "USD":
        amount = amount / rates[from_currency]
    return round(amount * rates[to_currency], 6)


def main() -> None:
    st.set_page_config(page_title="Currency Converter", page_icon="💱", layout="centered")

    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #1D4ED8 0%, #1E40AF 52%, #0F2C7A 100%);
        }
        .main-card {
            background: #EFF6FF;
            border: 2px solid #BFDBFE;
            border-radius: 18px;
            padding: 22px;
            color: #0F172A;
        }
        .headline {
            color: white;
            text-align: center;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.1rem;
        }
        .subline {
            color: #DBEAFE;
            text-align: center;
            margin-bottom: 1.3rem;
        }
        .result-box {
            background: white;
            border-radius: 10px;
            border: 2px solid #93C5FD;
            padding: 0.75rem;
            font-size: 1.1rem;
            font-weight: 700;
            text-align: center;
            color: #0F172A;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="headline">Real Time Currency Converter</div>', unsafe_allow_html=True)
    st.markdown('<div class="subline">Fast conversion with live exchange rates</div>', unsafe_allow_html=True)

    try:
        data = fetch_rates(API_URL)
        rates = data["rates"]
        update_date = data["date"]
    except Exception as exc:
        st.error(f"Could not fetch exchange rates: {exc}")
        return

    currencies = sorted(rates.keys())
    usd_to_inr = convert_currency(rates, "USD", "INR", 1)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(f"**1 USD = {usd_to_inr} INR**")
    st.caption(f"Updated: {update_date}")

    col1, col2 = st.columns(2)
    with col1:
        from_currency = st.selectbox("From", currencies, index=currencies.index("INR") if "INR" in currencies else 0)
        amount = st.number_input("Amount", min_value=0.0, value=1.0, format="%.6f")
    with col2:
        to_currency = st.selectbox("To", currencies, index=currencies.index("USD") if "USD" in currencies else 0)

    if st.button("Convert", use_container_width=True, type="primary"):
        converted = convert_currency(rates, from_currency, to_currency, float(amount))
        st.markdown(f'<div class="result-box">{converted:.6f}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
