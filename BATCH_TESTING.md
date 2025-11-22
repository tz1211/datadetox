# Batch Testing - Quick Start

Test multiple prompts simultaneously through your chatbot and save results to CSV.

## 📁 Organized Structure

```
backend/batch_testing/
├── batch_test.py       # Main CLI tool
├── input/              # Your input CSV files go here
│   └── *.csv
├── output/             # Results are saved here
│   └── *_results.csv
└── README.md          # Full documentation
```

## 🚀 Quick Start (3 Commands)

### 1. Create sample queries

```bash
./batch_test.sh --sample
```

### 2. Run batch test

```bash
./batch_test.sh sample_queries.csv
```

### 3. Download results

```bash
./batch_test.sh --get sample_queries_results.csv
```

That's it! You now have `sample_queries_results.csv` with full responses.

## 📝 Test Your Own Queries

Create `my_queries.csv` on your machine:

```csv
query
"Tell me about BERT"
"What is LAION-5B?"
"Explain GPT-2"
```

Then:

```bash
# Upload to container
./batch_test.sh --put my_queries.csv

# Run batch test (auto-generates output filename)
./batch_test.sh my_queries.csv

# Download results
./batch_test.sh --get my_queries_results.csv
```

## 🔧 All Commands

| Command | What it does |
|---------|-------------|
| `./batch_test.sh --sample` | Create sample CSV in container |
| `./batch_test.sh --list` | List all input/output files |
| `./batch_test.sh --put my_file.csv` | Upload your CSV to container |
| `./batch_test.sh my_file.csv` | Run batch test (auto output name) |
| `./batch_test.sh input.csv output.csv` | Run with custom output name |
| `./batch_test.sh --get results.csv` | Download results from container |

## 📊 What You Get

Output CSV includes:

- Full markdown response for each query
- Search terms used
- arXiv paper ID (if found)
- Stage timing breakdown (Stage 1, 2, 3)
- Total processing time
- Success/error status

## 💡 Common Use Cases

**Test prompt variations:**
```csv
query
"Tell me about BERT"
"What is BERT?"
"Explain BERT model"
```

**Verify dataset vs model handling:**
```csv
query
"What is LAION?"
"What is Stable Diffusion?"
```

LAION (dataset) won't trigger paper analysis, Stable Diffusion (model) will.

**Performance testing:**

Upload same query 10 times, measure average response time.

## 📖 Full Documentation

See [backend/batch_testing/README.md](backend/batch_testing/README.md) for:
- Complete examples
- Troubleshooting
- Advanced usage
- Technical details

## ⚡ Example Output

```
DataDetox Batch Testing Tool

✓ Loaded 6 queries from batch_testing/input/sample_queries.csv

Processing 1/6: Tell me about BERT...
✓ success - 28.3s total

Processing 2/6: What is LAION-5B?...
✓ success - 8.1s total

...

Results Summary:
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━┓
┃ Query                ┃ Status ┃ arXiv      ┃  Total┃
┣━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━╋━━━━━━━━━━━━╋━━━━━━━┫
┃ Tell me about BERT   ┃ success┃ 1810.04805 ┃ 28.3s ┃
┃ What is LAION-5B?    ┃ success┃ -          ┃  8.1s ┃
┗━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━┻━━━━━━━━━━━━┻━━━━━━━┛

Statistics:
  Successful: 6/6
  Papers analyzed: 4
  Average time: 22.05s

✓ Done!
```

## 🐛 Need Help?

```bash
# Show all available commands
./batch_test.sh

# List files in container
./batch_test.sh --list

# Check if backend is running
docker ps | grep backend
```
