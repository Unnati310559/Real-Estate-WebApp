from services.financial import calculate_noi, calculate_cap_rate, calculate_cashflow, calculate_roi, calculate_irr

# Sample Inputs
purchase_price = 400000
annual_rent = 36000
annual_expenses = 10000
annual_loan_payment = 15000
years = 5

noi = calculate_noi(annual_rent, annual_expenses)
cap_rate = calculate_cap_rate(noi, purchase_price)
cashflow = calculate_cashflow(annual_rent, annual_expenses, annual_loan_payment)
roi = calculate_roi(cashflow * years, purchase_price)
irr = calculate_irr(purchase_price, cashflow, years)

print("NOI:", noi)
print("Cap Rate:", cap_rate)
print("Annual Cashflow:", cashflow)
print("ROI:", roi)
print("IRR:", irr)