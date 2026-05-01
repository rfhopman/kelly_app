import streamlit as st

def calculate_kelly(win_prob, win_loss_ratio):
    # Kelly Formula: f* = (p * (b + 1) - 1) / b
    # Where b is the win/loss ratio (profit on win / loss on loss)
    p = win_prob / 100
    b = win_loss_ratio
    kelly_f = (p * (b + 1) - 1) / b
    return kelly_f

# UI Setup
st.set_page_config(page_title="Kelly Criterion Calculator", layout="centered")
st.title("📈 Kelly Criterion Investor")
st.write("Determine the optimal size of your next investment or trade.")

with st.sidebar:
    st.header("Parameters")
    win_prob = st.slider("Win Probability (%)", 0, 100, 50)
    win_loss_ratio = st.number_input("Win/Loss Ratio (Reward:Risk)", min_value=0.1, value=2.0, step=0.1)
    account_size = st.number_input("Total Account Balance ($)", min_value=0, value=10000)
    fractional_kelly = st.slider("Kelly Multiplier (Safety Factor)", 0.1, 1.0, 0.5, help="Many investors use 'Half-Kelly' (0.5) to reduce volatility.")

# Calculation
raw_kelly = calculate_kelly(win_prob, win_loss_ratio)
suggested_fraction = raw_kelly * fractional_kelly
investment_amount = account_size * suggested_fraction

# Display Results
st.divider()
col1, col2 = st.columns(2)

if raw_kelly <= 0:
    st.error("### ⚠️ Do Not Invest")
    st.write("The expected value is negative. Based on these parameters, this trade is likely to lose money over time.")
else:
    with col1:
        st.metric("Full Kelly %", f"{raw_kelly*100:.2f}%")
        st.metric("Adjusted Stake %", f"{suggested_fraction*100:.2f}%")
    
    with col2:
        st.metric("Suggested Investment", f"${investment_amount:,.2f}")
    
    st.info(f"**Strategy:** You should allocate **{suggested_fraction*100:.2f}%** of your capital to this position.")

st.expander("How this works").write("""
The Kelly Criterion maximizes the logarithm of wealth. 
- **Win Probability:** How often you expect to be right.
- **Win/Loss Ratio:** If you risk $100, how much do you make when you win? (e.g., 2.0 means you win $200).
- **Fractional Kelly:** Reduces the suggested bet size to protect against 'Black Swan' events or inaccurate probability estimates.
""")

# Specific logic for Iron Condors
st.subheader("Iron Condor Specifics")
wing_width = st.number_input("Wing Width ($)", value=5.0)
credit_received = st.number_input("Credit Received ($)", value=1.25)

# Calculate Risk and b
risk_per_spread = wing_width - credit_received
b_ratio = credit_received / risk_per_spread

# Update the Win Probability for 15-Delta
# Short Delta 0.15 on both sides = ~70% win rate
win_prob_ic = 70.0 

ic_kelly = calculate_kelly(win_prob_ic, b_ratio)
