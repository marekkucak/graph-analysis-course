"""
Generate synthetic approval handoff dataset for Lesson 05 - Community Detection.

Creates a realistic organizational approval workflow network with:
- Departments (6) and people (28) with departmental assignments
- Documents (240) requiring approval with document types
- Approval handoffs (580) person-to-person edges weighted by frequency

Used for teaching community detection to reveal organizational structure.

Key insight: Most approvals stay within department (80%), with specific
cross-department bridges (20%). Community detection should recover departments.
"""

from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from pathlib import Path

from src.config import Config
from src.data_generation.common import initialize_faker, generate_timestamps, set_random_seed


def generate_departments(n_departments: int = 6, seed: int = None) -> pd.DataFrame:
    """
    Generate department data.
    
    Args:
        n_departments: Number of departments
        seed: Random seed
        
    Returns:
        DataFrame with columns: department_id, name
    """
    set_random_seed(seed)
    
    dept_names = [
        'Finance',
        'Human Resources',
        'Legal',
        'Operations',
        'Engineering',
        'Marketing'
    ]
    
    departments = []
    for i in range(n_departments):
        departments.append({
            'department_id': f'DEPT_{i:02d}',
            'name': dept_names[i] if i < len(dept_names) else f'Department {i}',
            'manager_count': np.random.randint(1, 2),
        })
    
    return pd.DataFrame(departments)


def generate_people(n_people: int = 28, seed: int = None) -> pd.DataFrame:
    """
    Generate people data distributed across departments.
    
    Args:
        n_people: Number of people
        seed: Random seed
        
    Returns:
        DataFrame with columns: person_id, name, email, department_id, is_manager, level
    """
    set_random_seed(seed)
    fake = initialize_faker(seed)
    
    # Distribute people across departments
    dept_distribution = {
        'DEPT_00': 5,  # Finance
        'DEPT_01': 5,  # HR
        'DEPT_02': 4,  # Legal
        'DEPT_03': 5,  # Operations
        'DEPT_04': 4,  # Engineering
        'DEPT_05': 3,  # Marketing
    }
    
    people = []
    person_idx = 0
    
    for dept_id, count in dept_distribution.items():
        for i in range(count):
            is_manager = (i == 0)  # First person in each department is manager
            level = 'Manager' if is_manager else np.random.choice(['Junior', 'Mid', 'Senior'])
            
            people.append({
                'person_id': f'PERSON_{person_idx:02d}',
                'name': fake.name(),
                'email': fake.email(),
                'department_id': dept_id,
                'is_manager': is_manager,
                'level': level,
            })
            person_idx += 1
    
    return pd.DataFrame(people)


def generate_documents(n_documents: int = 240, seed: int = None) -> pd.DataFrame:
    """
    Generate document data requiring approvals.
    
    Args:
        n_documents: Number of documents
        seed: Random seed
        
    Returns:
        DataFrame with columns: document_id, document_type, created_date
    """
    set_random_seed(seed)
    fake = initialize_faker(seed)
    
    doc_types = ['Expense Report', 'Procurement', 'Policy Update', 'Contract', 'Termination', 'Hiring']
    created_dates = generate_timestamps(n_documents, start_date='2024-01-01', end_date='2024-12-31', seed=seed)
    
    documents = []
    for i in range(n_documents):
        documents.append({
            'document_id': f'DOC_{i:04d}',
            'document_type': np.random.choice(doc_types),
            'created_date': created_dates[i].strftime('%Y-%m-%d %H:%M:%S'),
        })
    
    return pd.DataFrame(documents)


def generate_approvals(people_df: pd.DataFrame, n_approvals: int = 580, seed: int = None) -> pd.DataFrame:
    """
    Generate approval handoff edges (person-to-person approval chains).
    
    Creates a structured approval network with document-based routing:
    - Documents flow through approval chains
    - Most approvals within department (tight clusters)
    - Some cross-department bridges
    
    Args:
        people_df: DataFrame of people
        n_approvals: Target number of approval edges
        seed: Random seed
        
    Returns:
        DataFrame with columns: from_person_id, to_person_id, approval_count
    """
    set_random_seed(seed)
    
    # Group people by department
    dept_people = {}
    for dept_id in people_df['department_id'].unique():
        dept_people[dept_id] = people_df[people_df['department_id'] == dept_id]['person_id'].tolist()
    
    # Create approval chains based on departments
    approval_counts = {}
    
    # Phase 1: Within-department approvals (build approval chains within departments)
    for dept_id, people_list in dept_people.items():
        # Create approval chains within department
        # Build multiple rounds of approval chains for density
        for _ in range(10):  # Multiple passes to create more edges
            shuffled = people_list.copy()
            np.random.shuffle(shuffled)
            
            # Create chains: each person approves to next 1-3 people
            for i, person in enumerate(shuffled):
                num_approves_to = np.random.randint(2, 4)  # Approves to 2-3 people
                for j in range(1, num_approves_to + 1):
                    if i + j < len(shuffled):
                        target = shuffled[i + j]
                        edge = (person, target)
                        if edge not in approval_counts:
                            approval_counts[edge] = 0
                        approval_counts[edge] += np.random.randint(3, 12)  # Higher frequency within dept
    
    # Phase 2: Cross-department bridges between adjacent departments
    dept_ids = list(dept_people.keys())
    for i in range(len(dept_ids) - 1):
        dept1 = dept_ids[i]
        dept2 = dept_ids[i + 1]
        
        # Create 5-8 bridge people from each department to next
        num_bridges = np.random.randint(5, 9)
        for _ in range(num_bridges):
            from_person = np.random.choice(dept_people[dept1])
            to_person = np.random.choice(dept_people[dept2])
            edge = (from_person, to_person)
            if edge not in approval_counts:
                approval_counts[edge] = 0
            approval_counts[edge] += np.random.randint(2, 6)  # Lower frequency for cross-dept
    
    # Phase 3: Add more random within-department edges to boost total
    for _ in range(300):
        dept_id = np.random.choice(dept_ids)
        people_list = dept_people[dept_id]
        if len(people_list) >= 2:
            from_person = np.random.choice(people_list)
            to_person = np.random.choice(people_list)
            if from_person != to_person:
                edge = (from_person, to_person)
                if edge not in approval_counts:
                    approval_counts[edge] = 0
                approval_counts[edge] += np.random.randint(2, 10)
    
    # Phase 4: Add random cross-department edges to reach target
    num_random_cross = int(n_approvals * 0.2)  # 20% random cross-dept
    for _ in range(num_random_cross):
        dept1, dept2 = np.random.choice(dept_ids, 2, replace=False)
        from_person = np.random.choice(dept_people[dept1])
        to_person = np.random.choice(dept_people[dept2])
        edge = (from_person, to_person)
        if edge not in approval_counts:
            approval_counts[edge] = 0
        approval_counts[edge] += np.random.randint(1, 3)
    
    # Convert to DataFrame and normalize to target count
    approval_list = [
        {'from_person_id': edge[0], 'to_person_id': edge[1], 'approval_count': count}
        for edge, count in approval_counts.items()
    ]
    
    # If we have more edges than target, downsample by removing low-count edges
    if len(approval_list) > n_approvals:
        approval_df = pd.DataFrame(approval_list).sort_values('approval_count', ascending=False)
        approval_df = approval_df.head(n_approvals).reset_index(drop=True)
    else:
        approval_df = pd.DataFrame(approval_list)
    
    return approval_df


def generate_all_datasets(seed: int = 42, output_dir: str = None) -> None:
    """
    Generate all datasets and save to CSVs.
    
    Args:
        seed: Random seed for reproducibility
        output_dir: Output directory path (default: data/seed/approval_handoffs)
    """
    set_random_seed(seed)
    
    if output_dir is None:
        output_dir = Config.PROJECT_ROOT / 'data' / 'seed' / 'approval_handoffs'
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating approval handoff dataset with seed={seed}...")
    
    # Generate datasets
    departments_df = generate_departments(n_departments=6, seed=seed)
    people_df = generate_people(n_people=28, seed=seed)
    documents_df = generate_documents(n_documents=240, seed=seed)
    approvals_df = generate_approvals(people_df, n_approvals=580, seed=seed)
    
    # Save to CSV
    departments_df.to_csv(output_dir / 'departments.csv', index=False)
    people_df.to_csv(output_dir / 'people.csv', index=False)
    documents_df.to_csv(output_dir / 'documents.csv', index=False)
    approvals_df.to_csv(output_dir / 'approvals.csv', index=False)
    
    # Verification output
    print(f"\nDataset Generation Complete:")
    print(f"  Departments: {len(departments_df)}")
    print(f"  People: {len(people_df)} (distributed across departments)")
    print(f"  Documents: {len(documents_df)}")
    print(f"  Approvals: {len(approvals_df)} edges")
    
    # Analysis
    dept_distribution = people_df.groupby('department_id').size()
    print(f"\nDepartment Distribution:")
    for dept_id, count in dept_distribution.items():
        dept_name = departments_df[departments_df['department_id'] == dept_id]['name'].values[0]
        print(f"  {dept_name}: {count} people")
    
    # Within vs cross-department
    within = 0
    cross = 0
    for _, row in approvals_df.iterrows():
        from_dept = people_df[people_df['person_id'] == row['from_person_id']]['department_id'].values[0]
        to_dept = people_df[people_df['person_id'] == row['to_person_id']]['department_id'].values[0]
        if from_dept == to_dept:
            within += 1
        else:
            cross += 1
    
    print(f"\nApproval Structure:")
    print(f"  Within-department: {within} ({100*within/len(approvals_df):.1f}%)")
    print(f"  Cross-department: {cross} ({100*cross/len(approvals_df):.1f}%)")
    
    # Identify bridges (people with many cross-dept approvals)
    bridge_counts = {}
    for _, row in approvals_df.iterrows():
        from_dept = people_df[people_df['person_id'] == row['from_person_id']]['department_id'].values[0]
        to_dept = people_df[people_df['person_id'] == row['to_person_id']]['department_id'].values[0]
        if from_dept != to_dept:
            person_id = row['from_person_id']
            if person_id not in bridge_counts:
                bridge_counts[person_id] = 0
            bridge_counts[person_id] += row['approval_count']
    
    if bridge_counts:
        print(f"\nIdentified Bridge People (cross-department approvals):")
        for person_id in sorted(bridge_counts.keys(), key=lambda x: bridge_counts[x], reverse=True)[:5]:
            person_name = people_df[people_df['person_id'] == person_id]['name'].values[0]
            person_dept = people_df[people_df['person_id'] == person_id]['department_id'].values[0]
            dept_name = departments_df[departments_df['department_id'] == person_dept]['name'].values[0]
            print(f"  {person_name} ({dept_name}): {bridge_counts[person_id]} cross-dept approvals")
    
    print(f"\nSaved to: {output_dir}")


if __name__ == '__main__':
    generate_all_datasets(seed=42)
