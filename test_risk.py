from services.risk import monte_carlo_simulation, calculate_risk_score

# Example expected return 8% with 5% volatility
simulated = monte_carlo_simulation(0.08, 0.05)

risk_result = calculate_risk_score(simulated)

print("Risk Analysis:", risk_result)