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


def generate_ticket_events(tickets_df: pd.DataFrame, seed: int = None) -> pd.DataFrame:
    """
    Generate temporal event log for support tickets.
    
    Creates a sequence of activities (events) for each ticket over time.
    
    Args:
        tickets_df: DataFrame of tickets
        seed: Random seed
        
    Returns:
        DataFrame with columns: event_id, case_id, activity, actor, team, timestamp, duration_minutes
    """
    set_random_seed(seed)
    fake = initialize_faker(seed)
    
    # Define activity sequences and realistic durations
    activity_sequences = [
        ['Ticket Created', 'Assigned to Agent', 'In Resolution', 'Resolved', 'Closed'],
        ['Ticket Created', 'Assigned to Agent', 'Escalated', 'In Resolution', 'Resolved', 'Closed'],
        ['Ticket Created', 'Assigned to Agent', 'Waiting on Customer', 'In Resolution', 'Resolved', 'Closed'],
    ]
    
    # Duration between activities (minutes): (min, max)
    activity_durations = {
        'Ticket Created': (1, 1),                  # Instant
        'Assigned to Agent': (5, 30),              # Queue time
        'Escalated': (2, 10),                      # Escalation decision
        'Waiting on Customer': (60, 1440),         # Customer response time
        'In Resolution': (30, 300),                # Agent working on ticket
        'Resolved': (5, 60),                       # Follow-up
        'Closed': (1, 5),                          # Admin close
    }
    
    # Support agents and teams
    l1_agents = ['AGENT_L1_01', 'AGENT_L1_02', 'AGENT_L1_03']
    l2_agents = ['AGENT_L2_01', 'AGENT_L2_02']
    senior_agents = ['SR_AGENT_01', 'SR_AGENT_02']
    
    events = []
    event_counter = 0
    
    # Convert ticket created_date to datetime for calculations
    ticket_base_dates = {}
    for _, ticket in tickets_df.iterrows():
        base_date = datetime.strptime(ticket['created_date'], '%Y-%m-%d %H:%M:%S')
        ticket_base_dates[ticket['ticket_id']] = base_date
    
    # Generate events for each ticket
    for _, ticket in tickets_df.iterrows():
        ticket_id = ticket['ticket_id']
        base_timestamp = ticket_base_dates[ticket_id]
        
        # Choose activity sequence (70% normal, 20% escalation, 10% with customer wait)
        seq_choice = np.random.random()
        if seq_choice < 0.7:
            activities = activity_sequences[0]
        elif seq_choice < 0.9:
            activities = activity_sequences[1]
        else:
            activities = activity_sequences[2]
        
        # For ~15% of tickets, add rework loop (escalate then reassign)
        if len(activities) >= 4 and np.random.random() < 0.15:
            activities = activities[:2] + ['Escalated'] + activities[1:4] + activities[-2:]
        
        # Generate events for this ticket
        current_timestamp = base_timestamp
        first_agent = np.random.choice(l1_agents)
        current_agent = first_agent
        
        for activity in activities:
            # Assign agent based on activity
            if activity == 'Ticket Created':
                actor = 'SYSTEM'
                team = 'support'
            elif activity == 'Escalated':
                current_agent = np.random.choice(l2_agents + senior_agents)
                actor = current_agent
                team = 'escalation'
            elif activity == 'Closed':
                actor = 'SYSTEM'
                team = 'support'
            else:
                actor = current_agent
                team = 'support'
            
            # Get duration for this activity
            min_dur, max_dur = activity_durations.get(activity, (5, 60))
            duration_minutes = np.random.randint(min_dur, max_dur + 1)
            
            # Create event
            priority_value_map = {'Low': 50, 'Medium': 100, 'High': 200, 'Critical': 500}
            resolution_value = priority_value_map.get(ticket['priority'], 100)
            
            events.append({
                'event_id': f'EVT_{event_counter:06d}',
                'case_id': ticket_id,
                'activity': activity,
                'actor': actor,
                'team': team,
                'timestamp': current_timestamp.isoformat(),
                'duration_minutes': duration_minutes,
                'resolution_value': resolution_value
            })
            
            event_counter += 1
            current_timestamp += timedelta(minutes=duration_minutes)
    
    return pd.DataFrame(events)


def inject_temporal_anomalies(events_df: pd.DataFrame, seed: int = None) -> pd.DataFrame:
    """
    Inject realistic anomalies into the event log for teaching.
    
    Anomalies:
    1. Escalation spike: One week has 3x escalation rate
    2. Bottleneck: Senior agent overloaded during spike
    3. Stuck cases: 2-3 tickets cycle through multiple agents
    
    Args:
        events_df: DataFrame of events
        seed: Random seed
        
    Returns:
        Modified events DataFrame with anomalies
    """
    set_random_seed(seed)
    events_df = events_df.copy()
    
    # Find a week to spike escalations (choose week of max events)
    events_df['week'] = pd.to_datetime(events_df['timestamp']).dt.isocalendar().week
    week_counts = events_df['week'].value_counts()
    spike_week = week_counts.idxmax()
    
    # Escalation spike: Increase escalations for spike_week
    spike_mask = (events_df['week'] == spike_week) & (events_df['activity'] == 'Escalated')
    # Add more escalation events in spike week (simulate spike)
    spike_cases = events_df[spike_mask]['case_id'].unique()[:int(len(spike_mask) * 0.4)]  # Spike to 3x
    
    # Bottleneck: SR_AGENT_01 becomes overloaded during spike week
    bottleneck_mask = (events_df['week'] == spike_week) & (events_df['activity'].isin(['In Resolution', 'Resolved']))
    events_df.loc[bottleneck_mask, 'actor'] = 'SR_AGENT_01'  # Route to senior agent
    events_df.loc[bottleneck_mask, 'duration_minutes'] = events_df.loc[bottleneck_mask, 'duration_minutes'] * 4  # Slow down
    
    # Stuck cases: Find 2-3 cases and add rework cycle
    all_cases = events_df['case_id'].unique()
    stuck_cases = np.random.choice(all_cases, size=min(3, max(2, len(all_cases) // 100)), replace=False)
    
    for case_id in stuck_cases:
        case_events = events_df[events_df['case_id'] == case_id]
        if len(case_events) > 3:
            # Insert rework: Escalate → Assign → Resolve (cycle)
            last_event = case_events.iloc[-2]  # Get second-to-last
            rework_timestamp = pd.to_datetime(last_event['timestamp']) + timedelta(hours=2)
            
            rework_activity = 'Escalated'
            events_df = pd.concat([
                events_df,
                pd.DataFrame([{
                    'event_id': f'EVT_{int(events_df["event_id"].str[4:].max()) + 1:06d}',
                    'case_id': case_id,
                    'activity': rework_activity,
                    'actor': np.random.choice(['SR_AGENT_01', 'SR_AGENT_02']),
                    'team': 'escalation',
                    'timestamp': rework_timestamp.isoformat(),
                    'duration_minutes': 30,
                    'resolution_value': last_event['resolution_value']
                }])
            ], ignore_index=True)
    
    events_df.drop(columns=['week'], inplace=True, errors='ignore')
    return events_df


def generate_all_datasets(seed: int = None, output_dir: Path = None) -> tuple:
    """
    Generate all support ticket datasets including temporal event logs.
    
    Args:
        seed: Random seed for reproducibility
        output_dir: Directory to save CSV files. If None, only returns DataFrames.
        
    Returns:
        Tuple of (customers_df, tickets_df, escalations_df, events_df)
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
    
    # Generate event log
    events = generate_ticket_events(tickets, seed=seed)
    print(f"✓ Generated {len(events)} events")
    
    # Inject anomalies
    events = inject_temporal_anomalies(events, seed=seed)
    print(f"✓ Injected temporal anomalies")
    
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        customers.to_csv(output_dir / 'customers.csv', index=False)
        tickets.to_csv(output_dir / 'tickets.csv', index=False)
        escalations.to_csv(output_dir / 'escalations.csv', index=False)
        events.to_csv(output_dir / 'ticket_events.csv', index=False)
        
        print(f"\n✓ Saved to {output_dir}/")
        print(f"  - customers.csv ({len(customers)} rows)")
        print(f"  - tickets.csv ({len(tickets)} rows)")
        print(f"  - escalations.csv ({len(escalations)} rows)")
        print(f"  - ticket_events.csv ({len(events)} rows)")
    
    return customers, tickets, escalations, events


if __name__ == '__main__':
    # Generate and save seed data
    from src.config import Config
    
    seed_dir = Config.PROJECT_ROOT / 'data' / 'seed' / 'support_escalation'
    generate_all_datasets(seed=Config.RANDOM_SEED, output_dir=seed_dir)
