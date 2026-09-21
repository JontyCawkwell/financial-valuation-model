import matplotlib.pyplot as plt


def plot_valuation_comparison(
    current_price: float,
    dcf_price: float,
    ev_ebitda_price: float,
    pe_price: float,
) -> None:
    """Plot current share price against implied valuation prices."""

    labels = [
        "Current Share Price",
        "DCF",
        "EV/EBITDA",
        "P/E",
    ]

    values = [
        current_price,
        dcf_price,
        ev_ebitda_price,
        pe_price,
    ]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)

    plt.ylabel("Share Price ($)")
    plt.title("Valuation Comparison")
    plt.tight_layout()
    plt.show()