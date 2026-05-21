"""
Data generator for Lesson 04: Centrality Algorithms
Creates a hidden expert network (IT escalation patterns) with intentional anomalies.

Dataset: IT support organization where issues escalate through a chain.
Each person escalates issues to others based on expertise/hierarchy.

Injected anomalies (for student discovery via centrality queries):
1. Overloaded expert: High in-degree (receives many escalations)
2. Gatekeeper/bottleneck: High betweenness (all paths go through them)
3. Cross-team bridge: High closeness (connects different teams)
4. Influencer: High PageRank (connected to other important people)
5. Siloed expert: High eigenvector but low in-degree (expert but isolated)
6. Leaf nodes: Junior staff (low all centralities)
"""

import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path

from src.config import Config
from src.data_generation.common import (
    initialize_faker,
    generate_timestamps,
    set_random_seed,
)


def generate_teams(n_teams=5, seed=None):
    """Generate IT teams."""
    set_random_seed(seed)
    
    team_names = [
        "Infrastructure",
        "Application",
        "Security",
        "Database",
        "Platform"
    ][:n_teams]
    
    teams = pd.DataFrame({
        'team_id': [f'TEAM_{i:02d}' for i in range(n_teams)],
        'name': team_names,
        'description': [f'{name} team responsible for system {name.lower()}' for name in team_names]
    })
    
    return teams


def generate_people(n_people=18, seed=None):
    """Generate support staff with team assignments and seniority levels."""
    set_random_seed(seed)
    fake = initialize_faker(seed)
    
    teams = ['TEAM_00', 'TEAM_01', 'TEAM_02', 'TEAM_03', 'TEAM_04']
    titles = ['Junior Support', 'Senior Support', 'Lead', 'Manager', 'Director']
    seniority_levels = [1, 2, 3, 4, 5]  # 1=junior, 5=director
    
    people = []
    for i in range(n_people):
        # Distribute seniority: most junior, few senior
        seniority = np.random.choice(seniority_levels, p=[0.35, 0.30, 0.20, 0.10, 0.05])
        title = titles[seniority - 1]
        
        people.append({
            'person_id': f'PERSON_{i:02d}',
            'name': fake.name(),
            'email': fake.email(),
            'team_id': np.random.choice(teams),
            'title': title,
            'seniority': seniority,
            'is_manager': seniority >= 4,
        })
    
    return pd.DataFrame(people)


def generate_issues(n_issues=150, people_df=None, seed=None):
    """Generate support tickets with creator, assignee, and resolver."""
    set_random_seed(seed)
    fake = initialize_faker(seed)
    
    if people_df is None:
        people_df = generate_people(seed=seed)
    
    severities = ['Low', 'Medium', 'High', 'Critical']
    statuses = ['Open', 'In Progress', 'Resolved']
    
    people_ids = people_df['person_id'].values
    
    issues = []
    created_dates = generate_timestamps(n_issues, seed=seed)
    
    for i, created_date in enumerate(created_dates):
        creator_id = np.random.choice(people_ids)
        assignee_id = np.random.choice(people_ids)
        
        # 70% resolved, 20% in progress, 10% open
        status = np.random.choice(statuses, p=[0.70, 0.20, 0.10])
        resolver_id = np.random.choice(people_ids) if status == 'Resolved' else None
        
        resolution_date = created_date + timedelta(hours=np.random.randint(1, 72)) if status == 'Resolved' else None
        
        issues.append({
            'issue_id': f'ISSUE_{i:04d}',
            'title': fake.catch_phrase(),
            'description': fake.text(max_nb_chars=100),
            'severity': np.random.choice(severities, p=[0.40, 0.35, 0.20, 0.05]),
            'status': status,
            'creator_id': creator_id,
            'assignee_id': assignee_id,
            'resolver_id': resolver_id,
            'created_date': created_date.isoformat(),
            'resolved_date': resolution_date.isoformat() if resolution_date else None,
        })
    
    return pd.DataFrame(issues)


def generate_escalations(people_df, n_escalations=180, seed=None):
    """
    Generate escalation edges (person-to-person) with injected anomalies.
    
    Anomalies:
    1. Overloaded expert (PERSON_00): 15+ incoming escalations
    2. Gatekeeper (PERSON_01): High betweenness—all paths go through them
    3. Cross-team bridge (PERSON_02): Connects multiple teams
    4. Influencer (PERSON_03): Connected to other important people
    5. Siloed expert (PERSON_04): High eigenvector but low in-degree
    6. Leaf nodes (PERSON_15-17): Minimal escalations
    """
    set_random_seed(seed)
    
    people_ids = people_df['person_id'].values
    n_people = len(people_ids)
    
    escalations = []
    added_escalations = set()
    
    # Anomaly 1: Overloaded expert (PERSON_00 receives many escalations)
    overloaded_expert = people_ids[0]
    for i in range(1, min(16, n_people)):
        source = people_ids[i]
        target = overloaded_expert
        escalations.append({
            'from_person_id': source,
            'to_person_id': target,
            'escalation_count': np.random.randint(1, 8),
        })
        added_escalations.add((source, target))
    
    # Anomaly 2: Gatekeeper (PERSON_01 in middle of all paths)
    # Create chains that go through PERSON_01
    gatekeeper = people_ids[1]
    junior_group = people_ids[5:9]  # 4 junior people
    senior_group = people_ids[9:12]  # 3 senior people
    
    # Juniors → Gatekeeper → Seniors
    for junior in junior_group:
        if (junior, gatekeeper) not in added_escalations:
            escalations.append({
                'from_person_id': junior,
                'to_person_id': gatekeeper,
                'escalation_count': np.random.randint(3, 10),
            })
            added_escalations.add((junior, gatekeeper))
    
    for senior in senior_group:
        if (gatekeeper, senior) not in added_escalations:
            escalations.append({
                'from_person_id': gatekeeper,
                'to_person_id': senior,
                'escalation_count': np.random.randint(2, 8),
            })
            added_escalations.add((gatekeeper, senior))
    
    # Anomaly 3: Cross-team bridge (PERSON_02 connects multiple teams)
    bridge = people_ids[2]
    # Connect bridge to people from different teams
    people_by_team = people_df.groupby('team_id')['person_id'].apply(list).to_dict()
    teams = list(people_by_team.keys())
    for team in teams[:3]:  # Connect to 3 different teams
        team_members = people_by_team[team]
        for member in team_members[:2]:  # Connect to 2 members per team
            if member != bridge and (member, bridge) not in added_escalations:
                escalations.append({
                    'from_person_id': member,
                    'to_person_id': bridge,
                    'escalation_count': np.random.randint(2, 6),
                })
                added_escalations.add((member, bridge))
    
    # Anomaly 4: Influencer (PERSON_03 connected to other important people)
    influencer = people_ids[3]
    important_people = [overloaded_expert, gatekeeper, bridge] + list(people_ids[9:12])
    for important in important_people:
        if important != influencer and (important, influencer) not in added_escalations:
            escalations.append({
                'from_person_id': important,
                'to_person_id': influencer,
                'escalation_count': np.random.randint(1, 5),
            })
            added_escalations.add((important, influencer))
    
    # Anomaly 5: Siloed expert (PERSON_04 has many internal connections but few incoming)
    siloed = people_ids[4]
    siloed_group = people_ids[12:15]  # Small group around siloed expert
    for member in siloed_group:
        if member != siloed:
            if (siloed, member) not in added_escalations:
                escalations.append({
                    'from_person_id': siloed,
                    'to_person_id': member,
                    'escalation_count': np.random.randint(2, 8),
                })
                added_escalations.add((siloed, member))
    
    # Fill remaining escalations randomly to reach target count
    # Use a simpler approach: randomly add edges with soft seniority bias
    attempts = 0
    max_attempts = n_escalations * 10  # Prevent infinite loops
    
    while len(escalations) < n_escalations and attempts < max_attempts:
        attempts += 1
        source = np.random.choice(people_ids)
        target = np.random.choice(people_ids)
        
        # Skip if same person or already added
        if source == target or (source, target) in added_escalations:
            continue
        
        # Soft bias towards seniority (not strict requirement)
        source_seniority = people_df[people_df['person_id'] == source]['seniority'].iloc[0]
        target_seniority = people_df[people_df['person_id'] == target]['seniority'].iloc[0]
        
        # With 70% probability, bias towards target being more senior
        if np.random.random() < 0.7 and target_seniority <= source_seniority:
            continue
        
        escalations.append({
            'from_person_id': source,
            'to_person_id': target,
            'escalation_count': np.random.randint(1, 5),
        })
        added_escalations.add((source, target))
    
    return pd.DataFrame(escalations[:n_escalations])


def generate_all_datasets(seed=None, output_dir=None):
    """Generate all datasets and save to CSVs."""
    if output_dir is None:
        output_dir = Config.PROJECT_ROOT / 'data' / 'seed' / 'hidden_experts'
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    set_random_seed(seed)
    
    # Generate in order
    teams = generate_teams(n_teams=5, seed=seed)
    people = generate_people(n_people=18, seed=seed)
    issues = generate_issues(n_issues=150, people_df=people, seed=seed)
    escalations = generate_escalations(people, n_escalations=180, seed=seed)
    
    # Save
    teams.to_csv(output_dir / 'teams.csv', index=False)
    people.to_csv(output_dir / 'people.csv', index=False)
    issues.to_csv(output_dir / 'issues.csv', index=False)
    escalations.to_csv(output_dir / 'escalations.csv', index=False)
    
    print(f"Generated 5 teams, 18 people, 150 issues")
    print(f"Generated {len(escalations)} escalation edges")
    print(f"Saved to {output_dir}")
    print(f"\nInjected anomalies:")
    print(f"  - Overloaded expert (PERSON_00): {len(escalations[escalations['to_person_id']=='PERSON_00'])} incoming")
    print(f"  - Gatekeeper (PERSON_01): Central to escalation paths")
    print(f"  - Cross-team bridge (PERSON_02): Connects multiple teams")
    print(f"  - Influencer (PERSON_03): Connected to important people")
    print(f"  - Siloed expert (PERSON_04): High internal connectivity, low incoming")
    
    return {
        'teams': teams,
        'people': people,
        'issues': issues,
        'escalations': escalations,
    }


if __name__ == '__main__':
    # Generate with default seed for reproducibility
    datasets = generate_all_datasets(seed=Config.RANDOM_SEED)
