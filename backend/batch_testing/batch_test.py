#!/usr/bin/env python3
"""
Batch testing CLI tool for DataDetox chatbot.

Usage:
    python batch_test.py input.csv output.csv
    python batch_test.py --sample

Input CSV format:
    query
    "Tell me about BERT"
    "What is LAION-5B?"
    "Explain GPT-2"

Output CSV will include all timing info and responses.

Folder structure:
    batch_testing/
        input/       - Place your input CSV files here
        output/      - Results will be saved here
"""

import asyncio
import csv
import sys
import time
import os
from pathlib import Path
from typing import List, Dict
import logging
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.logging import RichHandler

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the search pipeline
from routers.client import SearchRequest, run_search

# Define directory paths
BATCH_DIR = Path(__file__).parent
INPUT_DIR = BATCH_DIR / "input"
OUTPUT_DIR = BATCH_DIR / "output"

# Ensure directories exist
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger(__name__)
console = Console()


def load_queries_from_csv(input_path: str) -> List[str]:
    """
    Load queries from input CSV file.

    Expected format:
    query
    "Tell me about BERT"
    "What is LAION-5B?"

    Args:
        input_path: Path to input CSV file

    Returns:
        List of query strings
    """
    queries = []

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Validate header
            if 'query' not in reader.fieldnames:
                console.print("[red]Error: CSV must have 'query' column[/red]")
                sys.exit(1)

            for row in reader:
                query = row['query'].strip()
                if query:  # Skip empty queries
                    queries.append(query)

        console.print(f"[green]✓[/green] Loaded {len(queries)} queries from {input_path}")
        return queries

    except FileNotFoundError:
        console.print(f"[red]Error: File not found: {input_path}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error reading CSV: {str(e)}[/red]")
        sys.exit(1)


async def process_query(query: str, query_num: int, total: int) -> Dict:
    """
    Process a single query through the search pipeline.

    Args:
        query: Query string
        query_num: Current query number (1-indexed)
        total: Total number of queries

    Returns:
        Dict with query results
    """
    console.print(f"\n[cyan]Processing {query_num}/{total}:[/cyan] {query[:60]}...")

    start_time = time.time()
    request = SearchRequest(query=query)

    try:
        result = await run_search(request)
        total_time = round(time.time() - start_time, 2)

        return {
            'query': query,
            'response': result.get('response', ''),
            'search_terms': result.get('search_terms', ''),
            'arxiv_id': result.get('arxiv_id', ''),
            'stage1_time': result.get('stage1_time', ''),
            'stage2_time': result.get('stage2_time', ''),
            'stage3_time': result.get('stage3_time', ''),
            'total_time': total_time,
            'status': result.get('status', 'unknown')
        }
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        return {
            'query': query,
            'response': f"ERROR: {str(e)}",
            'search_terms': '',
            'arxiv_id': '',
            'stage1_time': '',
            'stage2_time': '',
            'stage3_time': '',
            'total_time': round(time.time() - start_time, 2),
            'status': 'error'
        }


async def process_all_queries(queries: List[str]) -> List[Dict]:
    """
    Process all queries sequentially (to avoid rate limits).

    Args:
        queries: List of query strings

    Returns:
        List of result dictionaries
    """
    results = []
    total = len(queries)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Processing queries...", total=total)

        for i, query in enumerate(queries, 1):
            result = await process_query(query, i, total)
            results.append(result)
            progress.update(task, advance=1)

            # Show result status
            status_emoji = "✓" if result['status'] == 'success' else "✗"
            status_color = "green" if result['status'] == 'success' else "red"
            console.print(f"[{status_color}]{status_emoji}[/{status_color}] {result['status']} - {result['total_time']}s total")

    return results


def save_results_to_csv(results: List[Dict], output_path: str):
    """
    Save results to output CSV file.

    Args:
        results: List of result dictionaries
        output_path: Path to output CSV file
    """
    try:
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            fieldnames = [
                'query',
                'response',
                'search_terms',
                'arxiv_id',
                'stage1_time',
                'stage2_time',
                'stage3_time',
                'total_time',
                'status'
            ]

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        console.print(f"\n[green]✓[/green] Saved {len(results)} results to {output_path}")

    except Exception as e:
        console.print(f"[red]Error saving results: {str(e)}[/red]")
        sys.exit(1)


def print_summary(results: List[Dict]):
    """
    Print a summary table of results.

    Args:
        results: List of result dictionaries
    """
    console.print("\n[bold]Results Summary:[/bold]")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Query", style="cyan", width=40)
    table.add_column("Status", width=10)
    table.add_column("arXiv", width=12)
    table.add_column("Stage 1", justify="right", width=8)
    table.add_column("Stage 2", justify="right", width=8)
    table.add_column("Stage 3", justify="right", width=8)
    table.add_column("Total", justify="right", width=8)

    total_time = 0
    success_count = 0
    arxiv_count = 0

    for result in results:
        # Truncate query for display
        query_display = result['query'][:37] + "..." if len(result['query']) > 40 else result['query']

        # Status with color
        status = result['status']
        status_color = "green" if status == "success" else "red"

        # arXiv ID
        arxiv = result['arxiv_id'] if result['arxiv_id'] else "-"
        if arxiv != "-":
            arxiv_count += 1

        # Times
        s1 = f"{result['stage1_time']}s" if result['stage1_time'] else "-"
        s2 = f"{result['stage2_time']}s" if result['stage2_time'] else "-"
        s3 = f"{result['stage3_time']}s" if result['stage3_time'] else "-"
        total = f"{result['total_time']}s"

        table.add_row(
            query_display,
            f"[{status_color}]{status}[/{status_color}]",
            arxiv,
            s1,
            s2,
            s3,
            total
        )

        total_time += result['total_time']
        if status == "success":
            success_count += 1

    console.print(table)

    # Statistics
    console.print(f"\n[bold]Statistics:[/bold]")
    console.print(f"  Total queries: {len(results)}")
    console.print(f"  Successful: [green]{success_count}[/green]")
    console.print(f"  Failed: [red]{len(results) - success_count}[/red]")
    console.print(f"  Papers analyzed: [cyan]{arxiv_count}[/cyan]")
    console.print(f"  Total time: [yellow]{round(total_time, 2)}s[/yellow]")
    console.print(f"  Average time: [yellow]{round(total_time / len(results), 2)}s[/yellow]")


def create_sample_csv():
    """
    Create a sample input CSV file with example queries in the input/ folder.
    """
    sample_queries = [
        "Tell me about BERT",
        "What is LAION-5B?",
        "Explain GPT-2",
        "What is Stable Diffusion trained on?",
        "Tell me about CLIP",
        "What is ImageNet?",
    ]

    output_path = INPUT_DIR / "sample_queries.csv"

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['query'])
        writer.writeheader()
        for query in sample_queries:
            writer.writerow({'query': query})

    console.print(f"[green]✓[/green] Created sample CSV: [cyan]{output_path}[/cyan]")
    console.print(f"\n[yellow]Run this to test:[/yellow]")
    console.print(f"  python batch_test.py sample_queries.csv")


async def main():
    """Main entry point."""
    console.print("[bold cyan]DataDetox Batch Testing Tool[/bold cyan]\n")

    # Parse arguments
    if len(sys.argv) < 2:
        console.print("[yellow]Usage:[/yellow]")
        console.print("  python batch_test.py input_file.csv [output_file.csv]")
        console.print("  python batch_test.py --sample")
        console.print("\n[yellow]Folder Structure:[/yellow]")
        console.print(f"  Input CSVs:  [cyan]{INPUT_DIR}[/cyan]")
        console.print(f"  Output CSVs: [cyan]{OUTPUT_DIR}[/cyan]")
        console.print("\n[yellow]Examples:[/yellow]")
        console.print("  python batch_test.py --sample                    # Create sample in input/")
        console.print("  python batch_test.py my_queries.csv              # Auto output to output/my_queries_results.csv")
        console.print("  python batch_test.py my_queries.csv my_out.csv   # Specify output filename")
        sys.exit(1)

    # Handle --sample flag
    if sys.argv[1] == '--sample':
        create_sample_csv()
        return

    # Parse input filename (just the name, not full path)
    input_filename = sys.argv[1]
    input_path = INPUT_DIR / input_filename

    # Generate output filename
    if len(sys.argv) > 2:
        output_filename = sys.argv[2]
    else:
        # Auto-generate output name: input.csv -> input_results.csv
        input_stem = Path(input_filename).stem
        output_filename = f"{input_stem}_results.csv"

    output_path = OUTPUT_DIR / output_filename

    # Validate input file exists
    if not input_path.exists():
        console.print(f"[red]Error: Input file not found: {input_path}[/red]")
        console.print(f"\n[yellow]Available files in input/:[/yellow]")
        input_files = list(INPUT_DIR.glob("*.csv"))
        if input_files:
            for f in input_files:
                console.print(f"  - {f.name}")
        else:
            console.print("  (none)")
        console.print("\nCreate a sample with: [cyan]python batch_test.py --sample[/cyan]")
        sys.exit(1)

    # Load queries
    queries = load_queries_from_csv(str(input_path))

    if not queries:
        console.print("[red]Error: No queries found in CSV[/red]")
        sys.exit(1)

    # Process queries
    console.print(f"\n[bold]Starting batch processing of {len(queries)} queries...[/bold]")
    results = await process_all_queries(queries)

    # Save results
    save_results_to_csv(results, str(output_path))

    # Print summary
    print_summary(results)

    console.print(f"\n[green]✓[/green] [bold]Done! Results saved to {output_path}[/bold]")


if __name__ == "__main__":
    asyncio.run(main())
