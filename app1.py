import streamlit as st
import pandas as pd


class CreditAnalysisApp:
    def __init__(self):
        # Placeholder for borrower data
        self.borrowers_data = pd.DataFrame()

    def add_borrower_data(self, borrower_info):
        """Add borrower data to the DataFrame"""
        new_data = pd.DataFrame([borrower_info])
        self.borrowers_data = pd.concat([self.borrowers_data, new_data], ignore_index=True)

    def calculate_financial_ratios(self, borrower_id):
        """Calculate key financial ratios for a given borrower"""
        borrower = self.borrowers_data.loc[self.borrowers_data['id'] == borrower_id]
        if borrower.empty:
            return "Borrower not found"

        try:
            debt_to_equity_ratio = borrower['total_debt'] / borrower['total_equity']
            current_ratio = borrower['current_assets'] / borrower['current_liabilities']
            dscr = borrower['ebit'] / borrower['interest_expense']
            return {
                "Debt to Equity Ratio": debt_to_equity_ratio.values[0],
                "Current Ratio": current_ratio.values[0],
                "Debt Service Coverage Ratio": dscr.values[0]
            }
        except KeyError as e:
            return f"Missing data for calculation: {e}"

    def credit_score_model(self, financial_ratios):
        """A simple credit scoring model based on financial ratios"""
        score = 0
        if financial_ratios["Debt to Equity Ratio"] < 2:
            score += 1
        if financial_ratios["Current Ratio"] > 1:
            score += 1
        if financial_ratios["Debt Service Coverage Ratio"] > 1.2:
            score += 2
        return "High" if score >= 3 else "Medium" if score == 2 else "Low"

    def make_lending_decision(self, borrower_id):
        """Make a lending decision based on the borrower's credit score"""
        financial_ratios = self.calculate_financial_ratios(borrower_id)
        if isinstance(financial_ratios, str):
            return financial_ratios
        credit_score = self.credit_score_model(financial_ratios)
        decision = "Approve" if credit_score == "High" else "Review" if credit_score == "Medium" else "Decline"
        return f"Lending Decision: {decision}"


app = CreditAnalysisApp()

st.title('Credit Analysis Application')

with st.form("borrower_data_form"):
    st.write("Enter borrower's data:")
    id = st.number_input('ID', step=1, format="%d")
    name = st.text_input('Name')
    total_debt = st.number_input('Total Debt')
    total_equity = st.number_input('Total Equity')
    current_assets = st.number_input('Current Assets')
    current_liabilities = st.number_input('Current Liabilities')
    ebit = st.number_input('EBIT')
    interest_expense = st.number_input('Interest Expense')

    submitted = st.form_submit_button("Submit")
    if submitted:
        borrower_info = {
            'id': id,
            'name': name,
            'total_debt': total_debt,
            'total_equity': total_equity,
            'current_assets': current_assets,
            'current_liabilities': current_liabilities,
            'ebit': ebit,
            'interest_expense': interest_expense
        }
        app.add_borrower_data(borrower_info)
        decision = app.make_lending_decision(id)
        st.write(decision)
