"""
Sales Accounts & Product Network Data Generator

Generates a customer-product bipartite network for teaching two-mode graphs,
node similarity, one-mode projections, and duplicate detection.

Domain: B2B SaaS customer base with product purchases
Entities: 250 customers, 120 products, 1200 purchases (bipartite)
Relationships: Customer purchases product (only these edge types)
Anomalies: Duplicate customers, power users, dead accounts, single-expert products
"""

import pandas as pd
import numpy as np
from pathlib import Path
from faker import Faker
from datetime import datetime, timedelta

from .common import set_random_seed


def generate_customers(n_customers=250, seed=42):
    """
    Generate customer records.
    
    Args:
        n_customers: Total customers (default 250)
        seed: Random seed
    
    Returns:
        DataFrame with columns: customer_id, company_name, industry, company_size, region, 
                               account_value, contract_start_date, status
    """
    set_random_seed(seed)
    fake = Faker()
    Faker.seed(seed)
    
    customers = []
    
    industries = ['manufacturing', 'finance', 'retail', 'tech', 'healthcare']
    sizes = ['small', 'medium', 'large']
    regions = ['north', 'south', 'east', 'west', 'central']
    statuses = ['active', 'inactive', 'at_risk']
    
    # Status distribution: 75% active, 20% inactive, 5% at_risk
    status_weights = [0.75, 0.20, 0.05]
    
    for i in range(n_customers):
        customer_id = f"CUST_{i:04d}"
        
        # Company name (realistic with some variations)
        company_base = fake.company()
        if np.random.random() < 0.05:  # 5% chance of name variation (for duplicates later)
            company_name = company_base.replace(' ', '').lower()[:15].upper()
        else:
            company_name = company_base
        
        industry = np.random.choice(industries)
        size = np.random.choice(sizes, p=[0.4, 0.4, 0.2])
        region = np.random.choice(regions)
        
        # Account value: skewed distribution (Pareto)
        # Most customers small, few very large
        base_value = np.random.pareto(2.5)  # Heavy tail
        if size == 'small':
            account_value = int((base_value * 50000) + 10000)
        elif size == 'medium':
            account_value = int((base_value * 150000) + 50000)
        else:  # large
            account_value = int((base_value * 500000) + 200000)
        account_value = min(account_value, 5000000)  # Cap at $5M
        
        # Contract start date: distributed across 3 years
        days_ago = np.random.randint(0, 1095)
        contract_start = datetime.now() - timedelta(days=days_ago)
        
        # Status: weighted random (most active, some inactive)
        status = np.random.choice(statuses, p=status_weights)
        
        customers.append({
            'customer_id': customer_id,
            'company_name': company_name,
            'industry': industry,
            'company_size': size,
            'region': region,
            'account_value': account_value,
            'contract_start_date': contract_start.strftime('%Y-%m-%d'),
            'status': status
        })
    
    return pd.DataFrame(customers)


def generate_products(n_products=120, seed=42):
    """
    Generate product records.
    
    Args:
        n_products: Total products (default 120)
        seed: Random seed
    
    Returns:
        DataFrame with columns: product_id, product_name, category, price_tier,
                               launch_date, status
    """
    set_random_seed(seed)
    fake = Faker()
    Faker.seed(seed)
    
    products = []
    
    categories = ['analytics', 'integration', 'workflow', 'compliance', 'security', 'ml']
    tiers = ['basic', 'pro', 'enterprise']
    statuses = ['active', 'deprecated', 'beta']
    
    # Category distribution: 20 products per category
    products_per_category = n_products // len(categories)
    
    product_templates = {
        'analytics': ['Dashboard', 'Reports', 'Insights', 'Visualization', 'BI Suite',
                      'Data Explorer', 'Analytics Hub', 'Metrics', 'KPI Tracker', 'Query Builder',
                      'Data Studio', 'Analytics Pro', 'Real-time Dashboard', 'Predictive Analytics', 'Custom Reports',
                      'Performance Monitor', 'Trend Analyzer', 'Data Governance', 'Audit Trail', 'Analytics Advanced'],
        'integration': ['Connector', 'API', 'Sync Engine', 'ETL Service', 'Data Bridge',
                        'Integration Hub', 'Middleware', 'Pipeline', 'Data Flow', 'Adapter',
                        'Webhooks', 'Stream Connector', 'Batch Sync', 'Real-time Integration', 'Data Mapper',
                        'Transformation Engine', 'Queue Service', 'Event Bus', 'API Gateway', 'Integration Pro'],
        'workflow': ['Automation', 'Process Engine', 'Orchestration', 'Task Manager', 'Scheduler',
                     'Workflow Studio', 'Approval Engine', 'State Machine', 'BPM Suite', 'Forms',
                     'Workflow Builder', 'Advanced Automation', 'Complex Flows', 'Workflow Designer', 'Custom Processes',
                     'Workflow Analytics', 'Collaboration Hub', 'Task Routing', 'SLA Manager', 'Workflow Pro'],
        'compliance': ['Audit Trail', 'Policy Manager', 'Compliance Dashboard', 'Risk Assessment', 'Controls',
                       'Compliance Suite', 'Document Repository', 'Access Control', 'Encryption', 'Data Masking',
                       'GDPR Toolkit', 'Privacy Manager', 'Compliance Automation', 'Audit Reports', 'Compliance Pro',
                       'Risk Monitor', 'Policy Engine', 'Certification Manager', 'Compliance Intelligence', 'Compliance Advanced'],
        'security': ['Authentication', 'Authorization', 'Encryption', 'Threat Detection', 'Firewall',
                     'Security Hub', 'Vulnerability Scan', 'Intrusion Detection', 'DLP', 'WAF',
                     'Advanced Security', 'Threat Intelligence', 'Penetration Testing', 'Security Analytics', 'Security Pro',
                     'API Security', 'Data Security', 'Application Security', 'Identity Management', 'Security Enterprise'],
        'ml': ['Model Builder', 'Prediction Engine', 'Classification', 'Clustering', 'Regression',
               'ML Platform', 'Feature Store', 'Model Registry', 'Experiment Tracking', 'AutoML',
               'Advanced Models', 'Neural Networks', 'Custom Models', 'ML Analytics', 'ML Pro',
               'Reinforcement Learning', 'NLP Suite', 'Computer Vision', 'Ensemble Models', 'ML Enterprise']
    }
    
    product_id_counter = 0
    for category in categories:
        for j in range(products_per_category):
            product_id = f"PROD_{product_id_counter:03d}"
            product_id_counter += 1
            
            # Product name
            template = product_templates[category][j % len(product_templates[category])]
            if np.random.random() < 0.3:
                product_name = f"{category.title()} {template}"
            else:
                product_name = template
            
            # Price tier: more enterprise than basic
            tier = np.random.choice(tiers, p=[0.3, 0.4, 0.3])
            
            # Launch date: distributed across 2 years
            days_ago = np.random.randint(0, 730)
            launch_date = datetime.now() - timedelta(days=days_ago)
            
            # Status: mostly active, some deprecated/beta
            status = np.random.choice(statuses, p=[0.80, 0.12, 0.08])
            
            products.append({
                'product_id': product_id,
                'product_name': product_name,
                'category': category,
                'price_tier': tier,
                'launch_date': launch_date.strftime('%Y-%m-%d'),
                'status': status
            })
    
    return pd.DataFrame(products)


def generate_purchases(customers_df, products_df, n_purchases=1200, seed=42):
    """
    Generate purchase edges (customer buys product).
    
    Realistic distribution: 70% buy 1-5, 20% buy 5-15, 10% are power users
    
    Args:
        customers_df: Customer DataFrame
        products_df: Product DataFrame
        n_purchases: Target number of purchase edges
        seed: Random seed
    
    Returns:
        DataFrame with columns: customer_id, product_id, purchase_date, quantity, 
                               total_value, renewal_status
    """
    set_random_seed(seed)
    
    purchases = []
    customer_ids = customers_df['customer_id'].tolist()
    product_ids = products_df['product_id'].tolist()
    
    # Create purchase distribution: most customers few products, few are power users
    n_customers = len(customer_ids)
    
    # Assign purchase counts to customers (skewed)
    purchase_counts = []
    for i in range(n_customers):
        if np.random.random() < 0.10:  # 10% power users
            # Power users: 20-80 products
            count = np.random.randint(20, 81)
        elif np.random.random() < 0.20:  # Next 20% moderate
            # Moderate: 5-15 products
            count = np.random.randint(5, 16)
        else:  # 70% light users
            # Light: 1-5 products
            count = np.random.randint(1, 6)
        
        purchase_counts.append(count)
    
    total_planned = sum(purchase_counts)
    
    # Scale down if too many
    if total_planned > n_purchases * 1.5:
        scale_factor = n_purchases / total_planned
        purchase_counts = [max(1, int(pc * scale_factor)) for pc in purchase_counts]
    
    # Generate purchases
    edge_set = set()  # Track edges to avoid duplicates
    
    for customer_idx, count in enumerate(purchase_counts):
        customer_id = customer_ids[customer_idx]
        
        # Randomly select products for this customer
        selected_products = np.random.choice(product_ids, size=min(count, len(product_ids)), replace=False)
        
        for product_id in selected_products:
            edge_key = (customer_id, product_id)
            
            if edge_key not in edge_set:  # Avoid duplicate edges
                edge_set.add(edge_key)
                
                # Purchase date: within last 2 years
                days_ago = np.random.randint(0, 730)
                purchase_date = datetime.now() - timedelta(days=days_ago)
                
                # Quantity (typically 1, occasionally more for bulk)
                quantity = np.random.choice([1, 1, 1, 1, 2], p=[0.85, 0.05, 0.05, 0.03, 0.02])
                
                # Total value: product price tier affects range
                product_row = products_df[products_df['product_id'] == product_id].iloc[0]
                tier = product_row['price_tier']
                
                if tier == 'basic':
                    price = np.random.randint(1000, 5000)
                elif tier == 'pro':
                    price = np.random.randint(5000, 20000)
                else:  # enterprise
                    price = np.random.randint(20000, 100000)
                
                total_value = price * quantity
                
                # Renewal status: active, expired, pending
                renewal = np.random.choice(['active', 'expired', 'pending_renewal'], 
                                          p=[0.80, 0.15, 0.05])
                
                purchases.append({
                    'customer_id': customer_id,
                    'product_id': product_id,
                    'purchase_date': purchase_date.strftime('%Y-%m-%d'),
                    'quantity': quantity,
                    'total_value': total_value,
                    'renewal_status': renewal
                })
    
    return pd.DataFrame(purchases)


def inject_duplicates(customers_df, purchases_df, seed=42):
    """
    Inject duplicate customer records to be discovered.
    
    Args:
        customers_df: Customer DataFrame (will be modified)
        purchases_df: Purchase DataFrame (will be modified)
        seed: Random seed
    
    Returns:
        Tuple of (modified customers_df, modified purchases_df, duplicates_info)
    """
    set_random_seed(seed)
    
    duplicates_info = []
    
    # Duplicate Pair 1: "Acme Corp" variants
    idx1 = np.random.randint(0, len(customers_df) // 2)
    customers_df.iloc[idx1, customers_df.columns.get_loc('company_name')] = 'Acme Corp'
    
    idx2 = np.random.randint(len(customers_df) // 2, len(customers_df))
    customers_df.iloc[idx2, customers_df.columns.get_loc('company_name')] = 'ACME Corporation'
    
    # Make them buy same products (90% overlap)
    products_for_dup = purchases_df[purchases_df['customer_id'] == customers_df.iloc[idx1]['customer_id']]['product_id'].tolist()[:8]
    
    if len(products_for_dup) > 0:
        for product_id in products_for_dup:
            new_row = {
                'customer_id': customers_df.iloc[idx2]['customer_id'],
                'product_id': product_id,
                'purchase_date': (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d'),
                'quantity': 1,
                'total_value': np.random.randint(5000, 50000),
                'renewal_status': 'active'
            }
            purchases_df = pd.concat([purchases_df, pd.DataFrame([new_row])], ignore_index=True)
        
        duplicates_info.append({
            'type': 'name_variation',
            'customer_1': customers_df.iloc[idx1]['customer_id'],
            'customer_2': customers_df.iloc[idx2]['customer_id'],
            'name_1': customers_df.iloc[idx1]['company_name'],
            'name_2': customers_df.iloc[idx2]['company_name'],
            'similarity': 0.92
        })
    
    return customers_df, purchases_df, duplicates_info


def inject_power_user(customers_df, purchases_df, seed=42):
    """
    Inject a power user customer (buys many products).
    
    Args:
        customers_df: Customer DataFrame (will be modified)
        purchases_df: Purchase DataFrame (will be modified)
        seed: Random seed
    
    Returns:
        Tuple of (modified customers_df, modified purchases_df, power_user_info)
    """
    set_random_seed(seed)
    
    # Create power user at index
    power_user_idx = np.random.randint(0, len(customers_df))
    power_user_id = customers_df.iloc[power_user_idx]['customer_id']
    
    # Update to high value
    customers_df.iloc[power_user_idx, customers_df.columns.get_loc('account_value')] = 2500000
    customers_df.iloc[power_user_idx, customers_df.columns.get_loc('status')] = 'active'
    
    # Remove old purchases for this customer
    purchases_df = purchases_df[purchases_df['customer_id'] != power_user_id]
    
    # Get actual product list
    product_ids = purchases_df['product_id'].unique().tolist()
    if len(product_ids) == 0:
        # Fallback: use generated products
        product_ids = [f"PROD_{i:03d}" for i in range(100)]
    
    power_products = np.random.choice(product_ids, size=min(72, len(product_ids)), replace=False)
    
    for product_id in power_products:
        new_row = {
            'customer_id': power_user_id,
            'product_id': product_id,
            'purchase_date': (datetime.now() - timedelta(days=np.random.randint(100, 400))).strftime('%Y-%m-%d'),
            'quantity': np.random.choice([1, 2]),
            'total_value': np.random.randint(10000, 80000),
            'renewal_status': np.random.choice(['active', 'pending_renewal'], p=[0.9, 0.1])
        }
        purchases_df = pd.concat([purchases_df, pd.DataFrame([new_row])], ignore_index=True)
    
    return customers_df, purchases_df, {
        'customer_id': power_user_id,
        'company_name': customers_df.iloc[power_user_idx]['company_name'],
        'account_value': 2500000,
        'product_count': len(power_products)
    }


def generate_all_datasets(seed=42, output_dir=None):
    """
    Generate all sales accounts datasets and save to CSV.
    
    Args:
        seed: Random seed
        output_dir: Output directory (default: data/seed/sales_accounts/)
    """
    if output_dir is None:
        from src.config import Config
        output_dir = Config.PROJECT_ROOT / 'data' / 'seed' / 'sales_accounts'
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print("Sales Accounts & Product Network Data Generator")
    print("="*70)
    
    # Generate base data
    print("\nGenerating customers...")
    customers_df = generate_customers(n_customers=250, seed=seed)
    
    print("Generating products...")
    products_df = generate_products(n_products=120, seed=seed)
    
    print("Generating purchases...")
    purchases_df = generate_purchases(customers_df, products_df, n_purchases=1200, seed=seed)
    
    # Inject anomalies
    print("\nInjecting anomalies...")
    customers_df, purchases_df, dup_info = inject_duplicates(customers_df, purchases_df, seed)
    customers_df, purchases_df, power_info = inject_power_user(customers_df, purchases_df, seed)
    
    # Remove duplicates from purchases (in case of conflicts)
    purchases_df = purchases_df.drop_duplicates(subset=['customer_id', 'product_id'], keep='first')
    
    # Save to CSV
    print("\nSaving datasets...")
    customers_df.to_csv(output_dir / 'customers.csv', index=False)
    products_df.to_csv(output_dir / 'products.csv', index=False)
    purchases_df.to_csv(output_dir / 'purchases.csv', index=False)
    
    # Summary
    print("\n" + "-"*70)
    print("Dataset Summary:")
    print(f"  Customers: {len(customers_df)}")
    print(f"  Products: {len(products_df)}")
    print(f"  Purchases (edges): {len(purchases_df)}")
    print(f"  Bipartite density: {len(purchases_df) / (len(customers_df) * len(products_df)):.4f}")
    print(f"\n  Customers by status:")
    print(f"    {customers_df['status'].value_counts().to_string()}")
    print(f"\n  Products by category:")
    print(f"    {products_df['category'].value_counts().to_string()}")
    print(f"\n  Injected Anomalies:")
    print(f"    - Duplicate pair detected: {dup_info[0]['name_1']} vs {dup_info[0]['name_2']}")
    print(f"    - Power user: {power_info['company_name']} ({power_info['product_count']} products, ${power_info['account_value']:,.0f} value)")
    print(f"    - Single-customer products: {len(purchases_df[purchases_df['product_id'].isin(purchases_df.groupby('product_id').size()[purchases_df.groupby('product_id').size() <= 2].index)])}")
    print(f"    - Inactive customers: {len(customers_df[customers_df['status'] == 'inactive'])}")
    print("-"*70 + "\n")
    
    return customers_df, products_df, purchases_df


if __name__ == '__main__':
    generate_all_datasets(seed=42)
