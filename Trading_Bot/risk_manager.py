def calculate_position_size(balance, risk_pct, stop_loss_pct):
    risk_amount = balance * risk_pct
    position_size = risk_amount / stop_loss_pct
    return round(position_size, 4)
