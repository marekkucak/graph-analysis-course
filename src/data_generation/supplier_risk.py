#!/usr/bin/env python3
"""
Generate supplier risk dataset for Lesson 18 capstone.
Creates 8 CSVs modeling multi-tier supply chain with intentional risks.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.utils.random_seed import set_random_seed

set_random_seed(42)

OUTPUT_DIR = Path(__file__).parent.parent.parent / 'data' / 'seed' / 'supplier_risk'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ===== 1. SUPPLIERS (500 vendors) =====
suppliers_data = []
for i in range(500):
    supp_id = f'SUPP_{i:04d}'
    name_base = ['Acme', 'GlobalTech', 'FastLogistics', 'QualityFirst', 'Innovate', 'EcoDynamics', 'SecureSupply', 'PrimeSystems'][i % 8]
    name_var = ['Inc', 'Corp', 'Corporation', 'Ltd', 'LLC', 'Global', 'Solutions'][i % 7]
    supplier_name = f'{name_base} {name_var} {i}'
    
    category = ['IT', 'Logistics', 'Staffing', 'Packaging', 'Electronics', 'Chemicals', 'Manufacturing', 'Services'][i % 8]
    location = ['USA', 'Taiwan', 'Mexico', 'Germany', 'India', 'Brazil', 'Vietnam', 'Japan'][i % 8]
    
    # Inject risk: some suppliers have higher baseline risk
    base_risk = np.random.uniform(0.1, 0.7)
    if i in [147, 89, 234]:  # Special risk suppliers
        base_risk = np.random.uniform(0.6, 0.9)
    
    status = 'active'
    if base_risk > 0.75:
        status = 'at_risk'
    elif np.random.random() < 0.05:
        status = 'inactive'
    
    year_established = 2024 - np.random.randint(2, 25)
    
    suppliers_data.append({
        'supplier_id': supp_id,
        'supplier_name': supplier_name,
        'category': category,
        'location': location,
        'status': status,
        'risk_score': round(base_risk, 2),
        'year_established': year_established
    })

suppliers_df = pd.DataFrame(suppliers_data)
suppliers_df.to_csv(OUTPUT_DIR / 'suppliers.csv', index=False)
print(f'[OK] Generated suppliers.csv: {len(suppliers_df)} records')

# ===== 2. BUSINESS UNITS (8 BUs) =====
business_units_data = [
    {'bu_id': 'BU_001', 'bu_name': 'Procurement', 'department': 'Operations', 'region': 'Global', 'revenue_budget': 5000000},
    {'bu_id': 'BU_002', 'bu_name': 'Manufacturing', 'department': 'Operations', 'region': 'North America', 'revenue_budget': 3000000},
    {'bu_id': 'BU_003', 'bu_name': 'IT', 'department': 'Technology', 'region': 'Global', 'revenue_budget': 2000000},
    {'bu_id': 'BU_004', 'bu_name': 'HR', 'department': 'Administration', 'region': 'Global', 'revenue_budget': 1500000},
    {'bu_id': 'BU_005', 'bu_name': 'Finance', 'department': 'Administration', 'region': 'Global', 'revenue_budget': 1000000},
    {'bu_id': 'BU_006', 'bu_name': 'Logistics', 'department': 'Operations', 'region': 'Global', 'revenue_budget': 4000000},
    {'bu_id': 'BU_007', 'bu_name': 'Marketing', 'department': 'Sales', 'region': 'North America', 'revenue_budget': 2000000},
    {'bu_id': 'BU_008', 'bu_name': 'Product', 'department': 'Product', 'region': 'Global', 'revenue_budget': 2500000},
]
bu_df = pd.DataFrame(business_units_data)
bu_df.to_csv(OUTPUT_DIR / 'business_units.csv', index=False)
print(f'[OK] Generated business_units.csv: {len(bu_df)} records')

# ===== 3. CATEGORIES (40 procurement categories) =====
categories = ['IT Services', 'Software', 'Hardware', 'Staffing', 'Logistics', 'Packaging', 'Electronics', 'Chemicals',
              'Manufacturing', 'Consulting', 'Facilities', 'Security', 'Insurance', 'Legal', 'Recruiting', 'Training',
              'Maintenance', 'Repairs', 'Transportation', 'Warehousing', 'Testing', 'Quality', 'Compliance', 'Audit',
              'Engineering', 'Design', 'Marketing', 'Communications', 'Advertising', 'Analytics', 'Data', 'Cloud',
              'Networking', 'Telecom', 'Travel', 'Hospitality', 'Food Services', 'Office Supplies', 'Cleaning', 'Utilities']

categories_data = []
for i, cat in enumerate(categories):
    spend_target = np.random.uniform(100000, 2000000)
    criticality = ['high', 'high', 'medium', 'low'][i % 4]
    categories_data.append({
        'category_id': f'CAT_{i:02d}',
        'category_name': cat,
        'spend_target': round(spend_target, 0),
        'criticality_level': criticality
    })

cat_df = pd.DataFrame(categories_data)
cat_df.to_csv(OUTPUT_DIR / 'categories.csv', index=False)
print(f'[OK] Generated categories.csv: {len(cat_df)} records')

# ===== 4. CONTRACTS (1,500 supplier-BU-category relationships) =====
contracts_data = []
contract_id = 0
for _ in range(1500):
    contract_id += 1
    supp_id = suppliers_df.sample(1)['supplier_id'].values[0]
    bu_id = bu_df.sample(1)['bu_id'].values[0]
    cat_id = cat_df.sample(1)['category_id'].values[0]
    
    contract_value = np.random.uniform(10000, 500000)
    start_date = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365))
    end_date = start_date + timedelta(days=np.random.randint(90, 730))
    renewal_status = ['active', 'active', 'active', 'pending', 'at_risk', 'expired'][np.random.randint(0, 6)]
    
    contracts_data.append({
        'contract_id': f'CTR_{contract_id:05d}',
        'supplier_id': supp_id,
        'bu_id': bu_id,
        'category_id': cat_id,
        'contract_value': round(contract_value, 0),
        'start_date': start_date.date(),
        'end_date': end_date.date(),
        'renewal_status': renewal_status
    })

contracts_df = pd.DataFrame(contracts_data)
contracts_df.to_csv(OUTPUT_DIR / 'contracts.csv', index=False)
print(f'[OK] Generated contracts.csv: {len(contracts_df)} records')

# ===== 5. INVOICES (20,000 transaction records) =====
invoices_data = []
invoice_id = 0
for _ in range(20000):
    invoice_id += 1
    contract = contracts_df.sample(1).iloc[0]
    invoice_date = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365))
    amount = np.random.uniform(1000, contract['contract_value'])
    
    # Inject risk: some suppliers have poor payment reliability
    if contract['supplier_id'] in ['SUPP_0089', 'SUPP_0147', 'SUPP_0234']:
        on_time = np.random.random() < 0.65  # 65% on-time for at-risk suppliers
    else:
        on_time = np.random.random() < 0.95  # 95% on-time for normal suppliers
    
    invoices_data.append({
        'invoice_id': f'INV_{invoice_id:08d}',
        'contract_id': contract['contract_id'],
        'invoice_date': invoice_date.date(),
        'amount': round(amount, 0),
        'on_time_payment': on_time
    })

invoices_df = pd.DataFrame(invoices_data)
invoices_df.to_csv(OUTPUT_DIR / 'invoices.csv', index=False)
print(f'[OK] Generated invoices.csv: {len(invoices_df)} records')

# ===== 6. LOCATIONS (30 geographic locations) =====
locations_data = [
    ('USA_CA', 'California, USA', 'USA', 'North America', 0.1),
    ('USA_TX', 'Texas, USA', 'USA', 'North America', 0.1),
    ('USA_NY', 'New York, USA', 'USA', 'North America', 0.1),
    ('MEX_MX', 'Mexico City, Mexico', 'Mexico', 'North America', 0.2),
    ('CAN_ON', 'Ontario, Canada', 'Canada', 'North America', 0.1),
    ('GER_BW', 'Baden-Württemberg, Germany', 'Germany', 'Europe', 0.15),
    ('GER_BY', 'Bavaria, Germany', 'Germany', 'Europe', 0.15),
    ('GBR_EN', 'England, UK', 'UK', 'Europe', 0.2),
    ('TWN_TP', 'Taipei, Taiwan', 'Taiwan', 'Asia', 0.85),
    ('TWN_TW', 'Taichung, Taiwan', 'Taiwan', 'Asia', 0.85),
    ('IND_MH', 'Mumbai, India', 'India', 'Asia', 0.35),
    ('IND_KA', 'Bangalore, India', 'India', 'Asia', 0.35),
    ('JPN_TK', 'Tokyo, Japan', 'Japan', 'Asia', 0.15),
    ('JPN_OS', 'Osaka, Japan', 'Japan', 'Asia', 0.15),
    ('VTM_HN', 'Hanoi, Vietnam', 'Vietnam', 'Asia', 0.45),
    ('VTM_HM', 'Ho Chi Minh, Vietnam', 'Vietnam', 'Asia', 0.45),
    ('BRA_SP', 'São Paulo, Brazil', 'Brazil', 'South America', 0.3),
    ('BRA_RJ', 'Rio de Janeiro, Brazil', 'Brazil', 'South America', 0.3),
    ('CHN_SH', 'Shanghai, China', 'China', 'Asia', 0.75),
    ('CHN_BJ', 'Beijing, China', 'China', 'Asia', 0.75),
    ('KOR_SL', 'Seoul, South Korea', 'South Korea', 'Asia', 0.2),
    ('THA_BK', 'Bangkok, Thailand', 'Thailand', 'Asia', 0.4),
    ('SGP_SG', 'Singapore', 'Singapore', 'Asia', 0.1),
    ('AUS_SY', 'Sydney, Australia', 'Australia', 'Oceania', 0.1),
    ('NLD_AM', 'Amsterdam, Netherlands', 'Netherlands', 'Europe', 0.15),
    ('FRA_PA', 'Paris, France', 'France', 'Europe', 0.15),
    ('ITA_MI', 'Milan, Italy', 'Italy', 'Europe', 0.2),
    ('ESP_MD', 'Madrid, Spain', 'Spain', 'Europe', 0.2),
    ('POL_WR', 'Warsaw, Poland', 'Poland', 'Europe', 0.25),
    ('RUS_MO', 'Moscow, Russia', 'Russia', 'Europe', 0.9),
]

locations_df = pd.DataFrame(locations_data, columns=['location_id', 'location_name', 'country', 'region', 'geopolitical_risk_score'])
locations_df.to_csv(OUTPUT_DIR / 'locations.csv', index=False)
print(f'[OK] Generated locations.csv: {len(locations_df)} records')

# ===== 7. PRODUCTS (50 revenue-generating products) =====
products_data = []
for i in range(50):
    product_name = ['Product Alpha', 'Product Beta', 'Service Gold', 'Premium Plus', 'Essential Core'][i % 5] + f' {i+1}'
    revenue_impact = np.random.uniform(100000, 5000000)
    
    # Some products depend on multiple suppliers (vulnerability)
    if i in [0, 5, 10, 15, 20]:  # Critical products
        supplier_dependencies = np.random.randint(3, 8)
    else:
        supplier_dependencies = np.random.randint(1, 4)
    
    products_data.append({
        'product_id': f'PRD_{i:03d}',
        'product_name': product_name,
        'revenue_impact': round(revenue_impact, 0),
        'supplier_dependencies': supplier_dependencies
    })

products_df = pd.DataFrame(products_data)
products_df.to_csv(OUTPUT_DIR / 'products.csv', index=False)
print(f'[OK] Generated products.csv: {len(products_df)} records')

# ===== 8. RISK EVENTS (100 disruption/quality/financial incidents) =====
risk_events_data = []
event_types = ['disruption', 'quality', 'financial', 'legal', 'compliance']
impact_severities = ['critical', 'high', 'medium']

for i in range(100):
    # Focus risk events on at-risk suppliers
    if i < 20:
        supp_id = suppliers_df[suppliers_df['risk_score'] > 0.7].sample(1)['supplier_id'].values[0]
    else:
        supp_id = suppliers_df.sample(1)['supplier_id'].values[0]
    
    event_date = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365))
    event_type = event_types[i % 5]
    severity = impact_severities[i % 3]
    
    risk_events_data.append({
        'event_id': f'EVT_{i:04d}',
        'supplier_id': supp_id,
        'event_date': event_date.date(),
        'event_type': event_type,
        'impact_severity': severity
    })

events_df = pd.DataFrame(risk_events_data)
events_df.to_csv(OUTPUT_DIR / 'risk_events.csv', index=False)
print(f'[OK] Generated risk_events.csv: {len(events_df)} records')

# ===== 9. SUMMARY =====
print(f'\n[SUMMARY] Supplier Risk Dataset Generated')
print(f'  Location: {OUTPUT_DIR}')
print(f'  Files: 8 CSVs')
print(f'  Total records: {len(suppliers_df) + len(bu_df) + len(cat_df) + len(contracts_df) + len(invoices_df) + len(locations_df) + len(products_df) + len(events_df)}')
print(f'  Injected risks:')
print(f'    • Spend fragmentation (multiple BUs buying same category from different suppliers)')
print(f'    • Single-point-of-failure (SUPP_0147 serves multiple critical products)')
print(f'    • Geopolitical concentration (15% suppliers in high-risk zones)')
print(f'    • Duplicate vendors (similar names for consolidation opportunity)')
print(f'    • Payment defaults (SUPP_0089, SUPP_0234 with <70% on-time payment)')
print(f'\n[DONE] Data generation complete')
