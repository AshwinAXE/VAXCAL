import streamlit as st
import pandas as pd
import urllib.parse

# --- Page Config ---
st.set_page_config(
    page_title="Vaccination Earnings Calculator",
    layout="centered",
    page_icon="💉"
)

# --- Title ---
st.title("💉 Vaccination Potential Earnings Calculator")
st.markdown("Use this tool to estimate the potential financial impact of vaccination services offered in your pharmacy.")

st.markdown("---")

# --- Vaccine Pricing Defaults ---
vaccine_prices = {
    "Influenza": 19.32,
    "COVID-19": 27.35,
    "COVID-19 (site visit)": 122.4,
    "Pneumococcal": 19.32,
    "Respiratory Syncytial Virus (RSV)": 19.32,
    "Measles, mumps, rubella": 19.32,
    "Diphtheria, tetanus, pertussis": 19.32,
    "Shingles": 19.32,
    "Hepatitis A": 19.32,
    "Hepatitis B": 19.32,
    "Typhoid": 19.32,
    "Human papillomavirus": 19.32,
    "Japanese encephalitis": 19.32,
    "Meningococcal ACWY": 19.32,
    "Meningococcal B": 19.32,
    "Meningococcal C": 19.32,
    "Mpox (Monkeypox)": 19.32,
    "Poliomyelitis": 19.32,
    "Varicella": 19.32,
    "Rabies": 19.32
}

# --- Sidebar Pricing Customisation ---
st.sidebar.header("💰 Customise Vaccine Pricing")
custom_prices = {}
for vaccine, price in vaccine_prices.items():
    custom_prices[vaccine] = st.sidebar.number_input(f"{vaccine}", value=price, min_value=0.0)

# --- Input Form ---
with st.form("calculator_form"):
    st.markdown("### 🧮 Calculation Inputs")

    col1, col2 = st.columns(2)
    with col1:
        main_vaccine = st.selectbox("Main Vaccine", list(vaccine_prices.keys()))
    with col2:
        coadmin_vaccine = st.selectbox("Optional Co-admin Vaccine", ["None"] + list(vaccine_prices.keys()))

    col3, col4 = st.columns(2)
    with col3:
        target_patients = st.number_input("🎯 Target Patients", min_value=0, value=100)
    with col4:
        include_stock_cost = st.checkbox("Include Stock Cost")
        stock_cost = st.number_input("💸 Total Stock Cost ($)", min_value=0.0, value=100.0) if include_stock_cost else 0.0

    include_basket_size = st.checkbox("🛒 Include Basket Size")
    basket_size = st.number_input("Avg. Basket Size per Patient ($)", min_value=0.0, value=10.0) if include_basket_size else 0.0

    submitted = st.form_submit_button("Calculate Earnings")

# --- Calculation Logic ---
if submitted:
    main_vaccine_price = custom_prices.get(main_vaccine, 0)
    coadmin_vaccine_price = custom_prices.get(coadmin_vaccine, 0) if coadmin_vaccine != "None" else 0
    total_earnings = ((main_vaccine_price + coadmin_vaccine_price + basket_size) * target_patients) - stock_cost

    st.markdown("### 💡 Results")

    # Show as metric
    st.metric(label="💰 Estimated Potential Earnings", value=f"${total_earnings:,.2f}")

    # Break-even calc
    if include_stock_cost and (main_vaccine_price + coadmin_vaccine_price + basket_size) > 0:
        break_even_patients = stock_cost / (main_vaccine_price + coadmin_vaccine_price + basket_size)
        st.markdown(f"📊 **Break-even Patients:** {break_even_patients:.0f}")

    # Show breakdown table
    st.markdown("### 📊 Breakdown")
    df = pd.DataFrame({
        "Component": ["Main Vaccine", "Co-admin Vaccine", "Basket Size", "Stock Cost", "Target Patients", "Total Earnings"],
        "Value": [
            f"${main_vaccine_price:,.2f}",
            f"${coadmin_vaccine_price:,.2f}" if coadmin_vaccine != "None" else "N/A",
            f"${basket_size:,.2f}" if include_basket_size else "N/A",
            f"${stock_cost:,.2f}" if include_stock_cost else "$0.00",
            target_patients,
            f"${total_earnings:,.2f}"
        ]
    })
    st.dataframe(df)

    # Email feature
    st.markdown("### 📧 Send Estimate by Email")
    recipient_email = st.text_input("Enter recipient email:")
    if recipient_email:
        email_body = f"""
Main Vaccine: {main_vaccine}
Secondary Vaccine: {coadmin_vaccine if coadmin_vaccine != 'None' else 'N/A'}
Target Patients: {target_patients}
Stock Cost: ${stock_cost:,.2f}
Basket Size: {'N/A' if not include_basket_size else f'${basket_size:,.2f}'}
Estimated Earnings: ${total_earnings:,.2f}
"""
        mailto_link = f"mailto:{recipient_email}?subject={urllib.parse.quote('Vaccination Earnings Estimate')}&body={urllib.parse.quote(email_body)}"
        st.markdown(f"""
            <a href="{mailto_link}" style="display: inline-block; padding: 10px 16px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">
            📩 Send Email
            </a>
        """, unsafe_allow_html=True)

# --- Disclaimer Footer ---
st.markdown("---")
st.markdown(
    """
    <div style="background-color: #f0f0f5; padding: 10px; border-radius: 5px; font-size: 0.85em;">
    ⚠️ <strong>Disclaimer:</strong> This tool is for estimation purposes only and does not guarantee actual revenue outcomes. Please validate all inputs before applying in a clinical or business setting.
    </div>
    """,
    unsafe_allow_html=True
)
