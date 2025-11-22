# Batch Testing - File Structure

This document explains the organized structure of the batch testing tool.

## Directory Layout

```
datadetox/
├── batch_test.sh                      # Wrapper script (run from project root)
├── BATCH_TESTING.md                   # Quick start guide
│
└── backend/
    └── batch_testing/                 # Batch testing module
        ├── batch_test.py              # Main CLI tool
        ├── README.md                  # Full documentation
        ├── STRUCTURE.md               # This file
        ├── .gitignore                 # Ignore CSV files
        │
        ├── input/                     # Input CSV files
        │   ├── .gitkeep              # Keep folder in git
        │   └── *.csv                 # Your query CSV files (ignored by git)
        │
        └── output/                    # Output result files
            ├── .gitkeep              # Keep folder in git
            └── *.csv                 # Result CSV files (ignored by git)
```

## File Purposes

### Root Level

**`batch_test.sh`**
- Wrapper script for easy usage from host machine
- Handles file uploads/downloads from container
- Commands: `--sample`, `--list`, `--put`, `--get`

**`BATCH_TESTING.md`**
- Quick start guide
- Common use cases
- Example workflows

### Backend/Batch Testing Module

**`batch_test.py`**
- Main Python CLI tool
- Runs inside Docker container
- Processes queries through 3-stage pipeline
- Auto-organizes files into input/output folders

**`README.md`**
- Complete documentation
- Advanced usage examples
- Troubleshooting guide
- Technical details

**`STRUCTURE.md`** (this file)
- Explains file organization
- Describes purpose of each file/folder

**`.gitignore`**
- Ignores CSV files (they're user-generated)
- Keeps folder structure (via .gitkeep files)

### Input Folder

- Place your test query CSV files here
- Format: Single `query` column with one query per row
- Files are automatically read from this folder
- Example: `sample_queries.csv`, `my_tests.csv`

### Output Folder

- Results are automatically saved here
- Naming convention: `{input_name}_results.csv`
- Contains full responses + metadata + timing info
- Example: `sample_queries_results.csv`

## Workflow

### From Host Machine (Recommended)

```bash
# 1. Create sample
./batch_test.sh --sample

# 2. Or upload your own CSV
./batch_test.sh --put my_queries.csv

# 3. Run batch test
./batch_test.sh my_queries.csv

# 4. Download results
./batch_test.sh --get my_queries_results.csv
```

### From Inside Container

```bash
# 1. Enter container
docker exec -it datadetox-backend-1 bash

# 2. Navigate to batch_testing
cd batch_testing

# 3. Create sample
uv run python batch_test.py --sample

# 4. Run test
uv run python batch_test.py sample_queries.csv

# 5. Results are in output/sample_queries_results.csv
cat output/sample_queries_results.csv
```

## File Naming Conventions

### Input Files

- Should end with `.csv`
- Can have any name (e.g., `my_tests.csv`, `bert_variants.csv`)
- Must have `query` column header

### Output Files

**Auto-generated names:**
- Format: `{input_stem}_results.csv`
- Examples:
  - `test.csv` → `test_results.csv`
  - `my_queries.csv` → `my_queries_results.csv`

**Custom names:**
- Specify as second argument: `batch_test.py input.csv custom_output.csv`

## Git Configuration

The `.gitignore` file ensures:

✅ **Tracked by git:**
- `batch_test.py` (code)
- `README.md` (docs)
- `input/` folder (via .gitkeep)
- `output/` folder (via .gitkeep)

❌ **Not tracked by git:**
- `input/*.csv` (user-generated query files)
- `output/*.csv` (user-generated result files)

This keeps the repo clean while preserving the folder structure.

## Benefits of This Structure

### Organized
- Clear separation of input/output
- No clutter in root directory
- Easy to find files

### Safe
- CSV files not committed to git
- Prevents accidentally committing sensitive queries/responses
- Preserves folder structure

### Convenient
- Auto-generates output filenames
- Lists available files with `--list`
- Easy file uploads/downloads with wrapper script

### Scalable
- Can have many input files for different test suites
- Output files clearly linked to input files
- Easy to clean up old results

## Examples

### Test Suite Organization

```
batch_testing/input/
├── dataset_tests.csv       # Tests for datasets (LAION, ImageNet, etc.)
├── model_tests.csv         # Tests for models (BERT, GPT-2, etc.)
├── edge_cases.csv          # Edge case handling
└── performance_bench.csv   # Same query repeated for benchmarking

batch_testing/output/
├── dataset_tests_results.csv
├── model_tests_results.csv
├── edge_cases_results.csv
└── performance_bench_results.csv
```

### Version Control

Different test suites can be maintained:

```
input/
├── v1_baseline.csv          # Original test suite
├── v2_improved_prompts.csv  # After prompt improvements
└── v3_edge_cases.csv        # Added edge cases
```

Compare outputs to measure improvements over time.

## Maintenance

### Clean Up Old Results

```bash
# From host
./batch_test.sh --list  # See what's there

# Enter container and remove old files
docker exec datadetox-backend-1 rm batch_testing/output/*.csv
```

### Backup Important Results

```bash
# Download result before it gets overwritten
./batch_test.sh --get important_results.csv

# Keep it safe
mv important_results.csv backups/important_results_2024-11-22.csv
```

### Share Test Cases

Since input CSVs aren't tracked by git, share them manually:

```bash
# Export a test suite to share with team
docker cp datadetox-backend-1:/app/batch_testing/input/my_tests.csv ./shared_tests/
```

## Summary

The batch testing tool is organized to:
- Keep files separated (input vs output)
- Prevent git clutter (CSV files ignored)
- Make it easy to upload/download files
- Auto-organize outputs with clear naming
- Support multiple test suites

All managed through simple wrapper commands! 🎉
