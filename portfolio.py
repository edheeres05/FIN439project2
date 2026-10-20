"""Lab 14: reusable portfolio return and risk engine. Standard library only."""
from math import isclose, isfinite, sqrt

# Course-authored training inputs, not estimates of current market returns.
ASSETS = {
    "Treasury bills": {"return": 0.035, "volatility": 0.005},
    "Treasury 10-year note": {"return": 0.043, "volatility": 0.070},
    "Investment-grade bond fund": {"return": 0.050, "volatility": 0.060},
    "Global equity index fund": {"return": 0.080, "volatility": 0.160},
}
# Rows/columns ordered as ASSETS: bills, 10-year, IG, equity.
CORRELATIONS = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
]
OBJECTIVE_RETURN = 0.065  # Estimated CPI 2.5% + 4%
RESERVE_ASSETS = ("Treasury bills", "Treasury 10-year note")


def validate_inputs(assets=ASSETS, correlations=CORRELATIONS):
    """Check correlation bounds, symmetry, dimensions, and volatilities."""
    names = list(assets)
    if len(correlations) != len(names) or any(len(row) != len(names) for row in correlations):
        raise ValueError("Correlation table must be square and match the asset list.")
    for name, values in assets.items():
        if not isfinite(values["return"]) or not isfinite(values["volatility"]):
            raise ValueError(f"Return and volatility must be finite for {name}.")
        if values["volatility"] <= 0:
            raise ValueError(f"Volatility must be positive for {name}.")
    for i in range(len(names)):
        for j in range(len(names)):
            r = correlations[i][j]
            if not isfinite(r) or not -1 <= r <= 1:
                raise ValueError(f"Invalid correlation for {names[i]} and {names[j]}: {r}. Must be between -1 and 1.")
            if not isclose(r, correlations[j][i], rel_tol=0, abs_tol=1e-12):
                raise ValueError(f"Correlation table is not symmetric: {names[i]} / {names[j]}.")
        if not isclose(correlations[i][i], 1.0, rel_tol=0, abs_tol=1e-12):
            raise ValueError(f"Self-correlation must equal 1 for {names[i]}.")


def covariance_matrix(assets=ASSETS, correlations=CORRELATIONS):
    """covariance[i][j] = correlation[i][j] * volatility[i] * volatility[j]."""
    validate_inputs(assets, correlations)
    names = list(assets)
    return [[correlations[i][j] * assets[names[i]]["volatility"] *
             assets[names[j]]["volatility"] for j in range(len(names))]
            for i in range(len(names))]


def benchmark_weights(assets=ASSETS):
    return {name: (0.40 if name == "Investment-grade bond fund"
                   else 0.60 if name == "Global equity index fund" else 0.0)
            for name in assets}


def equal_weight_weights(assets=ASSETS):
    return {name: 1 / len(assets) for name in assets}


def inverse_volatility_weights(assets=ASSETS):
    inverse = {name: 1 / values["volatility"] for name, values in assets.items()}
    total = sum(inverse.values())
    return {name: weight / total for name, weight in inverse.items()}


def validate_weights(weights, assets=ASSETS):
    if set(weights) != set(assets):
        raise ValueError("Weights must include exactly the listed assets.")
    if any(not isfinite(w) or w < 0 for w in weights.values()):
        raise ValueError("Weights must be nonnegative and finite.")
    if not isclose(sum(weights.values()), 1.0, rel_tol=0, abs_tol=1e-10):
        raise ValueError("Weights must sum to 100%.")


def expected_return(weights, assets=ASSETS):
    validate_weights(weights, assets)
    return sum(weight * assets[name]["return"] for name, weight in weights.items())


def portfolio_variance(weights, covariance, assets=ASSETS):
    """Sum over all pairs; includes both cross-asset covariance terms."""
    validate_weights(weights, assets)
    names = list(assets)
    return sum(weights[names[i]] * weights[names[j]] * covariance[i][j]
               for i in range(len(names)) for j in range(len(names)))


def portfolio_volatility(weights, covariance, assets=ASSETS):
    variance = portfolio_variance(weights, covariance, assets)
    if variance < -1e-12:
        raise ValueError("Negative portfolio variance; check correlation inputs.")
    return sqrt(max(variance, 0.0))


def reserve_weight(weights):
    return sum(weights[name] for name in RESERVE_ASSETS)


def meets_objective(value, objective=OBJECTIVE_RETURN):
    return value >= objective


def main():
    covariance = covariance_matrix()
    portfolios = {
        "Benchmark": benchmark_weights(),
        "Equal weight": equal_weight_weights(),
        "Inverse volatility": inverse_volatility_weights(),
    }
    print(f"Meridian training inputs | Return objective: {OBJECTIVE_RETURN:.2%}")
    print("Weights order: bills / 10-year / IG bonds / equity")
    for name, weights in portfolios.items():
        ret = expected_return(weights)
        volatility = portfolio_volatility(weights, covariance)
        print(f"\n{name}")
        print("Weights: " + " / ".join(f"{w * 100:.1f}%" for w in weights.values()))
        print(f"Expected return: {ret:.2%}")
        print(f"Volatility: {volatility:.2%}")
        print(f"Reserve-eligible: {reserve_weight(weights):.1%}")
        print(f"Meets return objective: {'yes' if meets_objective(ret) else 'no'}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        raise SystemExit(f"Input error: {error}")
