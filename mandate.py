from math import isclose

# Editable inputs: weights are percentages, money is USD millions.
holdings = {
    "Cash": {"issuer": None, "days": 0, "reserve_eligible": True},
    "Treasury bills": {
        "issuer": "U.S. Treasury", "days": 1, "reserve_eligible": True
    },
    "Treasury 10-year note": {
        "issuer": "U.S. Treasury", "days": 1, "reserve_eligible": True
    },
    "Global equity index fund": {
        "issuer": "diversified fund", "days": 2, "reserve_eligible": False
    },
    "Investment-grade bond fund": {
        "issuer": "diversified fund", "days": 3, "reserve_eligible": False
    },
    "Private real estate fund": {
        "issuer": "diversified fund", "days": 90, "reserve_eligible": False
    },
    "Acme Corp bonds": {
        "issuer": "Acme Corp", "days": 4, "reserve_eligible": False
    },
    "Acme Corp stock": {
        "issuer": "Acme Corp", "days": 1, "reserve_eligible": False
    },
}

candidates = {
    "A": {
        "Cash": 2,
        "Treasury bills": 2,
        "Treasury 10-year note": 10,
        "Global equity index fund": 60,
        "Investment-grade bond fund": 26,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1,
        "Treasury bills": 0,
        "Treasury 10-year note": 0,
        "Global equity index fund": 55,
        "Investment-grade bond fund": 20,
        "Private real estate fund": 15,
        "Acme Corp bonds": 5,
        "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1,
        "Treasury bills": 1,
        "Treasury 10-year note": 0,
        "Global equity index fund": 70,
        "Investment-grade bond fund": 20,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 8,
    },
    "D": {
        "Cash": 3,
        "Treasury bills": 0,
        "Treasury 10-year note": 0,
        "Global equity index fund": 97,
        "Investment-grade bond fund": 0,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
}

reserve_size = 100
quarterly_distribution = 0.75
quarters_to_cover = 4
liquidity_window = 5
minimum_liquid_share = 90
issuer_limit = 8
exempt_issuers = {None, "U.S. Treasury", "diversified fund"}


def check_portfolio(weights, reserve_minimum):
    total_weight = sum(weights.values())
    lowest_weight = min(weights.values())

    reserve_weight = sum(
        weight for name, weight in weights.items()
        if holdings[name]["reserve_eligible"]
    )

    liquid_weight = sum(
        weight for name, weight in weights.items()
        if holdings[name]["days"] <= liquidity_window
    )

    company_weights = {}
    for name, weight in weights.items():
        issuer = holdings[name]["issuer"]
        if issuer not in exempt_issuers:
            company_weights[issuer] = company_weights.get(issuer, 0) + weight

    largest_company = max(company_weights.values(), default=0)

    return [
        (
            "Weights sum to 100",
            total_weight,
            isclose(total_weight, 100, rel_tol=0, abs_tol=1e-9),
        ),
        ("Long-only (lowest weight)", lowest_weight, lowest_weight >= 0),
        (
            f"Reserve >= {reserve_minimum:.1f}%",
            reserve_weight,
            reserve_weight >= reserve_minimum,
        ),
        (
            f"Redeemable in {liquidity_window} days >= {minimum_liquid_share:.1f}%",
            liquid_weight,
            liquid_weight >= minimum_liquid_share,
        ),
        (
            f"Largest single company <= {issuer_limit:.1f}%",
            largest_company,
            largest_company <= issuer_limit,
        ),
    ]


def main():
    reserve_minimum = (
        quarters_to_cover * quarterly_distribution / reserve_size * 100
    )
    print(f"Reserve minimum: {reserve_minimum:.1f}%")

    for candidate, weights in candidates.items():
        print(f"\nCandidate {candidate}")
        checks = check_portfolio(weights, reserve_minimum)
        failures = 0

        for label, value, passed in checks:
            status = "pass" if passed else "FAIL"
            print(f"{label}: {value:.1f} {status}")
            if not passed:
                failures += 1

        print("Calendar-year loss: requires CIO clarification")

        if failures == 0:
            print("passes every checkable rule")
        else:
            print(f"fails {failures} rule(s)")


if __name__ == "__main__":
    main()
