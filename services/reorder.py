def calculate_reorder(current_stock, forecast_demand, safety_stock=0):
    """Suggested order quantity: forecast demand + safety stock - current stock."""
    return max(0, int(forecast_demand) + int(safety_stock) - int(current_stock))
