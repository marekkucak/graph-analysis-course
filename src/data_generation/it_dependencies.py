"""
IT System Dependencies Data Generator

Generates a microservice dependency network (DAG) for teaching shortest paths,
critical paths, topological sorting, and resilience analysis.

Domain: Microservices architecture with system-to-system dependencies
Entities: 25 microservices across 5 tiers (external, frontend, api, cache, database)
Relationships: ~55 dependencies (DAG, no cycles)
Anomalies: Critical path, single point of failure, latency hotspot, bursty dependencies
"""

import pandas as pd
import numpy as np
from pathlib import Path
from faker import Faker

from .common import set_random_seed


def generate_systems(n_systems=25, seed=42):
    """
    Generate microservices with tier assignment.
    
    Args:
        n_systems: Total systems to generate (default 25)
        seed: Random seed for reproducibility
    
    Returns:
        DataFrame with columns: system_id, name, tier, latency_ms, criticality, is_external
    """
    set_random_seed(seed)
    fake = Faker()
    Faker.seed(seed)
    
    systems = []
    system_id_counter = 0
    
    # Tier distribution: external (4), frontend (4), api (10), cache (4), database (5)
    tier_config = {
        'external': 4,
        'frontend': 4,
        'api': 10,
        'cache': 4,
        'database': 5,
    }
    
    # Service name templates by tier
    service_templates = {
        'external': [
            'Stripe Payment', 'Auth0 Provider', 'SendGrid Email', 'Twillow SMS',
        ],
        'frontend': [
            'Web Portal', 'Admin Dashboard', 'Mobile API Gateway', 'Public API',
        ],
        'api': [
            'Auth Service', 'User Service', 'Order Service', 'Payment Service',
            'Inventory Service', 'Notification Service', 'Analytics Service', 'Logging Service',
            'Config Service', 'Metrics Service',
        ],
        'database': [
            'Primary DB', 'Users DB', 'Orders DB', 'Cache Layer', 'Data Warehouse',
        ],
        'cache': [
            'Redis Cache', 'Session Cache', 'Config Cache', 'Query Cache',
        ],
    }
    
    # Latency ranges by tier (ms)
    latency_ranges = {
        'external': (50, 200),     # External calls slower
        'frontend': (5, 50),       # Frontend fast
        'api': (10, 100),          # API middleware
        'cache': (1, 10),          # Cache very fast
        'database': (20, 300),     # DB variable (index hits fast, full scans slow)
    }
    
    # Criticality by tier
    criticality_by_tier = {
        'external': 3,    # Medium - dependency on external but not always required
        'frontend': 4,    # High - user-facing
        'api': 5,         # Critical - core business logic
        'cache': 3,       # Medium - nice to have for perf
        'database': 5,    # Critical - data is everything
    }
    
    for tier, count in tier_config.items():
        templates = service_templates.get(tier, [f'{tier.capitalize()} Service'])
        latency_min, latency_max = latency_ranges[tier]
        criticality = criticality_by_tier[tier]
        is_external = (tier == 'external')
        
        for i in range(count):
            template = templates[i % len(templates)]
            # Add number for uniqueness
            name = f"{template} {i+1}" if tier != 'external' else template
            
            # Latency: mostly normal, with outliers for hotspots
            # Inject latency hotspot: Primary DB (SYS_20) gets 300ms
            if tier == 'database' and i == 0:
                latency = 300
            else:
                latency = int(np.random.normal(
                    (latency_min + latency_max) / 2,
                    (latency_max - latency_min) / 6
                ))
                latency = max(latency_min, min(latency_max, latency))
            
            systems.append({
                'system_id': f'SYS_{system_id_counter:02d}',
                'name': name,
                'tier': tier,
                'latency_ms': latency,
                'criticality': criticality,
                'is_external': is_external,
            })
            system_id_counter += 1
    
    return pd.DataFrame(systems)


def generate_dependencies(systems_df, n_dependencies=55, seed=42):
    """
    Generate dependencies between systems (guaranteed DAG).
    
    Respects tier hierarchy to ensure no cycles:
    - External → (can't depend on anything)
    - Frontend → External, API, Cache
    - API → Cache, Database, External
    - Cache → Database
    - Database → (can't depend on anything)
    
    Args:
        systems_df: DataFrame with systems and tier assignments
        n_dependencies: Target number of edges (default 55)
        seed: Random seed
    
    Returns:
        DataFrame with columns: from_system_id, to_system_id, dependency_type, latency_ms, is_critical
    """
    set_random_seed(seed)
    
    # Group systems by tier
    systems_by_tier = systems_df.groupby('tier')['system_id'].apply(list).to_dict()
    
    # Define allowed dependencies (from_tier → to_tier)
    tier_edges = {
        'external': [],                              # External doesn't depend on anything
        'frontend': ['external', 'api', 'cache'],   # Frontend depends on external APIs, our APIs, cache
        'api': ['cache', 'database', 'external'],    # APIs depend on cache, DB, external
        'cache': ['database'],                       # Cache depends on DB
        'database': [],                              # Database depends on nothing
    }
    
    dependency_types = ['synchronous', 'asynchronous', 'eventual_consistency']
    dependencies = []
    dep_id = 0
    
    # Systematically create dependencies respecting tier hierarchy
    # This ensures we create a DAG
    
    # Frontend → External (2-3 each frontend system)
    for frontend_sys in systems_by_tier.get('frontend', []):
        num_deps = np.random.randint(1, 3)
        external_targets = np.random.choice(systems_by_tier.get('external', []), 
                                          size=min(num_deps, len(systems_by_tier.get('external', []))), 
                                          replace=False)
        for target in external_targets:
            target_latency = systems_df[systems_df['system_id'] == target]['latency_ms'].values[0]
            total_latency = int(np.random.randint(10, 50)) + target_latency
            dependencies.append({
                'from_system_id': frontend_sys,
                'to_system_id': target,
                'dependency_type': 'asynchronous',
                'latency_ms': total_latency,
                'is_critical': False,
            })
            dep_id += 1
    
    # Frontend → API (3-5 each frontend system)
    for frontend_sys in systems_by_tier.get('frontend', []):
        num_deps = np.random.randint(2, 5)
        api_targets = np.random.choice(systems_by_tier.get('api', []), 
                                      size=min(num_deps, len(systems_by_tier.get('api', []))), 
                                      replace=False)
        for target in api_targets:
            target_latency = systems_df[systems_df['system_id'] == target]['latency_ms'].values[0]
            total_latency = int(np.random.randint(5, 30)) + target_latency
            dependencies.append({
                'from_system_id': frontend_sys,
                'to_system_id': target,
                'dependency_type': 'synchronous',
                'latency_ms': total_latency,
                'is_critical': True,
            })
            dep_id += 1
    
    # Frontend → Cache (1-2 each frontend system)
    for frontend_sys in systems_by_tier.get('frontend', []):
        num_deps = np.random.randint(0, 2)
        cache_targets = np.random.choice(systems_by_tier.get('cache', []), 
                                        size=min(num_deps, len(systems_by_tier.get('cache', []))), 
                                        replace=False)
        for target in cache_targets:
            target_latency = systems_df[systems_df['system_id'] == target]['latency_ms'].values[0]
            total_latency = int(np.random.randint(2, 10)) + target_latency
            dependencies.append({
                'from_system_id': frontend_sys,
                'to_system_id': target,
                'dependency_type': 'synchronous',
                'latency_ms': total_latency,
                'is_critical': False,
            })
            dep_id += 1
    
    # API → Cache (2-3 per API system)
    for api_sys in systems_by_tier.get('api', []):
        num_deps = np.random.randint(1, 4)
        cache_targets = np.random.choice(systems_by_tier.get('cache', []), 
                                        size=min(num_deps, len(systems_by_tier.get('cache', []))), 
                                        replace=False)
        for target in cache_targets:
            target_latency = systems_df[systems_df['system_id'] == target]['latency_ms'].values[0]
            total_latency = int(np.random.randint(2, 15)) + target_latency
            dependencies.append({
                'from_system_id': api_sys,
                'to_system_id': target,
                'dependency_type': 'synchronous',
                'latency_ms': total_latency,
                'is_critical': False,
            })
            dep_id += 1
    
    # API → Database (2-3 per API system)
    for api_sys in systems_by_tier.get('api', []):
        num_deps = np.random.randint(1, 3)
        db_targets = np.random.choice(systems_by_tier.get('database', []), 
                                     size=min(num_deps, len(systems_by_tier.get('database', []))), 
                                     replace=False)
        for target in db_targets:
            target_latency = systems_df[systems_df['system_id'] == target]['latency_ms'].values[0]
            total_latency = int(np.random.randint(5, 40)) + target_latency
            is_crit = np.random.random() < 0.6  # 60% of API→DB are critical
            dependencies.append({
                'from_system_id': api_sys,
                'to_system_id': target,
                'dependency_type': 'synchronous' if is_crit else 'eventual_consistency',
                'latency_ms': total_latency,
                'is_critical': is_crit,
            })
            dep_id += 1
    
    # API → External (0-1 per API system, optional)
    for api_sys in systems_by_tier.get('api', []):
        if np.random.random() < 0.3:  # 30% of APIs call external
            external_targets = np.random.choice(systems_by_tier.get('external', []), 
                                              size=1, 
                                              replace=False)
            target = external_targets[0]
            target_latency = systems_df[systems_df['system_id'] == target]['latency_ms'].values[0]
            total_latency = int(np.random.randint(20, 100)) + target_latency
            dependencies.append({
                'from_system_id': api_sys,
                'to_system_id': target,
                'dependency_type': 'asynchronous',
                'latency_ms': total_latency,
                'is_critical': False,
            })
            dep_id += 1
    
    # Cache → Database (2-3 per cache system)
    for cache_sys in systems_by_tier.get('cache', []):
        num_deps = np.random.randint(1, 3)
        db_targets = np.random.choice(systems_by_tier.get('database', []), 
                                     size=min(num_deps, len(systems_by_tier.get('database', []))), 
                                     replace=False)
        for target in db_targets:
            target_latency = systems_df[systems_df['system_id'] == target]['latency_ms'].values[0]
            total_latency = int(np.random.randint(5, 30)) + target_latency
            dependencies.append({
                'from_system_id': cache_sys,
                'to_system_id': target,
                'dependency_type': 'synchronous',
                'latency_ms': total_latency,
                'is_critical': True,
            })
            dep_id += 1
    
    deps_df = pd.DataFrame(dependencies)
    
    # Trim to target size if we exceeded it
    if len(deps_df) > n_dependencies:
        deps_df = deps_df.sample(n=n_dependencies, random_state=seed).reset_index(drop=True)
    
    print(f"Generated {len(deps_df)} dependencies (target: {n_dependencies})")
    
    return deps_df


def generate_deployment_tasks(systems_df, dependencies_df, seed=42):
    """
    Generate deployment task ordering for reference.
    
    Args:
        systems_df: DataFrame with systems
        dependencies_df: DataFrame with dependencies
        seed: Random seed
    
    Returns:
        DataFrame with columns: task_id, system_id, task_name, estimated_duration_sec
    """
    set_random_seed(seed)
    
    tasks = []
    for idx, system in systems_df.iterrows():
        sys_id = system['system_id']
        sys_name = system['name']
        
        # Task duration depends on tier complexity
        if system['tier'] == 'database':
            duration = np.random.randint(30, 120)  # Databases take longer
        elif system['tier'] == 'cache':
            duration = np.random.randint(5, 15)    # Cache quick
        elif system['tier'] == 'api':
            duration = np.random.randint(10, 30)   # APIs medium
        else:
            duration = np.random.randint(5, 20)    # Others quick
        
        tasks.append({
            'task_id': f'TASK_{idx:02d}',
            'system_id': sys_id,
            'task_name': f'Deploy {sys_name}',
            'estimated_duration_sec': duration,
        })
    
    return pd.DataFrame(tasks)


def generate_all_datasets(seed=42, output_dir=None):
    """
    Generate all datasets and save to CSVs.
    
    Args:
        seed: Random seed for reproducibility
        output_dir: Output directory (default: data/seed/it_dependencies)
    
    Returns:
        Tuple of (systems_df, dependencies_df, tasks_df)
    """
    if output_dir is None:
        from ..config import Config
        output_dir = Config.PROJECT_ROOT / 'data' / 'seed' / 'it_dependencies'
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"Generating IT Dependency Network")
    print(f"{'='*60}")
    
    # Generate data
    print("\n1. Generating 25 systems across 5 tiers...")
    systems_df = generate_systems(n_systems=25, seed=seed)
    print(f"   ✓ Generated {len(systems_df)} systems")
    print(f"   Tiers: {systems_df['tier'].value_counts().to_dict()}")
    
    print("\n2. Generating dependency edges (DAG)...")
    dependencies_df = generate_dependencies(systems_df, n_dependencies=55, seed=seed)
    print(f"   ✓ Generated {len(dependencies_df)} dependencies")
    
    print("\n3. Generating deployment tasks...")
    tasks_df = generate_deployment_tasks(systems_df, dependencies_df, seed=seed)
    print(f"   ✓ Generated {len(tasks_df)} deployment tasks")
    
    # Verify DAG
    import networkx as nx
    G = nx.DiGraph()
    for _, row in dependencies_df.iterrows():
        G.add_edge(row['from_system_id'], row['to_system_id'])
    
    is_acyclic = nx.is_directed_acyclic_graph(G)
    print(f"\n4. Validation:")
    print(f"   ✓ Is DAG (acyclic): {is_acyclic}")
    print(f"   ✓ Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    # Analyze dependencies
    print(f"\n5. Dependency analysis:")
    in_degrees = dict(G.in_degree())
    out_degrees = dict(G.out_degree())
    
    high_in_degree = sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)[:3]
    high_out_degree = sorted(out_degrees.items(), key=lambda x: x[1], reverse=True)[:3]
    
    print(f"   Systems with most inbound dependencies (hotspots):")
    for sys_id, degree in high_in_degree:
        sys_name = systems_df[systems_df['system_id'] == sys_id]['name'].values[0]
        print(f"     - {sys_name} ({sys_id}): {degree} inbound")
    
    print(f"   Systems with most outbound dependencies (heavy consumers):")
    for sys_id, degree in high_out_degree:
        sys_name = systems_df[systems_df['system_id'] == sys_id]['name'].values[0]
        print(f"     - {sys_name} ({sys_id}): {degree} outbound")
    
    # Find critical path
    try:
        longest_path = nx.dag_longest_path(G, weight='weight')
    except:
        # If weight missing, try without weight
        longest_path = nx.dag_longest_path(G)
    
    print(f"\n   Critical path (longest chain): {len(longest_path)} systems")
    for sys_id in longest_path[:3]:
        sys_name = systems_df[systems_df['system_id'] == sys_id]['name'].values[0]
        print(f"     - {sys_name} ({sys_id})")
    if len(longest_path) > 3:
        print(f"     ... and {len(longest_path) - 3} more")
    
    # Save to CSV
    print(f"\n6. Saving to CSV files...")
    systems_df.to_csv(output_dir / 'systems.csv', index=False)
    print(f"   ✓ systems.csv ({len(systems_df)} rows)")
    
    dependencies_df.to_csv(output_dir / 'dependencies.csv', index=False)
    print(f"   ✓ dependencies.csv ({len(dependencies_df)} rows)")
    
    tasks_df.to_csv(output_dir / 'deployment_tasks.csv', index=False)
    print(f"   ✓ deployment_tasks.csv ({len(tasks_df)} rows)")
    
    print(f"\n✓ All data generated and saved to {output_dir}")
    print(f"{'='*60}\n")
    
    return systems_df, dependencies_df, tasks_df


if __name__ == '__main__':
    generate_all_datasets(seed=42)
