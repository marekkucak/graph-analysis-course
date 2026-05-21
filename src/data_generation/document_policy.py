"""
Generate synthetic document-policy governance network for Lesson 03 - Graph Profiling.

Creates a realistic document governance system with:
- Documents (100) with status (active/deprecated/draft) and ownership
- Policy topics (15) for document categorization
- Document owners (10) responsible for sets of documents
- Teams (8) that use documents
- Document references (300) - document-to-document citations (weighted by usage)
- Team usage (200) - which teams use which documents
- Injected anomalies for student discovery:
  * Obsolete but used documents (deprecated but high degree)
  * Ownerless critical documents (high degree, no owner)
  * Isolated clusters (siloed documentation)
  * Dense duplicates (over-referencing)

Used for teaching graph profiling before running algorithms.
"""

from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from pathlib import Path

from src.config import Config
from src.data_generation.common import initialize_faker, generate_timestamps, set_random_seed


def generate_topics(n_topics: int = 15, seed: int = None) -> pd.DataFrame:
    """
    Generate policy topics/categories.
    
    Args:
        n_topics: Number of topics
        seed: Random seed
        
    Returns:
        DataFrame with columns: topic_id, name, category
    """
    set_random_seed(seed)
    
    categories = ['Compliance', 'Operations', 'Security', 'Finance', 'HR']
    topic_names = [
        'Data Privacy', 'Access Control', 'Financial Reporting', 'Employee Benefits',
        'Procurement', 'Risk Management', 'Audit Trails', 'Incident Response',
        'Disaster Recovery', 'Change Management', 'Quality Assurance', 'Retention',
        'Governance', 'Training', 'Certification'
    ]
    
    topics = []
    for i in range(n_topics):
        topics.append({
            'topic_id': f'TOPIC_{i+1:02d}',
            'name': topic_names[i] if i < len(topic_names) else f'Topic_{i+1}',
            'category': np.random.choice(categories)
        })
    
    return pd.DataFrame(topics)


def generate_owners(n_owners: int = 10, seed: int = None) -> pd.DataFrame:
    """
    Generate document owners (people responsible for documents).
    
    Args:
        n_owners: Number of owners
        seed: Random seed
        
    Returns:
        DataFrame with columns: owner_id, name, email, department
    """
    set_random_seed(seed)
    fake = initialize_faker(seed)
    
    departments = ['Compliance', 'Operations', 'IT', 'Finance', 'Legal', 'HR']
    
    owners = []
    for i in range(n_owners):
        name = fake.name()
        owners.append({
            'owner_id': f'O_{i+1:03d}',
            'name': name,
            'email': fake.email(),
            'department': np.random.choice(departments)
        })
    
    return pd.DataFrame(owners)


def generate_teams(n_teams: int = 8, seed: int = None) -> pd.DataFrame:
    """
    Generate teams that consume documents.
    
    Args:
        n_teams: Number of teams
        seed: Random seed
        
    Returns:
        DataFrame with columns: team_id, name, size
    """
    set_random_seed(seed)
    fake = initialize_faker(seed)
    
    teams = []
    for i in range(n_teams):
        teams.append({
            'team_id': f'T_{i+1:02d}',
            'name': f'{fake.word().capitalize()} Team',
            'size': np.random.randint(5, 50)
        })
    
    return pd.DataFrame(teams)


def generate_documents(n_documents: int = 100, owners_df: pd.DataFrame = None, 
                      topics_df: pd.DataFrame = None, seed: int = None) -> pd.DataFrame:
    """
    Generate documents with attributes and potential anomalies.
    
    Args:
        n_documents: Number of documents
        owners_df: DataFrame of owners (for assignment)
        topics_df: DataFrame of topics (for categorization)
        seed: Random seed
        
    Returns:
        DataFrame with columns: document_id, name, status, owner_id, topic_id, created_date, modified_date
    """
    set_random_seed(seed)
    fake = initialize_faker(seed)
    
    statuses = ['active', 'deprecated', 'draft']
    status_dist = [0.7, 0.15, 0.15]  # Most active, some deprecated, some draft
    
    created_dates = generate_timestamps(n_documents, start_date='2022-01-01', end_date='2024-01-01', seed=seed)
    
    documents = []
    for i in range(n_documents):
        created = created_dates[i]
        modified = created + timedelta(days=np.random.randint(0, 365)) if np.random.random() > 0.3 else created
        
        # Assign owner (some documents will be ownerless - anomaly)
        if np.random.random() < 0.95:  # 95% have owner
            owner_id = owners_df.iloc[np.random.randint(0, len(owners_df))]['owner_id']
        else:
            owner_id = None
        
        # Assign topic
        topic_id = topics_df.iloc[np.random.randint(0, len(topics_df))]['topic_id']
        
        documents.append({
            'document_id': f'DOC_{i+1:04d}',
            'name': f'{fake.word().capitalize()} - {fake.word().capitalize()}',
            'status': np.random.choice(statuses, p=status_dist),
            'owner_id': owner_id,
            'topic_id': topic_id,
            'created_date': created.strftime('%Y-%m-%d'),
            'modified_date': modified.strftime('%Y-%m-%d')
        })
    
    return pd.DataFrame(documents)


def generate_references(documents_df: pd.DataFrame, n_references: int = 300, seed: int = None) -> pd.DataFrame:
    """
    Generate document-to-document references (citations/edges).
    Includes injected anomalies:
    - Some deprecated documents referenced heavily (obsolete but used)
    - Isolated clusters (documents only reference within small group)
    - Dense duplicates (cliques of over-referenced documents)
    
    Args:
        documents_df: DataFrame of documents
        n_references: Number of reference edges
        seed: Random seed
        
    Returns:
        DataFrame with columns: from_doc_id, to_doc_id, weight (usage count)
    """
    set_random_seed(seed)
    
    references = []
    doc_ids = documents_df['document_id'].values
    
    # Inject Anomaly 1: Isolated cluster (6-8 docs that only reference each other)
    isolated_cluster_docs = doc_ids[80:87]  # Last 7 documents form isolated cluster
    for i in range(len(isolated_cluster_docs)):
        for j in range(i+1, len(isolated_cluster_docs)):
            references.append({
                'from_doc_id': isolated_cluster_docs[i],
                'to_doc_id': isolated_cluster_docs[j],
                'weight': np.random.randint(1, 4)
            })
    
    # Inject Anomaly 2: Dense duplicate clique (10 docs that heavily reference each other)
    duplicate_clique = doc_ids[65:75]  # 10 documents (65-74)
    for i in range(len(duplicate_clique)):
        for j in range(i+1, len(duplicate_clique)):
            references.append({
                'from_doc_id': duplicate_clique[i],
                'to_doc_id': duplicate_clique[j],
                'weight': np.random.randint(3, 6)  # High weight - heavily cross-referenced
            })
    
    # Generate random references for remaining slots
    remaining_refs = n_references - len(references)
    for _ in range(remaining_refs):
        from_doc = np.random.choice(doc_ids)
        to_doc = np.random.choice(doc_ids)
        
        # Avoid self-loops and duplicates
        if from_doc == to_doc:
            continue
        
        # Check if already exists
        exists = any(
            (r['from_doc_id'] == from_doc and r['to_doc_id'] == to_doc) or
            (r['from_doc_id'] == to_doc and r['to_doc_id'] == from_doc)
            for r in references
        )
        if exists:
            continue
        
        references.append({
            'from_doc_id': from_doc,
            'to_doc_id': to_doc,
            'weight': np.random.randint(1, 5)
        })
        
        if len(references) >= n_references:
            break
    
    return pd.DataFrame(references)


def generate_usages(documents_df: pd.DataFrame, teams_df: pd.DataFrame, 
                   n_usages: int = 200, seed: int = None) -> pd.DataFrame:
    """
    Generate team-document usage relationships.
    Includes injected anomaly: some deprecated docs heavily used by teams.
    
    Args:
        documents_df: DataFrame of documents
        teams_df: DataFrame of teams
        n_usages: Number of usage edges
        seed: Random seed
        
    Returns:
        DataFrame with columns: team_id, document_id, usage_count
    """
    set_random_seed(seed)
    
    usages = []
    doc_ids = documents_df['document_id'].values
    team_ids = teams_df['team_id'].values
    deprecated_docs = documents_df[documents_df['status'] == 'deprecated']['document_id'].values
    
    # Inject Anomaly 3: Deprecated but heavily used documents (governance debt)
    # Pick 3-5 deprecated docs and make them heavily used
    if len(deprecated_docs) > 0:
        anomaly_deps = np.random.choice(deprecated_docs, size=min(5, len(deprecated_docs)), replace=False)
        for dep_doc in anomaly_deps:
            # This doc is used by many teams
            for team_id in np.random.choice(team_ids, size=np.random.randint(3, 6), replace=False):
                usages.append({
                    'team_id': team_id,
                    'document_id': dep_doc,
                    'usage_count': np.random.randint(10, 30)  # High usage
                })
    
    # Generate random usages for remaining slots
    while len(usages) < n_usages:
        team_id = np.random.choice(team_ids)
        doc_id = np.random.choice(doc_ids)
        usage_count = np.random.randint(1, 15)
        
        # Check if already exists
        exists = any(
            u['team_id'] == team_id and u['document_id'] == doc_id
            for u in usages
        )
        if not exists:
            usages.append({
                'team_id': team_id,
                'document_id': doc_id,
                'usage_count': usage_count
            })
    
    return pd.DataFrame(usages[:n_usages])


def generate_all_datasets(seed: int = None, output_dir: Path = None) -> tuple:
    """
    Generate all document-policy governance datasets.
    
    Args:
        seed: Random seed for reproducibility
        output_dir: Directory to save CSV files. If None, only returns DataFrames.
        
    Returns:
        Tuple of (topics_df, owners_df, teams_df, documents_df, references_df, usages_df)
    """
    if seed is None:
        seed = Config.RANDOM_SEED
    
    set_random_seed(seed)
    
    print(f"Generating document-policy governance network (seed={seed})...")
    
    topics = generate_topics(n_topics=15, seed=seed)
    print(f"✓ Generated {len(topics)} topics")
    
    owners = generate_owners(n_owners=10, seed=seed)
    print(f"✓ Generated {len(owners)} owners")
    
    teams = generate_teams(n_teams=8, seed=seed)
    print(f"✓ Generated {len(teams)} teams")
    
    documents = generate_documents(n_documents=100, owners_df=owners, topics_df=topics, seed=seed)
    print(f"✓ Generated {len(documents)} documents")
    
    references = generate_references(documents, n_references=300, seed=seed)
    print(f"✓ Generated {len(references)} document references")
    
    usages = generate_usages(documents, teams, n_usages=200, seed=seed)
    print(f"✓ Generated {len(usages)} team usage relationships")
    
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        topics.to_csv(output_dir / 'topics.csv', index=False)
        owners.to_csv(output_dir / 'owners.csv', index=False)
        teams.to_csv(output_dir / 'teams.csv', index=False)
        documents.to_csv(output_dir / 'documents.csv', index=False)
        references.to_csv(output_dir / 'references.csv', index=False)
        usages.to_csv(output_dir / 'usages.csv', index=False)
        
        print(f"\n✓ Saved to {output_dir}/")
        print(f"  - topics.csv ({len(topics)} rows)")
        print(f"  - owners.csv ({len(owners)} rows)")
        print(f"  - teams.csv ({len(teams)} rows)")
        print(f"  - documents.csv ({len(documents)} rows)")
        print(f"  - references.csv ({len(references)} rows)")
        print(f"  - usages.csv ({len(usages)} rows)")
        
        # Print anomaly summary
        deprecated_count = len(documents[documents['status'] == 'deprecated'])
        ownerless_count = len(documents[documents['owner_id'].isnull()])
        print(f"\n✓ Injected anomalies:")
        print(f"  - {deprecated_count} deprecated documents")
        print(f"  - {ownerless_count} ownerless documents")
        print(f"  - 1 isolated cluster (7 docs in isolation)")
        print(f"  - 1 dense duplicate clique (10 over-referenced docs)")
    
    return topics, owners, teams, documents, references, usages


if __name__ == '__main__':
    # Generate and save seed data
    from src.config import Config
    
    seed_dir = Config.PROJECT_ROOT / 'data' / 'seed' / 'document_policy'
    generate_all_datasets(seed=Config.RANDOM_SEED, output_dir=seed_dir)
