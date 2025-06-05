# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 15:19:45 2025

@author: dheer
"""

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import streamlit as st
import io

# Set Streamlit page configuration for better aesthetics
st.set_page_config(
    page_title="Prescription Data Analysis",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a cleaner look and feel
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5em;
        color: #2F80ED;
        text-align: center;
        margin-bottom: 30px;
    }
    .stSlider > div > div > div:nth-child(2) {
        background-color: #2F80ED;
    }
    .stButton > button {
        background-color: #2F80ED;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 1.1em;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #56CCF2;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_and_preprocess_data(uploaded_file_buffer):
    """
    Loads the f dataset from the uploaded file buffer and preprocesses it
    for association rule mining. This function is cached to prevent re-running
    on every interaction.

    Args:
        uploaded_file_buffer (io.BytesIO): The buffer containing the uploaded CSV file.

    Returns:
        tuple: A tuple containing:
            - pd.DataFrame: The one-hot encoded DataFrame suitable for Apriori.
            - list: The original list of transactions (list of lists of drugs).
            - pd.DataFrame: The raw DataFrame loaded from the CSV.
    """
    # Read the CSV into a pandas DataFrame
    df = pd.read_csv(uploaded_file_buffer)

    # Convert the 'DrugsPrescribed' string into a list of drugs.
    # Each prescription is treated as a 'transaction'.
    # .apply(lambda x: [item.strip() for item in str(x).split(',') if item.strip()])
    # The str(x) handles potential non-string types, and the final if ensures no empty strings.
    df['DrugsPrescribedList'] = df['DrugsPrescribed'].apply(
        lambda x: [item.strip() for item in str(x).split(',') if item.strip()]
    )

    # Create a list of lists (transactions) for TransactionEncoder.
    # This is the format required by mlxtend's TransactionEncoder.
    transactions = df['DrugsPrescribedList'].tolist()

    # Initialize TransactionEncoder to convert transactions into a one-hot encoded format.
    te = TransactionEncoder()
    # Fit the encoder to the transactions to learn all unique items (drugs).
    te_ary = te.fit(transactions).transform(transactions)
    # Create a DataFrame from the one-hot encoded array, with drug names as column headers.
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

    return df_encoded, transactions, df

# --- Streamlit Application Layout ---

st.markdown("<h1 class='main-header'>💊 Medical Prescription Data Analysis</h1>", unsafe_allow_html=True)

st.write(
    """
    This application helps you uncover hidden patterns in medical prescription data using
    **Association Rule Mining**. Upload your `prescriptions.csv` file to identify
    frequently co-prescribed medications and interesting drug combinations.
    """
)

# File uploader widget
uploaded_file = st.file_uploader("Upload your `prescriptions.csv` file here", type="csv")

if uploaded_file is not None:
    # Use io.BytesIO to handle the uploaded file, allowing it to be read by pandas
    bytes_data = io.BytesIO(uploaded_file.getvalue())

    # Load and preprocess the data using the cached function
    df_encoded, transactions, df_raw = load_and_preprocess_data(bytes_data)

    st.success("File uploaded and preprocessed successfully!")

    # Sidebar for parameters
    st.sidebar.header("Analysis Parameters")
    st.sidebar.write("Adjust the sliders to fine-tune the association rule mining.")

    # Sliders for Apriori and Association Rules parameters
    min_support = st.sidebar.slider(
        "Minimum Support (for Frequent Itemsets)",
        min_value=0.001,  # Lower min to find more rules in potentially sparse data
        max_value=1.0,
        value=0.05,
        step=0.001,
        help="Support indicates the popularity of an itemset. It's the proportion of transactions containing the itemset."
    )
    min_confidence = st.sidebar.slider(
        "Minimum Confidence (for Association Rules)",
        min_value=0.01,
        max_value=1.0,
        value=0.5,
        step=0.01,
        help="Confidence indicates how often the rule 'if A then B' is true. It's P(B|A)."
    )
    min_lift = st.sidebar.slider(
        "Minimum Lift (for Association Rules)",
        min_value=0.0,
        max_value=5.0, # Adjusted max value for more realistic lift ranges
        value=1.0,
        step=0.01,
        help="Lift indicates how much more likely B is given A than B is without A. Lift > 1 suggests a positive association."
    )

    st.markdown("---") # Separator

    # --- Frequent Itemsets Section ---
    st.subheader("📊 Frequent Itemsets")
    st.info(f"Finding itemsets that appear in at least **{min_support:.1%}** of all prescriptions.")
    
    # Apply the Apriori algorithm to find frequent itemsets
    # `use_colnames=True` ensures the output DataFrame uses drug names instead of column indices.
    frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)

    if not frequent_itemsets.empty:
        # Sort by support in descending order for better readability
        frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
        st.dataframe(frequent_itemsets.sort_values(by='support', ascending=False).reset_index(drop=True))
        st.write(f"Found {len(frequent_itemsets)} frequent itemsets.")
    else:
        st.warning("No frequent itemsets found with the current minimum support. Try decreasing it.")

    st.markdown("---") # Separator

    # --- Association Rules Section ---
    st.subheader("🔗 Discovered Association Rules")
    st.info(f"Generating rules with at least **{min_confidence:.1%}** confidence and **{min_lift:.2f}** lift.")

    if not frequent_itemsets.empty:
        # Generate association rules from the frequent itemsets
        # We start by filtering on confidence, then apply lift.
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

        # Filter rules further based on the minimum lift threshold
        rules = rules[rules['lift'] >= min_lift]

        if not rules.empty:
            # Sort rules by lift (descending) and then confidence (descending) for best insights
            rules = rules.sort_values(by=['lift', 'confidence'], ascending=[False, False]).reset_index(drop=True)

            # Format the 'antecedents' and 'consequents' columns for better display
            rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
            rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))

            st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
            st.write(f"Found {len(rules)} association rules.")

            st.markdown(
                """
                **Understanding the Metrics:**
                - **Support:** How often the itemset appears in the dataset.
                - **Confidence:** How often the rule is true (if A then B).
                - **Lift:** How much more likely B is given A than B is without A.
                  - Lift > 1: Positive correlation (A and B appear together more often than expected).
                  - Lift = 1: No correlation (A and B are independent).
                  - Lift < 1: Negative correlation (A and B appear together less often than expected).
                """
            )
        else:
            st.warning("No association rules found with the current thresholds. Try adjusting the sliders.")
    else:
        st.warning("Cannot generate association rules because no frequent itemsets were found.")

    st.markdown("---") # Separator

    # --- Raw Data Sample Section ---
    st.subheader("📋 Raw Data Sample")
    st.write("First 10 rows of the uploaded and processed prescription data:")
    st.dataframe(df_raw.head(10))

else:
    st.info("Please upload your `prescriptions.csv` file to begin the analysis.")

