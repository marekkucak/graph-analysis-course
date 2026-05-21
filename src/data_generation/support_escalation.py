"""
Generate synthetic support ticket dataset for Lesson 02 - NetworkX Foundations.

Creates a realistic support ticket system with:
- Customers (20) with regions and priority levels
- Support tickets (50) with statuses and priorities
- Escalation paths (agent-to-agent routing for complex issues)

Used for teaching graph construction from relational data.
"""

from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from pathlib import Path

from src.config import Config
from src.data_generation.common import initialize_faker, generate_timestamps, set_random_seed


def generate_customers(n_customers: int = 20, seed: int = None) -> pd.DataFrame:
    """
    Generate customer data.
    
    Args:
        n_customers: Number of customers
        seed: Random seed
        
    Returns:
        DataFrame with columns: customer_id, name, region, priority_level
    """
    set_random_seed(seed)
    fake = initialize_faker(seed)
    
    regions = ['North', 'South', 'East', 'West', 'Central']
    priority_levels = ['Low', 'Medium', 'High', 'Critical']
    
    customers = []
    for i in range(n_customers):
        customers.append({
            'customer_id': f'CUST_{i+1:03d}',
            'name': fake.company(),
            'region': np.random.choice(regions),
            'priority_level': np.random.choice(priority_levels, p=[0.4, 0.35, 0.20, 0.05])
        })
    
    return pd.DataFrame(customers)


def generate_tickets(customers_df: pd.DataFrame, n_tickets: int = 50, seed: int = None) -> pd.DataFrame:
    """
    Generate support ticket data.
    
    Args:
        customers_df: DataFrame of customers (for assigning tickets)
        n_tickets: Number of tickets to generate
        seed: Random seed
        
    Returns:
        DataFrame with columns: ticket_id, customer_id, status, priority, created_date, resolved_date
    """
    set_random_seed(seed)
    fake = initialize_faker(seed)
    
    statuses = ['Open', 'In Progress', 'Waiting', 'Resolved', 'Closed']
    priorities = ['Low', 'Medium', 'High', 'Critical']
    
    created_dates = generate_timestamps(n_tickets, start_date='2024-01-01', end_date='2024-12-01', seed=seed)
    
    tickets = []
    for i in range(n_tickets):
        created = created_dates[i]
        resolved = created + timedelta(days=np.random.randint(1, 30)) if np.random.random() > 0.3 else None
        
        tickets.append({
            'ticket_id': f'TKT_{i+1:04d}',
            'customer_id': np.random.choice(customers_df['customer_id']),
            'status': np.random.choice(statuses),
            'priority': np.random.choice(priorities, p=[0.3, 0.4, 0.20, 0.10]),
            'created_date': created.strftime('%Y-%m-%d %H:%M:%S'),
            'resolved_date': resolved.strftime('%Y-%m-%d %H:%M:%S') if resolved else None
        })
    
    return pd.DataFrame(tickets)


def generate_escalations(tickets_df: pd.DataFrame, seed: int = None) -> pd.DataFrame:
    """
    Generate escalation paths (agent-to-agent routing).
    
    Args:
        tickets_df: DataFrame of tickets
        seed: Random seed
        
    Returns:
        DataFrame with columns: ticket_id, from_agent, to_agent, escalation_level
    """
    set_random_seed(seed)
    
    # Define support agent roles
    agents = [
        'Agent_L1_01', 'Agent_L1_02', 'Agent_L1_03',  # Tier 1: Front-line support
        'Agent_L2_01', 'Agent_L2_02',                  # Tier 2: Specialized support
        'Supervisor_01', 'Manager_01'                   # Tier 3: Management
    ]
    
    escalations = []
    
    # About 40% of tickets get escalated at least once
    for ticket_id in tickets_df['ticket_id'].values:
        if np.random.random() < 0.4:
            # Determine escalation chain
            from_agent = np.random.choice(agents[:3])  # Start with L1
            
            if np.random.random() < 0.7:  # 70% escalate to L2
                to_agent = np.random.choice(agents[3:5])  # Go to L2
                escalations.append({
                    'ticket_id': ticket_id,
                    'from_agent': from_agent,
                    'to_agent': to_agent,
                    'escalation_level': 1
                })
            
            # Some further escalate to management
            if np.random.random() < 0.3:
                escalations.append({
                    'ticket_id': ticket_id,
                    'from_agent': to_agent if len(escalations) > 0 else from_agent,
                    'to_agent': np.random.choice(agents[5:7]),  # Go to Supervisor/Manager
                    'escalation_level': 2
                })
    
    return pd.DataFrame(escalations)


def generate_all_datasets(seed: int = None, output_dir: Path = None) -> tuple:
    """
    Generate all support ticket datasets.
    
    Args:
        seed: Random seed for reproducibility
        output_dir: Directory to save CSV files. If None, only returns DataFrames.
        
    Returns:
        Tuple of (customers_df, tickets_df, escalations_df)
    """
    if seed is None:
        seed = Config.RANDOM_SEED
    
    set_random_seed(seed)
    
    print(f"Generating support ticket dataset (seed={seed})...")
    
    customers = generate_customers(n_customers=20, seed=seed)
    print(f"✓ Generated {len(customers)} customers")
    
    tickets = generate_tickets(customers, n_tickets=50, seed=seed)
    print(f"✓ Generated {len(tickets)} tickets")
    
    escalations = generate_escalations(tickets, seed=seed)
    print(f"✓ Generated {len(escalations)} escalation records")
    
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        customers.to_csv(output_dir / 'customers.csv', index=False)
        tickets.to_csv(output_dir / 'tickets.csv', index=False)
        escalations.to_csv(output_dir / 'escalations.csv', index=False)
        
        print(f"\n✓ Saved to {output_dir}/")
        print(f"  - customers.csv ({len(customers)} rows)")
        print(f"  - tickets.csv ({len(tickets)} rows)")
        print(f"  - escalations.csv ({len(escalations)} rows)")
    
    return customers, tickets, escalations


if __name__ == '__main__':
    # Generate and save seed data
    from src.config import Config
    
    seed_dir = Config.PROJECT_ROOT / 'data' / 'seed'
    generate_all_datasets(seed=Config.RANDOM_SEED, output_dir=seed_dir)
