import numpy as np


def monte_carlo_simulation(expected_return, volatility, simulations=1000):

    simulated_returns = np.random.normal(
        expected_return,
        volatility,
        simulations
    )

    return simulated_returns.tolist()   # convert to normal list

def calculate_risk_score(simulated_returns):
    probability_of_loss = float(np.mean(np.array(simulated_returns) < 0))

    if probability_of_loss < 0.2:
        risk_level = "Low"
    elif probability_of_loss < 0.4:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "probability_of_loss": round(probability_of_loss * 100, 2),
        "risk_level": risk_level
    }