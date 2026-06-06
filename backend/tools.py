def calculate_sip(monthly_investment, annual_rate, years):
    
    # Convert annual return rate to monthly and from percentage to decimal
    r= annual_rate / 12 / 100
    n = years * 12
    future_value = monthly_investment * ((((1 + r) ** n)- 1) / r) * (1 + r)
    invested = monthly_investment * n
    returns = future_value - invested
    return {
        "monthly_investment": monthly_investment,
        "future_value": round(future_value, 2),
        "invested": round(invested, 2),
        "returns": round(returns, 2)
    }   
    
def calculate_emi (principal, annual_rate, years):
    r = annual_rate / 100 / 12
    n = years * 12
    emi = principal * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
    total= emi * n
    interest = total - principal
    return {
        "emi": round(emi, 2),
        "total_payment": round(total, 2),
        "interest": round(interest, 2),
        "principal": principal
    }
    
def calculate_cagr(initial_value, final_value, years):
    cagr = ((final_value / initial_value) ** (1 / years) - 1) * 100
    return {
        "initial_value": initial_value,
        "final_value": final_value,
        "years": years,
        "cagr_%": round(cagr, 2)
    }

def calculate_fd(principal, annual_rate, years):
    amount= principal * ((1 + annual_rate / 100)** years)
    interest = amount - principal
    return {
        "principal": principal,
        "amount": round(amount, 2),
        "interest": round(interest, 2),
        "annual_rate": annual_rate,
    }