#!/usr/bin/env python3
"""
Demonstrate loading and analyzing the converted actuarial Polars DataFrames.
"""

import polars as pl
from pathlib import Path


def main():
    """Load and analyze the actuarial Polars DataFrames."""
    output_dir = Path("output")
    
    print("🚀 ACTUARIAL DATA POLARS ANALYSIS")
    print("=" * 50)
    
    # ===== LOAD ALL POLARS DATAFRAMES =====
    print("\n📊 Loading Polars DataFrames...")
    
    # Load from Parquet files (most efficient)
    life_table = pl.read_parquet(output_dir / "life_table.parquet")
    policies = pl.read_parquet(output_dir / "policies.parquet")
    claims = pl.read_parquet(output_dir / "claims.parquet")
    reserves = pl.read_parquet(output_dir / "reserves.parquet")
    
    print(f"✅ Life Table: {life_table.shape} (rows × columns)")
    print(f"✅ Policies: {policies.shape}")
    print(f"✅ Claims: {claims.shape}")
    print(f"✅ Reserves: {reserves.shape}")
    
    # ===== POLARS DATAFRAME ANALYSIS =====
    print("\n" + "=" * 50)
    print("POLARS DATAFRAME ANALYSIS")
    print("=" * 50)
    
    # 1. CLAIMS ANALYSIS
    print("\n📋 CLAIMS ANALYSIS")
    print("-" * 30)
    
    # Claims by status using Polars aggregation
    claims_by_status = claims.group_by("Claim_Status").agg([
        pl.count().alias("count"),
        pl.col("Claim_Amount").mean().round(2).alias("avg_claim_amount"),
        pl.col("Settlement_Amount").mean().round(2).alias("avg_settlement"),
        pl.col("Investigation_Days").mean().round(1).alias("avg_investigation_days")
    ]).sort("count", descending=True)
    
    print("\n📊 Claims by Status:")
    print(claims_by_status)
    
    # High-value claims using Polars filtering
    high_value_claims = claims.filter(pl.col("Claim_Amount") > 400000)
    print(f"\n💰 High-value claims (>$400k): {len(high_value_claims)} out of {len(claims)}")
    
    # Claims by type
    claims_by_type = claims.group_by("Claim_Type").agg([
        pl.count().alias("count"),
        pl.col("Claim_Amount").mean().round(2).alias("avg_amount")
    ]).sort("avg_amount", descending=True)
    
    print("\n📈 Claims by Type:")
    print(claims_by_type)
    
    # 2. POLICY ANALYSIS
    print("\n🏢 POLICY ANALYSIS")
    print("-" * 30)
    
    # Policy statistics by type
    policy_stats = policies.group_by("Policy_Type").agg([
        pl.count().alias("count"),
        pl.col("Face_Amount").mean().round(2).alias("avg_face_amount"),
        pl.col("Annual_Premium").mean().round(2).alias("avg_premium"),
        (pl.col("Annual_Premium") / pl.col("Face_Amount") * 1000).mean().round(3).alias("premium_rate_per_1000")
    ]).sort("count", descending=True)
    
    print("\n📊 Policy Statistics by Type:")
    print(policy_stats)
    
    # Active vs. inactive policies
    policy_status = policies.group_by("Policy_Status").agg([
        pl.count().alias("count"),
        pl.col("Face_Amount").sum().alias("total_face_amount")
    ]).sort("count", descending=True)
    
    print("\n📋 Policy Status Distribution:")
    print(policy_status)
    
    # 3. LIFE TABLE ANALYSIS
    print("\n💀 MORTALITY ANALYSIS")
    print("-" * 30)
    
    # High mortality ages
    high_mortality = life_table.filter(pl.col("Mortality_Rate_qx") > 0.1).select([
        "Age", "Mortality_Rate_qx", "Life_Expectancy"
    ])
    
    print("\n⚠️  High Mortality Ages (>10%):")
    print(high_mortality)
    
    # Life expectancy statistics
    life_stats = life_table.select([
        pl.col("Life_Expectancy").mean().round(2).alias("avg_life_expectancy"),
        pl.col("Life_Expectancy").min().alias("min_life_expectancy"),
        pl.col("Life_Expectancy").max().round(2).alias("max_life_expectancy")
    ])
    
    print(f"\n📊 Life Expectancy Statistics:")
    print(life_stats)
    
    # 4. RESERVE ANALYSIS
    print("\n💰 RESERVE ANALYSIS")
    print("-" * 30)
    
    # Reserve trends by year
    reserve_trends = reserves.group_by("Valuation_Year").agg([
        pl.col("Policy_Reserves").sum().alias("total_policy_reserves"),
        pl.col("Claim_Reserves").sum().alias("total_claim_reserves"),
        pl.col("IBNR_Reserves").sum().alias("total_ibnr_reserves"),
        pl.col("Total_Reserves").sum().alias("grand_total_reserves")
    ]).sort("Valuation_Year")
    
    print("\n📈 Reserve Trends by Year:")
    print(reserve_trends)
    
    # Reserve by product type
    reserve_by_product = reserves.group_by("Product_Type").agg([
        pl.col("Total_Reserves").sum().alias("total_reserves"),
        pl.col("Interest_Rate").mean().round(4).alias("avg_interest_rate")
    ]).sort("total_reserves", descending=True)
    
    print("\n🏭 Reserves by Product Type:")
    print(reserve_by_product)
    
    # 5. ADVANCED POLARS OPERATIONS
    print("\n🔗 ADVANCED POLARS ANALYSIS")
    print("-" * 30)
    
    # Join policies with claims for loss analysis
    policy_claims = policies.join(
        claims,
        on="Policy_ID",
        how="inner"
    ).select([
        "Policy_Type", "Face_Amount", "Annual_Premium", 
        "Claim_Type", "Claim_Amount", "Claim_Status"
    ])
    
    print(f"\n🔗 Successfully joined {len(policy_claims)} policy-claim records")
    
    # Calculate loss ratios by policy type
    loss_ratios = policy_claims.group_by("Policy_Type").agg([
        pl.count().alias("claims_count"),
        pl.col("Claim_Amount").sum().alias("total_claims"),
        pl.col("Face_Amount").sum().alias("total_face_amount"),
        (pl.col("Claim_Amount").sum() / pl.col("Face_Amount").sum() * 100).round(2).alias("loss_ratio_percent")
    ]).sort("loss_ratio_percent", descending=True)
    
    print("\n📊 Loss Ratios by Policy Type:")
    print(loss_ratios)
    
    # 6. DATA EXPORT EXAMPLES
    print("\n💾 DATA EXPORT EXAMPLES")
    print("-" * 30)
    
    # Save filtered data to new files
    print("\n🔄 Creating filtered datasets...")
    
    # High-value claims only
    high_value_claims.write_parquet(output_dir / "high_value_claims.parquet")
    print(f"✅ Saved {len(high_value_claims)} high-value claims to high_value_claims.parquet")
    
    # Active policies only
    active_policies = policies.filter(pl.col("Policy_Status") == "Active")
    active_policies.write_parquet(output_dir / "active_policies.parquet")
    print(f"✅ Saved {len(active_policies)} active policies to active_policies.parquet")
    
    # Loss ratio summary
    loss_ratios.write_csv(output_dir / "loss_ratios_summary.csv")
    print("✅ Saved loss ratios summary to loss_ratios_summary.csv")
    
    # 7. SUMMARY STATISTICS
    print("\n📈 SUMMARY STATISTICS")
    print("-" * 30)
    
    total_face_amount = policies.select(pl.col("Face_Amount").sum()).item()
    total_claims = claims.select(pl.col("Claim_Amount").sum()).item()
    total_reserves = reserves.select(pl.col("Total_Reserves").sum()).item()
    
    print(f"💰 Total Face Amount: ${total_face_amount:,.0f}")
    print(f"📋 Total Claims: ${total_claims:,.0f}")
    print(f"🏦 Total Reserves: ${total_reserves:,.0f}")
    print(f"📊 Overall Loss Ratio: {(total_claims / total_face_amount * 100):.2f}%")
    
    print(f"\n✅ All Polars DataFrames are ready for further analysis!")
    print("\n💡 Next steps:")
    print("   - Perform statistical modeling")
    print("   - Create actuarial projections")
    print("   - Build machine learning models")
    print("   - Generate reports and visualizations")


if __name__ == "__main__":
    main()
