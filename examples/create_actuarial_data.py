"""Create sample actuarial Excel file with multiple sheets."""

import random
from datetime import datetime, timedelta
from pathlib import Path

import polars as pl


def generate_life_table_data(num_ages: int = 101) -> pl.DataFrame:
    """Generate a life table with mortality rates by age."""
    ages = list(range(num_ages))
    
    # Simplified mortality rates (qx) - increases with age
    mortality_rates = []
    for age in ages:
        if age < 1:
            qx = 0.006  # Infant mortality
        elif age < 20:
            qx = 0.0005 + (age * 0.00001)
        elif age < 60:
            qx = 0.001 + ((age - 20) * 0.0002)
        else:
            qx = 0.009 + ((age - 60) * 0.01)
        mortality_rates.append(min(qx, 1.0))
    
    # Calculate survival probabilities
    survival_probs = [1 - qx for qx in mortality_rates]
    
    # Calculate life expectancy (simplified)
    life_expectancy = []
    for i in range(num_ages):
        remaining_years = max(0, 85 - i + random.uniform(-5, 5))
        life_expectancy.append(round(remaining_years, 2))
    
    return pl.DataFrame({
        "Age": ages,
        "Mortality_Rate_qx": [round(qx, 6) for qx in mortality_rates],
        "Survival_Probability_px": [round(px, 6) for px in survival_probs],
        "Life_Expectancy": life_expectancy,
        "Population_Count": [random.randint(50000, 100000) for _ in ages]
    })


def generate_policy_data(num_policies: int = 1000) -> pl.DataFrame:
    """Generate sample insurance policy data."""
    policy_types = ["Term Life", "Whole Life", "Universal Life", "Endowment", "Annuity"]
    genders = ["M", "F"]
    occupations = ["Professional", "Skilled", "Semi-skilled", "Hazardous", "Administrative"]
    
    policies = []
    for i in range(num_policies):
        issue_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1460))
        birth_date = issue_date - timedelta(days=random.randint(18*365, 70*365))
        age_at_issue = (issue_date - birth_date).days // 365
        
        policy = {
            "Policy_ID": f"POL{i+1:06d}",
            "Policy_Type": random.choice(policy_types),
            "Issue_Date": issue_date.strftime("%Y-%m-%d"),
            "Birth_Date": birth_date.strftime("%Y-%m-%d"),
            "Age_at_Issue": age_at_issue,
            "Gender": random.choice(genders),
            "Occupation_Class": random.choice(occupations),
            "Face_Amount": random.randint(50000, 1000000),
            "Annual_Premium": random.randint(500, 10000),
            "Policy_Status": random.choice(["Active", "Lapsed", "Paid-up", "Surrendered"]),
            "Smoker_Status": random.choice(["Y", "N"]),
            "Territory": random.choice(["Urban", "Suburban", "Rural"])
        }
        policies.append(policy)
    
    return pl.DataFrame(policies)


def generate_claims_data(num_claims: int = 150) -> pl.DataFrame:
    """Generate sample insurance claims data."""
    claim_types = ["Death", "Disability", "Accident", "Critical Illness", "Maturity"]
    claim_status = ["Approved", "Pending", "Denied", "Under Investigation"]
    
    claims = []
    for i in range(num_claims):
        claim_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1460))
        notification_date = claim_date + timedelta(days=random.randint(0, 30))
        
        claim = {
            "Claim_ID": f"CLM{i+1:06d}",
            "Policy_ID": f"POL{random.randint(1, 1000):06d}",
            "Claim_Type": random.choice(claim_types),
            "Claim_Date": claim_date.strftime("%Y-%m-%d"),
            "Notification_Date": notification_date.strftime("%Y-%m-%d"),
            "Claim_Amount": random.randint(10000, 500000),
            "Claim_Status": random.choice(claim_status),
            "Investigation_Days": random.randint(1, 180),
            "Settlement_Amount": random.randint(5000, 500000) if random.random() > 0.3 else 0
        }
        claims.append(claim)
    
    return pl.DataFrame(claims)


def generate_reserves_data() -> pl.DataFrame:
    """Generate reserve calculations by product and year."""
    products = ["Term Life", "Whole Life", "Universal Life", "Endowment", "Annuity"]
    years = list(range(2020, 2025))
    
    reserves = []
    for product in products:
        for year in years:
            base_reserve = random.randint(10000000, 100000000)
            reserve = {
                "Product_Type": product,
                "Valuation_Year": year,
                "Policy_Reserves": base_reserve,
                "Claim_Reserves": int(base_reserve * random.uniform(0.05, 0.15)),
                "IBNR_Reserves": int(base_reserve * random.uniform(0.02, 0.08)),
                "Total_Reserves": 0,  # Will calculate
                "Reserve_Method": random.choice(["Net Premium", "Gross Premium", "Modified Reserve"]),
                "Interest_Rate": round(random.uniform(0.02, 0.06), 4),
                "Mortality_Basis": random.choice(["CSO 2017", "CSO 2001", "Company Experience"])
            }
            reserve["Total_Reserves"] = (
                reserve["Policy_Reserves"] + 
                reserve["Claim_Reserves"] + 
                reserve["IBNR_Reserves"]
            )
            reserves.append(reserve)
    
    return pl.DataFrame(reserves)


def create_actuarial_excel_file():
    """Create a comprehensive actuarial Excel file with multiple sheets."""
    output_path = Path("sample_data/actuarial_data.xlsx")
    
    # Generate all datasets
    print("Generating life table data...")
    life_table = generate_life_table_data()
    
    print("Generating policy data...")
    policies = generate_policy_data()
    
    print("Generating claims data...")
    claims = generate_claims_data()
    
    print("Generating reserves data...")
    reserves = generate_reserves_data()
    
    # Create Excel file with multiple sheets
    print(f"Creating Excel file: {output_path}")
    
    # Write each sheet separately - first create individual files then combine
    temp_files = []
    
    # Write Life Table
    life_table_path = output_path.parent / "temp_life_table.xlsx"
    life_table.write_excel(life_table_path)
    temp_files.append(life_table_path)
    
    # Use xlsxwriter to create multi-sheet workbook
    import xlsxwriter
    
    workbook = xlsxwriter.Workbook(output_path)
    
    # Write Life Table sheet
    worksheet1 = workbook.add_worksheet("Life_Table")
    life_table_data = life_table.to_dict(as_series=False)
    for col_idx, (col_name, col_data) in enumerate(life_table_data.items()):
        worksheet1.write(0, col_idx, col_name)
        for row_idx, value in enumerate(col_data):
            worksheet1.write(row_idx + 1, col_idx, value)
    
    # Write Policies sheet
    worksheet2 = workbook.add_worksheet("Policies")
    policies_data = policies.to_dict(as_series=False)
    for col_idx, (col_name, col_data) in enumerate(policies_data.items()):
        worksheet2.write(0, col_idx, col_name)
        for row_idx, value in enumerate(col_data):
            worksheet2.write(row_idx + 1, col_idx, value)
    
    # Write Claims sheet
    worksheet3 = workbook.add_worksheet("Claims")
    claims_data = claims.to_dict(as_series=False)
    for col_idx, (col_name, col_data) in enumerate(claims_data.items()):
        worksheet3.write(0, col_idx, col_name)
        for row_idx, value in enumerate(col_data):
            worksheet3.write(row_idx + 1, col_idx, value)
    
    # Write Reserves sheet
    worksheet4 = workbook.add_worksheet("Reserves")
    reserves_data = reserves.to_dict(as_series=False)
    for col_idx, (col_name, col_data) in enumerate(reserves_data.items()):
        worksheet4.write(0, col_idx, col_name)
        for row_idx, value in enumerate(col_data):
            worksheet4.write(row_idx + 1, col_idx, value)
    
    workbook.close()
    
    # Clean up temp files
    for temp_file in temp_files:
        if temp_file.exists():
            temp_file.unlink()
    
    print(f"✅ Actuarial Excel file created: {output_path}")
    print("📊 Sheets created:")
    print(f"   - Life_Table: {life_table.shape[0]} rows, {life_table.shape[1]} columns")
    print(f"   - Policies: {policies.shape[0]} rows, {policies.shape[1]} columns")
    print(f"   - Claims: {claims.shape[0]} rows, {claims.shape[1]} columns")
    print(f"   - Reserves: {reserves.shape[0]} rows, {reserves.shape[1]} columns")
    
    return output_path


if __name__ == "__main__":
    create_actuarial_excel_file()
