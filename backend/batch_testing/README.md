# Batch Testing Tool

Test multiple prompts through the DataDetox chatbot pipeline and save results to CSV.

## 📁 Folder Structure

```
batch_testing/
├── batch_test.py           # Main CLI tool
├── input/                  # Place your input CSV files here
│   └── sample_queries.csv  # (created with --sample)
├── output/                 # Results are saved here
│   └── *_results.csv
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Create a sample CSV

```bash
docker exec datadetox-backend-1 uv run python batch_testing/batch_test.py --sample
```

This creates `input/sample_queries.csv` with 6 example queries.

### 2. Run batch testing

```bash
# Auto-generate output filename (sample_queries.csv -> output/sample_queries_results.csv)
docker exec datadetox-backend-1 uv run python batch_testing/batch_test.py sample_queries.csv

# Or specify output filename
docker exec datadetox-backend-1 uv run python batch_testing/batch_test.py sample_queries.csv my_results.csv
```

### 3. View results

```bash
# Copy results from container
docker cp datadetox-backend-1:/app/batch_testing/output/sample_queries_results.csv ./results.csv

# Open in your editor
open results.csv
```

## 📝 Creating Your Own Test CSV

Create a file in `batch_testing/input/` with a `query` column:

**Example: `input/my_tests.csv`**

```csv
query
"Tell me about BERT"
"What is LAION-5B?"
"Explain GPT-2"
"What is Stable Diffusion trained on?"
```

Then run:

```bash
# From host machine
docker cp my_tests.csv datadetox-backend-1:/app/batch_testing/input/my_tests.csv

# Run batch test
docker exec datadetox-backend-1 uv run python batch_testing/batch_test.py my_tests.csv

# Copy results back
docker cp datadetox-backend-1:/app/batch_testing/output/my_tests_results.csv ./
```

## 📊 Output Format

Results CSV includes these columns:

| Column | Description | Example |
|--------|-------------|---------|
| `query` | Original query text | "Tell me about BERT" |
| `response` | Full markdown response | "# BERT\n\n..." |
| `search_terms` | HF search terms (Stage 1) | "bert" |
| `arxiv_id` | arXiv paper ID if found | "1810.04805" |
| `stage1_time` | Stage 1 duration (seconds) | 1.5 |
| `stage2_time` | Stage 2 duration (seconds) | 6.2 |
| `stage3_time` | Stage 3 duration (seconds) | 20.6 |
| `total_time` | Total processing time | 28.3 |
| `status` | success/error/cancelled | "success" |

## 💡 Use Cases

### Test Dataset vs Model Distinction

```csv
query
"Tell me about LAION"
"Tell me about Stable Diffusion"
"What is ImageNet?"
"What is BERT?"
```

**Expected behavior:**
- LAION, ImageNet (datasets) → No Stage 3 paper analysis
- Stable Diffusion, BERT (models) → arXiv ID + Stage 3 analysis

### Test Prompt Variations

```csv
query
"Tell me about BERT"
"What is BERT?"
"Explain BERT model"
"BERT training data"
```

Compare how different phrasings affect response quality.

### Performance Benchmarking

```csv
query
"Tell me about BERT"
"Tell me about BERT"
"Tell me about BERT"
```

Run same query multiple times to measure average response time.

## 🎨 Example Output

```
DataDetox Batch Testing Tool

✓ Loaded 6 queries from batch_testing/input/sample_queries.csv

Starting batch processing of 6 queries...

Processing 1/6: Tell me about BERT...
✓ success - 28.3s total

Processing 2/6: What is LAION-5B?...
✓ success - 8.1s total

...

Results Summary:
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┓
┃ Query                ┃ Status ┃ arXiv      ┃ Stage1┃ Stage2┃ Stage3┃  Total┃
┣━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━╋━━━━━━━━━━━━╋━━━━━━━╋━━━━━━━╋━━━━━━━╋━━━━━━━┫
┃ Tell me about BERT   ┃ success┃ 1810.04805 ┃  1.5s ┃  6.2s ┃ 20.6s ┃ 28.3s ┃
┃ What is LAION-5B?    ┃ success┃ -          ┃  1.2s ┃  6.9s ┃     - ┃  8.1s ┃
┗━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━┻━━━━━━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┻━━━━━━━┛

Statistics:
  Total queries: 6
  Successful: 6
  Failed: 0
  Papers analyzed: 4
  Total time: 132.3s
  Average time: 22.05s

✓ Done! Results saved to batch_testing/output/sample_queries_results.csv
```

## 🔧 Advanced Usage

### List Available Input Files

```bash
docker exec datadetox-backend-1 ls -la batch_testing/input/
```

### View Output Files

```bash
docker exec datadetox-backend-1 ls -la batch_testing/output/
```

### Clean Up Output Files

```bash
docker exec datadetox-backend-1 rm batch_testing/output/*.csv
```

### Run from Inside Container

```bash
# Enter container
docker exec -it datadetox-backend-1 bash

# Navigate to batch_testing directory
cd batch_testing

# Create sample
uv run python batch_test.py --sample

# Run test
uv run python batch_test.py sample_queries.csv

# Exit
exit
```

## 🐛 Troubleshooting

**Error: Input file not found**

Make sure your CSV is in the `batch_testing/input/` folder:

```bash
docker cp my_queries.csv datadetox-backend-1:/app/batch_testing/input/
```

**Error: ModuleNotFoundError**

Make sure you're using `uv run python` not just `python`:

```bash
# Correct
docker exec datadetox-backend-1 uv run python batch_testing/batch_test.py --sample

# Wrong
docker exec datadetox-backend-1 python batch_testing/batch_test.py --sample
```

**Container not running**

```bash
docker-compose up -d backend
```

## 📖 Technical Details

The tool:
- Runs queries **sequentially** to avoid OpenAI API rate limits
- Processes each query through the full 3-stage pipeline
- Automatically creates `input/` and `output/` directories
- Auto-generates output filenames (e.g., `test.csv` → `test_results.csv`)
- Properly escapes CSV content (handles multi-line responses)
- Shows real-time progress with Rich library

## 🔑 Requirements

- Docker container running with backend
- OpenAI API key in `.env`
- Rich library installed (included in dependencies)
