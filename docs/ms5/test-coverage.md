# Test Coverage Documentation

This document provides a comprehensive overview of test coverage across all services in the DataDetox application, identifying which functions and modules are not covered by tests.

## Overall Coverage Summary

| Service | Coverage | Status |
|---------|----------|--------|
| **Backend** | 83% | ✅ Above 60% threshold |
| **Model-Lineage** | 77% | ✅ Above 60% threshold |
| **Frontend** | ~76% | ✅ Above 60% threshold |

## Backend Service Coverage

**Overall Coverage: 83%** (290 statements, 48 missing)

### Fully Covered Modules (100%)

- `main.py` - FastAPI application entry point
- `routers/client.py` - Main API router and search endpoint
- `routers/search/__init__.py` - Search router initialization
- `routers/search/agent.py` - Agent configuration
- `routers/search/utils/__init__.py` - Utils package initialization
- `routers/search/utils/tool_state.py` - Request context and tool state management

### Partially Covered Modules

#### `routers/search/utils/huggingface.py` - 91% Coverage

**Missing Lines: 133-140, 158-159, 303**

**Uncovered Functions/Code Blocks:**

1. **Model Card Loading Exception Handling** (lines 133-140)
   - Exception handling when `ModelCard.load()` fails
   - Warning log when model card cannot be loaded
   - Fallback to `None` for card_text

2. **Success Logging** (lines 158-159)
   - Info log message after successfully fetching model card
   - This is a logging statement that's not critical but could be tested

3. **Error Handling** (line 303)
   - Exception handling in dataset card retrieval
   - Likely an error path that's difficult to trigger in tests

#### `routers/search/utils/search_neo4j.py` - 60% Coverage ⚠️

**Missing Lines: 98-110, 116-128, 143-221**

**Uncovered Functions/Code Blocks:**

1. **`search_models()` Function** (lines 98-110)
   - Neo4j query execution for all models
   - Node parsing and filtering
   - Query summary logging
   - **Reason:** This function is a `@function_tool` that's called by the agent, not directly tested

2. **`search_datasets()` Function** (lines 116-128)
   - Neo4j query execution for all datasets
   - Dataset node parsing
   - Query summary logging
   - **Reason:** Similar to `search_models()`, called by agent

3. **`search_query()` Function** (lines 143-221)
   - Complex Cypher query execution with APOC procedures
   - Graph traversal and subgraph extraction
   - Node and relationship parsing
   - Error handling for query execution
   - **Reason:** This is the most complex function and requires Neo4j integration tests with APOC enabled


## Model-Lineage Service Coverage

**Overall Coverage: 77%** (650 statements, 152 missing)

### Fully Covered Modules (100%)

- `graph/__init__.py` - Graph package initialization
- `graph/builder.py` - Lineage graph building logic
- `graph/models.py` - Pydantic models for graph data
- `scrapers/__init__.py` - Scrapers package initialization
- `storage/__init__.py` - Storage package initialization

### Partially Covered Modules

#### `graph/neo4j_client.py` - 96% Coverage

**Missing Lines: 29-31**

**Uncovered Code:**
- Exception handling in `_connect()` method when Neo4j connection fails
- Error logging when connection verification fails
- **Reason:** Difficult to test connection failures without actually breaking the connection

#### `lineage_scraper.py` - 54% Coverage ⚠️

**Missing Lines: 54-58, 80-83, 100, 103-104, 145-151, 155-245, 249**

**Uncovered Functions/Code Blocks:**

1. **File Cleanup Logic** (lines 54-58, 80-83)
   - Cleanup of old files when `keep_latest` is specified
   - File deletion logic
   - **Reason:** Requires file system setup and cleanup in tests

2. **Metadata Saving** (line 100)
   - Metadata file saving in `scrape_models()`
   - **Reason:** Part of the scraping pipeline that's tested at integration level

3. **Error Handling** (lines 103-104)
   - Exception handling in graph building
   - **Reason:** Error paths are difficult to trigger

4. **`commit_data()` Function** (lines 145-151)
   - DVC and Git commit operations
   - Version control integration
   - **Reason:** Requires Git/DVC setup and is tested in integration tests

5. **`main()` Function** (lines 155-245, 249)
   - Command-line argument parsing
   - Pipeline orchestration
   - Error handling and logging
   - **Reason:** This is the CLI entry point, typically tested via integration tests or manual testing

#### `scrapers/huggingface_scraper.py` - 71% Coverage

**Missing Lines: 38-101, 167-168, 256-257, 263-265, 326, 349-368, 391, 396, 398-399, 422**

**Uncovered Functions/Code Blocks:**

1. **`scrape_all_models()` Main Loop** (lines 38-101)
   - Model listing from HuggingFace API
   - Progress bar iteration
   - Model processing loop
   - Exception handling for individual models
   - Dataset relationship extraction
   - Rate limiting delays
   - **Reason:** This is the main scraping loop that requires extensive mocking of HuggingFace API

2. **Error Handling Paths** (lines 167-168, 256-257, 263-265, 326, 349-368, 391, 396, 398-399, 422)
   - Various exception handling blocks throughout the scraper
   - API error handling
   - Parsing error handling
   - **Reason:** Error paths are difficult to trigger and require specific failure conditions

#### `storage/data_store.py` - 81% Coverage

**Missing Lines: 38, 45-47, 83-85, 198, 230, 268, 272, 275-276, 282-304, 309, 344-345, 367-368, 380-381, 409-412, 419**

**Uncovered Functions/Code Blocks:**

1. **Project Root Detection Edge Cases** (lines 38, 45-47, 83-85)
   - Edge cases in `_find_project_root()`
   - Docker workspace path detection
   - **Reason:** Requires specific directory structures

2. **DVC Operations Error Handling** (lines 268, 272, 275-276, 282-304)
   - `_dvc_add()` error handling
   - File path resolution errors
   - Subprocess execution errors
   - **Reason:** Error paths in DVC operations are difficult to trigger

3. **Git Operations** (lines 309, 344-345, 367-368, 380-381, 409-412, 419)
   - Git commit operations
   - Git initialization
   - Error handling in Git operations
   - **Reason:** Requires Git repository setup and is tested in integration tests


## Frontend Service Coverage

**Overall Coverage: ~76%**

### Fully Covered Modules

- `src/lib/utils.ts` - Utility functions (100%)

### Partially Covered Modules

#### `src/pages/Chatbot.tsx` - 91% Coverage

**Missing Lines: 80-181, 186-189**

**Uncovered Code:**
- Some edge cases in message handling
- Error handling paths
- Loading states
- **Reason:** Most functionality is covered, but some edge cases and error paths remain untested

#### `src/components/ModelTree.tsx` - Not fully covered

**Uncovered Code:**
- Complex D3 tree rendering logic
- Node interaction handlers
- Graph visualization updates
- **Reason:** D3 tree component is complex to test and is mocked in unit tests

#### `src/components/ChatMessage.tsx` - Well covered

- Most functionality is tested
- Some markdown rendering edge cases may be untested

### Excluded from Coverage

The following files are intentionally excluded from coverage reporting (as configured in `vitest.config.ts`):

- `src/main.tsx` - Application entry point
- `src/vite-env.d.ts` - Type definitions
- `src/components/ui/**` - Third-party UI components (shadcn/ui)
- `src/hooks/use-toast.ts` - UI-related toast hook
- `src/pages/NotFound.tsx` - Simple 404 page
- `src/pages/Index.tsx` - Landing page

## Coverage Gaps Summary

### Critical Gaps (Should be addressed)

1. **Backend: `search_neo4j.py` (60% coverage)**
   - `search_models()`, `search_datasets()`, and `search_query()` functions need direct testing
   - These are core functionality that should have better test coverage

2. **Model-Lineage: `lineage_scraper.py` (54% coverage)**
   - CLI argument parsing and main orchestration logic
   - File cleanup operations
   - Commit operations

### Moderate Gaps (Nice to have)

1. **Backend: `huggingface.py` (91% coverage)**
   - Error handling paths for model card loading
   - Dataset card error handling

2. **Model-Lineage: `huggingface_scraper.py` (71% coverage)**
   - Main scraping loop with various error conditions
   - Rate limiting behavior

3. **Model-Lineage: `data_store.py` (81% coverage)**
   - Edge cases in project root detection
   - DVC error handling paths

### Low Priority Gaps

1. **Frontend: UI components**
   - Complex visualization components (ModelTree)
   - Some edge cases in error handling

2. **Logging statements**
   - Many uncovered lines are just logging statements
   - Not critical for functionality testing

## Running Coverage Reports

### Backend
```bash
cd backend
uv run pytest tests/ --cov=routers --cov=main --cov-report=term-missing --cov-report=html
```

### Model-Lineage
```bash
cd model-lineage
uv run pytest tests/ --cov=graph --cov=scrapers --cov=storage --cov=lineage_scraper --cov-report=term-missing --cov-report=html
```

### Frontend
```bash
cd frontend
npm test -- --run --coverage
```

Coverage reports are also generated automatically in CI/CD and uploaded as artifacts.

## Conclusion

All services meet the 60% coverage threshold required by the milestone. The main areas for improvement are:

1. **Backend Neo4j search utilities** - Need more direct testing of search functions
2. **Model-Lineage CLI and orchestration** - Main function and argument parsing need tests
3. **Error handling paths** - Many error scenarios are untested but may be acceptable for now

The current test suite provides good coverage of core functionality, with integration tests ensuring the system works end-to-end. The uncovered code is primarily in error handling, logging, and CLI entry points, which are less critical than core business logic.
