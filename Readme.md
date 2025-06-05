# 💊 PrescribeAI: Medical Prescription Pattern Analysis

**Live Application:** [https://prescribe-ai.streamlit.app/](https://prescribe-ai.streamlit.app/)

## Project Overview

**PrescribeAI** is a Streamlit web application that utilizes **Association Rule Mining** to uncover interesting patterns and relationships within medical prescription data. Inspired by "market basket analysis," this project helps identify which medications are frequently co-prescribed, providing insights into common treatment regimens or potential (though strictly hypothetical in this simulated data) drug interactions.

The application allows users to upload a CSV file containing prescription records and interactively adjust key parameters (Support, Confidence, and Lift) to discover meaningful association rules.

## Features

- **Data Upload:** Easily upload your `fake_prescriptions.csv` (or similar structured CSV) file.
- **Interactive Parameter Adjustment:** Sliders for Minimum Support, Minimum Confidence, and Minimum Lift to dynamically filter and explore association rules.
- **Frequent Itemsets Display:** Visualize combinations of drugs that frequently appear together.
- **Association Rules Display:** See the derived rules (e.g., `{Drug A} -> {Drug B}`) along with their support, confidence, and lift metrics.
- **Clear Explanations:** Understand the meaning and importance of the key metrics.

## How It Works

The application employs the **Apriori Algorithm** to perform Association Rule Mining:

1.  **Data Preprocessing:** The uploaded prescription data is transformed into a transaction-based format, where each prescription is treated as a 'basket' of drugs.
2.  **Frequent Itemset Generation:** The Apriori algorithm identifies `frequent itemsets` – combinations of drugs that appear together above a specified `Minimum Support` threshold.
3.  **Association Rule Generation:** From these frequent itemsets, `association rules` are generated. These rules are then filtered based on `Minimum Confidence` and `Minimum Lift` values.

## Key Metrics Explained

- **Support:**

  - Indicates how frequently an itemset (a combination of drugs) appears in the entire dataset.
  - A higher support means the drug combination is more popular or common.
  - **Use in App:** Configurable via "Minimum Support" slider to focus on common patterns.

- **Confidence:**

  - Measures how often the rule 'if Antecedent then Consequent' is true. Specifically, it's the probability that the Consequent drugs are prescribed _given_ that the Antecedent drugs were prescribed. (P(B|A)).
  - A high confidence suggests a strong likelihood of the Consequent following the Antecedent.
  - **Use in App:** Configurable via "Minimum Confidence" slider to ensure rules are reliable.

- **Lift:**
  - Evaluates how much more likely the Consequent drugs are prescribed _when the Antecedent drugs are also prescribed_, compared to the Consequent drugs being prescribed purely by chance (its overall frequency).
  - **Lift > 1:** Indicates a **positive correlation**; the drugs appear together more often than expected, suggesting a meaningful association. This is what we typically seek.
  - **Lift = 1:** Indicates **no correlation** (independence).
  - **Lift < 1:** Indicates a **negative correlation**; the drugs appear together less often than expected.
  - **Use in App:** Configurable via "Minimum Lift" slider to identify truly interesting and non-random relationships.

## Potential Applications

- **Clinical Decision Support:** Help doctors identify common co-prescriptions for certain conditions.
- **Pharmacovigilance (Drug Safety):** Potentially highlight unusual combinations that might warrant further investigation for adverse drug reactions (though this requires medical expertise and real data).
- **Inventory Management for Pharmacies:** Understand which drugs are frequently dispensed together to optimize stock.
- **Drug Development:** Inform research into new drug combinations or therapeutic areas.

## Setup and Local Installation

To run this project locally, follow these steps:

1.  **Clone the repository (if applicable) or create your project directory:**

    ```bash
    mkdir PrescribeAI
    cd PrescribeAI
    ```

2.  **Create your `app.py` file:**
    Save the Streamlit application code (provided previously) as `app.py` inside the `PrescribeAI` directory.

3.  **Create your `requirements.txt` file:**
    In the same `PrescribeAI` directory, create a file named `requirements.txt` and add the following content:

    ```
    streamlit
    pandas
    mlxtend
    ```

4.  **Install the required libraries:**
    Open your terminal or command prompt, navigate to the `PrescribeAI` directory, and run:

    ```bash
    pip install -r requirements.txt
    ```

5.  **Generate a `fake_prescriptions.csv` file:**
    You'll need a CSV file to upload. Use the Python script provided earlier to generate `fake_prescriptions.csv` and place it in the same directory as `app.py` (or somewhere you can easily browse to).

6.  **Run the Streamlit application:**
    From your terminal in the `PrescribeAI` directory, execute:
    ```bash
    streamlit run app.py
    ```
    This will open the application in your default web browser.

## Dataset

The project utilizes a **synthetic dataset**, `prescriptions.csv`, generated using the `Faker` library. This dataset simulates medical prescriptions and contains columns such as `PatientID`, `PrescriptionID`, `PrescriptionDate`, `Condition`, `PatientAge`, `PatientGender`, and `DrugsPrescribed` (a comma-separated string of medications).

**Note:** This dataset is purely for demonstration and educational purposes. It does not contain real patient data and should not be used for actual medical analysis or decision-making.

---

Feel free to explore the app, adjust the parameters, and gain insights into the fascinating world of association rule mining!
