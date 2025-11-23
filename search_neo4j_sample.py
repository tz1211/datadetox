"""Sample function to search Neo4j database for model lineage information."""
import sys
from pathlib import Path

# Add model-lineage to path to import modules
model_lineage_path = Path(__file__).parent / "model-lineage"
sys.path.insert(0, str(model_lineage_path))

from typing import Dict, List, Any, Set, Optional
from graph.neo4j_client import Neo4jClient
from graph.models import ModelNode, DatasetNode, Relationship, GraphData


def search_model_lineage(model_id: str) -> GraphData:
    """
    Search Neo4j database for comprehensive lineage information about a model.
    
    Args:
        model_id: The model ID to search for (e.g., "bert-base-uncased")
        
    Returns:
        Dictionary containing:
        - child_models: List of all child models (models that are based on/fine-tuned from this model)
        - parent_ancestors: List of parent model and all ancestors up to base model
        - datasets: List of all datasets connected to the input model and its upstream ancestors
    """
    client = Neo4jClient()
    
    try:
        with client.driver.session() as session:
            # First, verify the model exists
            check_query = """
            MATCH (m:Model {model_id: $model_id})
            RETURN m.model_id as model_id
            LIMIT 1
            """
            check_result = session.run(check_query, model_id=model_id)
            if not check_result.single():
                raise ValueError(f"Model '{model_id}' not found in the database")
            
            # Get the input model itself
            input_model_query = """
            MATCH (m:Model {model_id: $model_id})
            RETURN m.model_id as model_id,
                   m.author as author,
                   m.downloads as downloads,
                   m.likes as likes,
                   m.tags as tags,
                   m.library_name as library_name,
                   m.pipeline_tag as pipeline_tag,
                   m.private as private,
                   m.url as url,
                   m.created_at as created_at,
                   m.updated_at as updated_at
            """
            input_model_result = session.run(input_model_query, model_id=model_id)
            input_model_record = input_model_result.single()
            input_model = ModelNode(
                model_id=input_model_record["model_id"],
                author=input_model_record.get("author"),
                downloads=input_model_record.get("downloads"),
                likes=input_model_record.get("likes"),
                tags=input_model_record.get("tags") or [],
                library_name=input_model_record.get("library_name"),
                pipeline_tag=input_model_record.get("pipeline_tag"),
                private=input_model_record.get("private", False),
                url=input_model_record.get("url", ""),
                created_at=input_model_record.get("created_at"),
                updated_at=input_model_record.get("updated_at")
            ) if input_model_record else None
            
            # 1. Find all child models (models that have relationships pointing TO this model)
            # These are models that are based on, fine-tuned from, or derived from this model
            child_query = """
            MATCH (child:Model)-[r]->(m:Model {model_id: $model_id})
            WHERE type(r) IN ['BASED_ON', 'FINE_TUNED', 'FINETUNED', 'ADAPTERS', 'MERGES', 'QUANTIZATIONS']
            RETURN DISTINCT child.model_id as model_id, 
                   child.author as author,
                   child.downloads as downloads,
                   child.likes as likes,
                   child.tags as tags,
                   child.library_name as library_name,
                   child.pipeline_tag as pipeline_tag,
                   child.private as private,
                   child.url as url,
                   child.created_at as created_at,
                   child.updated_at as updated_at
            ORDER BY child.model_id
            """
            child_result = session.run(child_query, model_id=model_id)
            child_models = [
                ModelNode(
                    model_id=record["model_id"],
                    author=record.get("author"),
                    downloads=record.get("downloads"),
                    likes=record.get("likes"),
                    tags=record.get("tags") or [],
                    library_name=record.get("library_name"),
                    pipeline_tag=record.get("pipeline_tag"),
                    private=record.get("private", False),
                    url=record.get("url", ""),
                    created_at=record.get("created_at"),
                    updated_at=record.get("updated_at")
                )
                for record in child_result
            ]
            
            # Get child relationships
            child_relationships_query = """
            MATCH (child:Model)-[r]->(m:Model {model_id: $model_id})
            WHERE type(r) IN ['BASED_ON', 'FINE_TUNED', 'FINETUNED', 'ADAPTERS', 'MERGES', 'QUANTIZATIONS']
            RETURN child.model_id as source,
                   m.model_id as target,
                   type(r) as relationship_type,
                   'model' as source_type,
                   'model' as target_type
            """
            child_rel_result = session.run(child_relationships_query, model_id=model_id)
            child_relationships = [
                Relationship(
                    source=record["source"],
                    target=record["target"],
                    relationship_type=record["relationship_type"].lower(),
                    source_type=record["source_type"],
                    target_type=record["target_type"]
                )
                for record in child_rel_result
            ]
            
            # 2. Find parent model and all ancestors up to base model
            # Traverse up the lineage chain until we reach a model with no parent
            parent_ancestors_query = """
            MATCH path = (m:Model {model_id: $model_id})-[r*]->(ancestor:Model)
            WHERE ALL(rel in relationships(path) 
                      WHERE type(rel) IN ['BASED_ON', 'FINE_TUNED', 'FINETUNED', 'ADAPTERS', 'MERGES', 'QUANTIZATIONS'])
            WITH ancestor, length(path) as depth
            ORDER BY depth
            RETURN DISTINCT ancestor.model_id as model_id,
                   ancestor.author as author,
                   ancestor.downloads as downloads,
                   ancestor.likes as likes,
                   ancestor.tags as tags,
                   ancestor.library_name as library_name,
                   ancestor.pipeline_tag as pipeline_tag,
                   ancestor.private as private,
                   ancestor.url as url,
                   ancestor.created_at as created_at,
                   ancestor.updated_at as updated_at,
                   depth
            """
            parent_result = session.run(parent_ancestors_query, model_id=model_id)
            parent_ancestors = [
                ModelNode(
                    model_id=record["model_id"],
                    author=record.get("author"),
                    downloads=record.get("downloads"),
                    likes=record.get("likes"),
                    tags=record.get("tags") or [],
                    library_name=record.get("library_name"),
                    pipeline_tag=record.get("pipeline_tag"),
                    private=record.get("private", False),
                    url=record.get("url", ""),
                    created_at=record.get("created_at"),
                    updated_at=record.get("updated_at")
                )
                for record in parent_result
            ]
            
            # Get parent/ancestor relationships
            parent_relationships_query = """
            MATCH path = (m:Model {model_id: $model_id})-[r*]->(ancestor:Model)
            WHERE ALL(rel in relationships(path) 
                      WHERE type(rel) IN ['BASED_ON', 'FINE_TUNED', 'FINETUNED', 'ADAPTERS', 'MERGES', 'QUANTIZATIONS'])
            UNWIND relationships(path) as rel
            WITH DISTINCT rel, startNode(rel) as start_node, endNode(rel) as end_node
            RETURN start_node.model_id as source,
                   end_node.model_id as target,
                   type(rel) as relationship_type,
                   'model' as source_type,
                   'model' as target_type
            """
            parent_rel_result = session.run(parent_relationships_query, model_id=model_id)
            parent_relationships = [
                Relationship(
                    source=record["source"],
                    target=record["target"],
                    relationship_type=record["relationship_type"].lower(),
                    source_type=record["source_type"],
                    target_type=record["target_type"]
                )
                for record in parent_rel_result
            ]
            
            # 3. Find all datasets connected to the input model and its upstream ancestors
            # Get all model IDs to search (input model + all ancestors)
            model_ids_to_search = {model_id}
            for ancestor in parent_ancestors:
                model_ids_to_search.add(ancestor.model_id)
            
            # Query for datasets connected to any of these models
            datasets_query = """
            MATCH (m:Model)-[r:TRAINED_ON]->(d:Dataset)
            WHERE m.model_id IN $model_ids
            RETURN DISTINCT d.dataset_id as dataset_id,
                   d.author as author,
                   d.downloads as downloads,
                   d.tags as tags
            ORDER BY d.dataset_id
            """
            datasets_result = session.run(datasets_query, model_ids=list(model_ids_to_search))
            datasets = [
                DatasetNode(
                    dataset_id=record["dataset_id"],
                    author=record.get("author"),
                    downloads=record.get("downloads"),
                    tags=record.get("tags") or []
                )
                for record in datasets_result
            ]
            
            # Get dataset relationships
            dataset_relationships_query = """
            MATCH (m:Model)-[r:TRAINED_ON]->(d:Dataset)
            WHERE m.model_id IN $model_ids
            RETURN m.model_id as source,
                   d.dataset_id as target,
                   'trained_on' as relationship_type,
                   'model' as source_type,
                   'dataset' as target_type
            """
            dataset_rel_result = session.run(dataset_relationships_query, model_ids=list(model_ids_to_search))
            dataset_relationships = [
                Relationship(
                    source=record["source"],
                    target=record["target"],
                    relationship_type=record["relationship_type"],
                    source_type=record["source_type"],
                    target_type=record["target_type"]
                )
                for record in dataset_rel_result
            ]
            
            # Combine all models (input model + child models + parent ancestors)
            all_models = []
            if input_model:
                all_models.append(input_model)
            all_models.extend(child_models)
            all_models.extend(parent_ancestors)
            
            # Remove duplicate models by model_id
            seen_model_ids = set()
            unique_models = []
            for model in all_models:
                if model.model_id not in seen_model_ids:
                    seen_model_ids.add(model.model_id)
                    unique_models.append(model)
            
            # Combine all relationships
            all_relationships = child_relationships + parent_relationships + dataset_relationships
            
            # Remove duplicate relationships
            seen_relationships = set()
            unique_relationships = []
            for rel in all_relationships:
                rel_key = (rel.source, rel.target, rel.relationship_type)
                if rel_key not in seen_relationships:
                    seen_relationships.add(rel_key)
                    unique_relationships.append(rel)
            
            return GraphData(
                models=unique_models,
                datasets=datasets,
                relationships=unique_relationships,
                metadata={
                    "input_model_id": model_id,
                    "num_child_models": len(child_models),
                    "num_ancestors": len(parent_ancestors),
                    "num_datasets": len(datasets),
                    "is_base_model": len(parent_ancestors) == 0
                }
            )
            
    finally:
        client.close()


def print_lineage_results(results: GraphData):
    """Pretty print the lineage search results."""
    summary = results.metadata if results.metadata else {}
    
    # Identify input model, child models, and ancestors from relationships
    input_model_id_from_meta = summary.get("input_model_id", "")
    
    # Find child models (models that have relationships pointing TO input model)
    child_model_ids = set()
    for rel in results.relationships:
        if rel.target == input_model_id_from_meta and rel.source_type == "model":
            child_model_ids.add(rel.source)
    
    # Find parent/ancestor models (input model has relationships pointing TO them)
    ancestor_model_ids = set()
    for rel in results.relationships:
        if rel.source == input_model_id_from_meta and rel.target_type == "model":
            ancestor_model_ids.add(rel.target)
    
    # Get model objects
    child_models = [m for m in results.models if m.model_id in child_model_ids]
    ancestor_models = [m for m in results.models if m.model_id in ancestor_model_ids]
    input_model = next((m for m in results.models if m.model_id == input_model_id_from_meta), None)
    
    print("=" * 80)
    print(f"Lineage Search Results for: {input_model_id_from_meta}")
    print("=" * 80)
    
    print(f"\n📊 Summary:")
    print(f"  - Is Base Model: {summary.get('is_base_model', False)}")
    print(f"  - Number of Child Models: {summary.get('num_child_models', 0)}")
    print(f"  - Number of Ancestors: {summary.get('num_ancestors', 0)}")
    print(f"  - Number of Connected Datasets: {summary.get('num_datasets', 0)}")
    print(f"  - Total Models: {len(results.models)}")
    print(f"  - Total Relationships: {len(results.relationships)}")
    
    if input_model:
        print(f"\n🎯 Input Model:")
        print(f"  - {input_model.model_id}")
        if input_model.author:
            print(f"    Author: {input_model.author}")
        if input_model.url:
            print(f"    URL: {input_model.url}")
    
    if ancestor_models:
        print(f"\n🔺 Parent & Ancestors (upstream lineage):")
        for i, ancestor in enumerate(ancestor_models, 1):
            print(f"  {i}. {ancestor.model_id}")
            if ancestor.author:
                print(f"     Author: {ancestor.author}")
            if ancestor.url:
                print(f"     URL: {ancestor.url}")
    else:
        print(f"\n🔺 Parent & Ancestors: None (this is a base model)")
    
    if child_models:
        print(f"\n🔻 Child Models (downstream lineage):")
        for i, child in enumerate(child_models, 1):
            # Find relationship type for this child
            rel_types = [rel.relationship_type for rel in results.relationships 
                        if rel.source == child.model_id and rel.target == input_model_id_from_meta]
            rel_type_str = f" (via {', '.join(rel_types)})" if rel_types else ""
            print(f"  {i}. {child.model_id}{rel_type_str}")
            if child.author:
                print(f"     Author: {child.author}")
            if child.url:
                print(f"     URL: {child.url}")
    else:
        print(f"\n🔻 Child Models: None")
    
    if results.datasets:
        print(f"\n📚 Connected Datasets:")
        for i, dataset in enumerate(results.datasets, 1):
            # Find which models this dataset is connected to
            connected_models = [rel.source for rel in results.relationships 
                              if rel.target == dataset.dataset_id and rel.relationship_type == "trained_on"]
            print(f"  {i}. {dataset.dataset_id}")
            if connected_models:
                print(f"     Connected to models: {', '.join(connected_models)}")
            if dataset.author:
                print(f"     Author: {dataset.author}")
    else:
        print(f"\n📚 Connected Datasets: None")
    
    print("=" * 80)


if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description="Search Neo4j database for model lineage information",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python search_neo4j_sample.py bert-base-uncased
  python search_neo4j_sample.py microsoft/DialoGPT-medium --json
  python search_neo4j_sample.py gpt2 --quiet
        """
    )
    
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="The model ID to search for (e.g., 'bert-base-uncased' or 'Qwen/Qwen2.5-7B')"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON instead of pretty-printed text"
    )
    
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress pretty-printed output (useful with --json)"
    )
    
    args = parser.parse_args()
    
    try:
        results = search_model_lineage(args.model)
        
        if args.json:
            import json
            # Convert GraphData to dict for JSON serialization
            output = {
                "input_model_id": results.metadata.get("input_model_id") if results.metadata else None,
                "models": [model.model_dump() for model in results.models],
                "datasets": [dataset.model_dump() for dataset in results.datasets],
                "relationships": [rel.model_dump() for rel in results.relationships],
                "metadata": results.metadata
            }
            print(json.dumps(output, indent=2))
        elif not args.quiet:
            print_lineage_results(results)
            
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error searching Neo4j: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

