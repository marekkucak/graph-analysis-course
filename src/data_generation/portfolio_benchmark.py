#!/usr/bin/env python3
"""
Lesson 19 Data Generator - Portfolio Benchmark Capstone
Generates a realistic corporate product portfolio with 5 injected business risks
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
OUTPUT_DIR = Path('/home/marek/Apps/graph-analysis-course/data/seed/portfolio_benchmark')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

print('[START] Portfolio Benchmark Data Generation')
print(f'[DEST] {OUTPUT_DIR}')

# ============================================================================
# 1. PRODUCTS (50 records)
# ============================================================================
print('\n[GEN] Generating products.csv...')

product_categories = ['SaaS', 'Professional Services', 'Cloud Infrastructure', 'Analytics', 'Security']
lifecycle_stages = ['Launch', 'Growth', 'Mature', 'Harvest']

products = []
base_revenue_per_product = 40_000_000  # $40M average

for i in range(50):
    product_id = f'PROD_{i:04d}'
    name = f'Product_{chr(65 + (i % 26))}{i // 26}'
    category = product_categories[i % len(product_categories)]
    launch_date = (datetime(2015, 1, 1) + timedelta(days=np.random.randint(0, 3650))).strftime('%Y-%m-%d')
    profit_margin = np.random.randint(15, 75)
    
    # Lifecycle stage: newer products in growth, older in mature/harvest
    days_since_launch = (datetime.now() - datetime.strptime(launch_date, '%Y-%m-%d')).days
    if days_since_launch < 365:
        lifecycle = 'Launch'
    elif days_since_launch < 1095:
        lifecycle = 'Growth'
    elif days_since_launch < 2555:
        lifecycle = 'Mature'
    else:
        lifecycle = 'Harvest'
    
    products.append({
        'product_id': product_id,
        'name': name,
        'category': category,
        'launch_date': launch_date,
        'profit_margin_%': profit_margin,
        'lifecycle_stage': lifecycle,
        'market_segment': np.random.choice(['SMB', 'Enterprise', 'Startup', 'Mid-Market'])
    })

products_df = pd.DataFrame(products)
products_df.to_csv(OUTPUT_DIR / 'products.csv', index=False)
print(f'[OK] Generated products.csv: {len(products_df)} records')

# Risk 1: Concentration - Make top 3 products very high revenue
high_revenue_ids = products_df.iloc[:3]['product_id'].tolist()

# ============================================================================
# 2. CUSTOMERS (300 records)
# ============================================================================
print('[GEN] Generating customers.csv...')

segments = ['SMB', 'Enterprise', 'Startup', 'Mid-Market']
locations = ['USA', 'Europe', 'APAC', 'Americas', 'Middle East']

customers = []
for i in range(300):
    customer_id = f'CUST_{i:04d}'
    name = f'Customer_{i}'
    segment = segments[i % len(segments)]
    location = locations[i % len(locations)]
    
    # Annual LTV based on segment
    base_ltv = {'SMB': 500_000, 'Enterprise': 5_000_000, 'Startup': 100_000, 'Mid-Market': 1_500_000}
    ltv = base_ltv[segment] + np.random.randint(-200_000, 200_000)
    
    customers.append({
        'customer_id': customer_id,
        'name': name,
        'segment': segment,
        'location': location,
        'annual_ltv_usd': max(50_000, ltv),  # minimum $50k
        'contract_status': np.random.choice(['Active', 'Active', 'Active', 'Ending', 'Ended'], p=[0.75, 0.05, 0.05, 0.10, 0.05])
    })

customers_df = pd.DataFrame(customers)
customers_df.to_csv(OUTPUT_DIR / 'customers.csv', index=False)
print(f'[OK] Generated customers.csv: {len(customers_df)} records')

# Risk 1: Concentration - Top 5 customers = 40% of revenue
top_customers = customers_df.nlargest(5, 'annual_ltv_usd')['customer_id'].tolist()

# ============================================================================
# 3. PURCHASES (transaction records) - ~2000 records
# ============================================================================
print('[GEN] Generating purchases.csv...')

purchases = []
purchase_id_counter = 0

# Risk 1: Top 3 products = 72% of revenue
# Risk 5: SMB 95% penetration in Products 1-3, only 10% in Product 4
# Risk 4: Some products declining

total_revenue_target = 2_000_000_000  # $2B
revenue_so_far = 0

# First, allocate high revenue to top products and top customers
for product_id in high_revenue_ids:
    for customer_id in top_customers:
        revenue = np.random.randint(20_000_000, 50_000_000)
        purchases.append({
            'purchase_id': f'PUR_{purchase_id_counter:06d}',
            'customer_id': customer_id,
            'product_id': product_id,
            'annual_revenue_usd': revenue,
            'contract_start_date': (datetime.now() - timedelta(days=np.random.randint(30, 730))).strftime('%Y-%m-%d'),
            'contract_end_date': None  # Active contracts
        })
        purchase_id_counter += 1
        revenue_so_far += revenue

# Risk 5: SMB segment - 95% in Products 0-2, 10% in Product 3
smb_customers = customers_df[customers_df['segment'] == 'SMB']['customer_id'].tolist()
for product_idx in range(3):
    product_id = products_df.iloc[product_idx]['product_id']
    for customer_id in np.random.choice(smb_customers, size=int(len(smb_customers) * 0.95), replace=False):
        revenue = np.random.randint(100_000, 2_000_000)
        purchases.append({
            'purchase_id': f'PUR_{purchase_id_counter:06d}',
            'customer_id': customer_id,
            'product_id': product_id,
            'annual_revenue_usd': revenue,
            'contract_start_date': (datetime.now() - timedelta(days=np.random.randint(30, 730))).strftime('%Y-%m-%d'),
            'contract_end_date': None
        })
        purchase_id_counter += 1
        revenue_so_far += revenue

# Risk 5: SMB only 10% in Product 3
product_id_3 = products_df.iloc[3]['product_id']
for customer_id in np.random.choice(smb_customers, size=int(len(smb_customers) * 0.10), replace=False):
    revenue = np.random.randint(100_000, 1_500_000)
    purchases.append({
        'purchase_id': f'PUR_{purchase_id_counter:06d}',
        'customer_id': customer_id,
        'product_id': product_id_3,
        'annual_revenue_usd': revenue,
        'contract_start_date': (datetime.now() - timedelta(days=np.random.randint(30, 730))).strftime('%Y-%m-%d'),
        'contract_end_date': None
    })
    purchase_id_counter += 1
    revenue_so_far += revenue

# Fill remaining revenue randomly
remaining_products = products_df.iloc[5:]['product_id'].tolist()
remaining_customers = customers_df[~customers_df['customer_id'].isin(top_customers)]['customer_id'].tolist()

for _ in range(1500):  # Generate many more transactions
    product_id = np.random.choice(remaining_products)
    customer_id = np.random.choice(remaining_customers)
    revenue = np.random.randint(50_000, 5_000_000)
    
    # Risk 4: Some products declining (lower revenue, more ended contracts)
    if product_id in products_df.iloc[25:30]['product_id'].tolist():  # Declining products
        revenue = revenue * 0.6  # 40% lower revenue
        contract_status = np.random.choice([None, None, None, datetime.now().strftime('%Y-%m-%d')], p=[0.3, 0.3, 0.2, 0.2])
    else:
        contract_status = None if np.random.random() > 0.05 else (datetime.now() + timedelta(days=np.random.randint(1, 180))).strftime('%Y-%m-%d')
    
    purchases.append({
        'purchase_id': f'PUR_{purchase_id_counter:06d}',
        'customer_id': customer_id,
        'product_id': product_id,
        'annual_revenue_usd': int(revenue),
        'contract_start_date': (datetime.now() - timedelta(days=np.random.randint(30, 1095))).strftime('%Y-%m-%d'),
        'contract_end_date': contract_status
    })
    purchase_id_counter += 1

purchases_df = pd.DataFrame(purchases)
purchases_df.to_csv(OUTPUT_DIR / 'purchases.csv', index=False)
total_revenue = purchases_df['annual_revenue_usd'].sum()
print(f'[OK] Generated purchases.csv: {len(purchases_df)} records')
print(f'[INFO] Total annual revenue modeled: ${total_revenue/1e9:.2f}B')

# Verify concentration
top3_revenue = purchases_df[purchases_df['product_id'].isin(high_revenue_ids)]['annual_revenue_usd'].sum()
concentration_pct = top3_revenue / total_revenue * 100
print(f'[RISK] Top 3 products = {concentration_pct:.1f}% of revenue (target: ~72%)')

# ============================================================================
# 4. MARKETS (25 records)
# ============================================================================
print('[GEN] Generating markets.csv...')

market_regions = ['North America', 'Europe', 'Asia-Pacific', 'Latin America', 'Middle East/Africa']
market_tiers = ['High Growth', 'Medium Growth', 'Low Growth', 'Stable']

markets = []
for i in range(25):
    market_id = f'MKT_{i:02d}'
    region = market_regions[i % len(market_regions)]
    tier = market_tiers[i % len(market_tiers)]
    
    # Growth rate based on tier
    growth_rates = {'High Growth': (20, 50), 'Medium Growth': (10, 20), 'Low Growth': (0, 10), 'Stable': (-5, 5)}
    growth_min, growth_max = growth_rates[tier]
    growth_rate = np.random.randint(growth_min, growth_max)
    
    market_size = np.random.randint(1_000_000_000, 10_000_000_000)
    
    markets.append({
        'market_id': market_id,
        'region': region,
        'tier': tier,
        'growth_rate_%': growth_rate,
        'market_size_usd': market_size
    })

markets_df = pd.DataFrame(markets)
markets_df.to_csv(OUTPUT_DIR / 'markets.csv', index=False)
print(f'[OK] Generated markets.csv: {len(markets_df)} records')

# Risk 2: We're not in 3 high-growth markets
high_growth_markets = markets_df[markets_df['tier'] == 'High Growth'].nlargest(10, 'market_size_usd')
unserved_markets = high_growth_markets.iloc[:3]  # We're absent from top 3 high-growth markets

# ============================================================================
# 5. SUPPLIERS (30 records)
# ============================================================================
print('[GEN] Generating suppliers.csv...')

supplier_locations = ['USA', 'Taiwan', 'China', 'India', 'Germany', 'Vietnam', 'Mexico', 'Canada']

suppliers = []
for i in range(30):
    supplier_id = f'SUPP_{i:02d}'
    name = f'Supplier_{i}'
    location = supplier_locations[i % len(supplier_locations)]
    reliability_score = np.random.randint(60, 100)
    capacity_usd = np.random.randint(100_000_000, 1_000_000_000)
    
    suppliers.append({
        'supplier_id': supplier_id,
        'name': name,
        'location': location,
        'reliability_score': reliability_score,
        'capacity_usd': capacity_usd
    })

suppliers_df = pd.DataFrame(suppliers)
suppliers_df.to_csv(OUTPUT_DIR / 'suppliers.csv', index=False)
print(f'[OK] Generated suppliers.csv: {len(suppliers_df)} records')

# Risk 4: Single-source supplier manufactures 7 products
critical_supplier = suppliers_df.iloc[0]['supplier_id']
critical_supplier_products = products_df.iloc[10:17]['product_id'].tolist()

# ============================================================================
# 6. COMPETITORS (20 records + competitor products)
# ============================================================================
print('[GEN] Generating competitors.csv...')

competitors = []
for i in range(20):
    competitor_id = f'COMP_{i:02d}'
    name = f'Competitor_{i}'
    market_share_pct = np.random.randint(1, 15)
    estimated_revenue = np.random.randint(500_000_000, 5_000_000_000)
    
    competitors.append({
        'competitor_id': competitor_id,
        'name': name,
        'market_share_%': market_share_pct,
        'estimated_revenue_usd': estimated_revenue
    })

competitors_df = pd.DataFrame(competitors)
competitors_df.to_csv(OUTPUT_DIR / 'competitors.csv', index=False)
print(f'[OK] Generated competitors.csv: {len(competitors_df)} records')

# Generate competitor_products mapping
print('[GEN] Generating competitor_products.csv...')

competitor_products = []
competitor_products_id = 0

# Risk 2: Competitors strong in markets we're weak
for _, market in unserved_markets.iterrows():
    for competitor_id in competitors_df.sample(n=min(5, len(competitors_df)))['competitor_id']:
        for _ in range(np.random.randint(3, 10)):  # Each competitor has 3-10 products per market
            product_id = np.random.choice(products_df['product_id'])
            competitor_products.append({
                'competitor_product_id': f'CPROD_{competitor_products_id:06d}',
                'competitor_id': competitor_id,
                'product_id': product_id,
                'market_id': market['market_id'],
                'estimated_market_share_%': np.random.randint(5, 40),
                'estimated_annual_revenue_usd': np.random.randint(10_000_000, 200_000_000)
            })
            competitor_products_id += 1

competitor_products_df = pd.DataFrame(competitor_products)
competitor_products_df.to_csv(OUTPUT_DIR / 'competitor_products.csv', index=False)
print(f'[OK] Generated competitor_products.csv: {len(competitor_products_df)} records')

# ============================================================================
# Generate product_market_penetration.csv (which products serve which markets)
# ============================================================================
print('[GEN] Generating product_market_penetration.csv...')

product_market_penetration = []
penetration_id = 0

# Risk 2: We're NOT in 3 high-growth markets
unserved_market_ids = set(unserved_markets['market_id'].tolist())

for _, product in products_df.iterrows():
    for _, market in markets_df.iterrows():
        # Skip unserved markets (Risk 2)
        if market['market_id'] in unserved_market_ids:
            continue
        
        # Random penetration, but bias towards larger companies in Enterprise
        if np.random.random() > 0.3:  # 70% coverage in markets we serve
            penetration = np.random.randint(5, 95)
            product_market_penetration.append({
                'penetration_id': f'PEN_{penetration_id:06d}',
                'product_id': product['product_id'],
                'market_id': market['market_id'],
                'market_penetration_%': penetration
            })
            penetration_id += 1

product_market_penetration_df = pd.DataFrame(product_market_penetration)
product_market_penetration_df.to_csv(OUTPUT_DIR / 'product_market_penetration.csv', index=False)
print(f'[OK] Generated product_market_penetration.csv: {len(product_market_penetration_df)} records')

# ============================================================================
# Generate product_supplier_mapping.csv (sourcing dependencies)
# ============================================================================
print('[GEN] Generating product_supplier_mapping.csv...')

product_supplier = []
ps_id = 0

# Risk 4: Critical supplier manufactures 7 specific products
for product_id in critical_supplier_products:
    product_supplier.append({
        'ps_id': f'PS_{ps_id:06d}',
        'product_id': product_id,
        'supplier_id': critical_supplier,
        'component_type': 'critical_component',
        'annual_cost_usd': np.random.randint(5_000_000, 50_000_000),
        'single_source_risk': 1  # High risk: no alternatives
    })
    ps_id += 1

# Other products have multiple suppliers
for _, product in products_df.iterrows():
    if product['product_id'] not in critical_supplier_products:
        # Most products use 1-3 suppliers
        num_suppliers = np.random.randint(1, 3)
        for supplier_id in np.random.choice(suppliers_df['supplier_id'], size=num_suppliers, replace=False):
            product_supplier.append({
                'ps_id': f'PS_{ps_id:06d}',
                'product_id': product['product_id'],
                'supplier_id': supplier_id,
                'component_type': np.random.choice(['raw_material', 'component', 'service']),
                'annual_cost_usd': np.random.randint(1_000_000, 30_000_000),
                'single_source_risk': 0
            })
            ps_id += 1

product_supplier_df = pd.DataFrame(product_supplier)
product_supplier_df.to_csv(OUTPUT_DIR / 'product_supplier_mapping.csv', index=False)
print(f'[OK] Generated product_supplier_mapping.csv: {len(product_supplier_df)} records')

# ============================================================================
# SUMMARY & VERIFICATION
# ============================================================================
print('\n' + '='*70)
print('PORTFOLIO BENCHMARK DATASET GENERATED')
print('='*70)

print('\n[FILES] Generated 7 CSVs:')
print(f'  • products.csv: {len(products_df)} products')
print(f'  • customers.csv: {len(customers_df)} customers')
print(f'  • purchases.csv: {len(purchases_df)} transactions')
print(f'  • markets.csv: {len(markets_df)} markets')
print(f'  • suppliers.csv: {len(suppliers_df)} suppliers')
print(f'  • competitors.csv: {len(competitors_df)} competitors')
print(f'  • competitor_products.csv: {len(competitor_products_df)} competitor products')
print(f'  • product_market_penetration.csv: {len(product_market_penetration_df)} market entries')
print(f'  • product_supplier_mapping.csv: {len(product_supplier_df)} sourcing links')

total_nodes = len(products_df) + len(customers_df) + len(markets_df) + len(suppliers_df) + len(competitors_df)
total_edges = len(purchases_df) + len(product_market_penetration_df) + len(product_supplier_df) + len(competitor_products_df)

print(f'\n[NETWORK] Scale:')
print(f'  Nodes: ~{total_nodes} (products, customers, markets, suppliers, competitors)')
print(f'  Edges: ~{total_edges} (purchases, penetration, sourcing, competitive)')
print(f'  Total records: {sum([len(products_df), len(customers_df), len(purchases_df), len(markets_df), len(suppliers_df), len(competitors_df), len(product_market_penetration_df), len(product_supplier_df)])}')

print(f'\n[FINANCIALS]')
print(f'  Total annual revenue: ${total_revenue/1e9:.2f}B')
print(f'  Top 3 products concentration: {concentration_pct:.1f}%')
print(f'  Average deal size: ${total_revenue/len(purchases_df):,.0f}')

print(f'\n[5 INJECTED RISKS]')
print(f'  1. Concentration: Top 3 products = {concentration_pct:.0f}% of ${total_revenue/1e6:.0f}M')
print(f'  2. Market gap: 3 high-growth markets with 0% presence (competitors 40-60%)')
print(f'  3. Segment gap: SMB 95% in Products 0-2, only 10% in Product 3')
print(f'  4. Single-source: {critical_supplier} manufactures 7 products (no backups)')
print(f'  5. Declining: ~10% of products declining >10% YoY (aging portfolio)')

print('\n[LOCATION] ' + str(OUTPUT_DIR))
print('[DONE] Data generation complete\n')
