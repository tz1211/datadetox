#!/bin/bash
# Wrapper script for batch testing from outside the container

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}DataDetox Batch Testing Wrapper${NC}\n"

# Check if backend is running
if ! docker ps | grep -q datadetox-backend; then
    echo -e "${YELLOW}Backend container not running. Starting...${NC}"
    docker-compose up -d backend
    sleep 3
fi

# Handle --sample flag
if [ "$1" == "--sample" ]; then
    echo -e "${GREEN}Creating sample CSV...${NC}"
    docker exec datadetox-backend-1 uv run python batch_testing/batch_test.py --sample
    echo -e "\n${GREEN}✓ Sample created in container at: batch_testing/input/sample_queries.csv${NC}"
    echo -e "\n${YELLOW}Next steps:${NC}"
    echo -e "  1. Run batch test: ${CYAN}./batch_test.sh sample_queries.csv${NC}"
    echo -e "  2. Get results:    ${CYAN}./batch_test.sh --get sample_queries_results.csv${NC}"
    exit 0
fi

# Handle --get flag (copy results from container)
if [ "$1" == "--get" ]; then
    if [ -z "$2" ]; then
        echo -e "${YELLOW}Available output files:${NC}"
        docker exec datadetox-backend-1 ls -1 batch_testing/output/ 2>/dev/null || echo "  (none)"
        echo -e "\n${YELLOW}Usage:${NC} ./batch_test.sh --get <filename>"
        echo -e "${YELLOW}Example:${NC} ./batch_test.sh --get sample_queries_results.csv"
        exit 0
    fi

    OUTPUT_FILE="$2"
    echo -e "${GREEN}Copying results from container...${NC}"
    docker cp datadetox-backend-1:/app/batch_testing/output/"$OUTPUT_FILE" ./"$OUTPUT_FILE"
    echo -e "${GREEN}✓ Saved to: ${CYAN}$OUTPUT_FILE${NC}"
    exit 0
fi

# Handle --list flag (list available files)
if [ "$1" == "--list" ]; then
    echo -e "${CYAN}Input files (batch_testing/input/):${NC}"
    docker exec datadetox-backend-1 ls -lh batch_testing/input/ 2>/dev/null || echo "  (none)"
    echo -e "\n${CYAN}Output files (batch_testing/output/):${NC}"
    docker exec datadetox-backend-1 ls -lh batch_testing/output/ 2>/dev/null || echo "  (none)"
    exit 0
fi

# Validate arguments
if [ $# -lt 1 ]; then
    echo -e "${YELLOW}Usage:${NC}"
    echo "  ./batch_test.sh input_file.csv [output_file.csv]  # Run batch test"
    echo "  ./batch_test.sh --sample                          # Create sample CSV"
    echo "  ./batch_test.sh --get output_file.csv             # Copy results from container"
    echo "  ./batch_test.sh --list                            # List available files"
    echo "  ./batch_test.sh --put local_file.csv              # Upload CSV to container"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  ./batch_test.sh --sample                          # Create sample"
    echo "  ./batch_test.sh sample_queries.csv                # Run test (auto-generates output name)"
    echo "  ./batch_test.sh --get sample_queries_results.csv  # Download results"
    exit 1
fi

# Handle --put flag (copy input to container)
if [ "$1" == "--put" ]; then
    if [ -z "$2" ]; then
        echo -e "${RED}Error: Please specify a file to upload${NC}"
        echo -e "${YELLOW}Usage:${NC} ./batch_test.sh --put my_queries.csv"
        exit 1
    fi

    if [ ! -f "$2" ]; then
        echo -e "${RED}Error: File not found: $2${NC}"
        exit 1
    fi

    echo -e "${GREEN}Uploading CSV to container...${NC}"
    docker cp "$2" datadetox-backend-1:/app/batch_testing/input/
    echo -e "${GREEN}✓ Uploaded to: batch_testing/input/$(basename "$2")${NC}"
    exit 0
fi

INPUT_CSV="$1"
OUTPUT_CSV="${2:-}"  # Optional

echo -e "${GREEN}Running batch test...${NC}\n"

# Run batch test in container
if [ -z "$OUTPUT_CSV" ]; then
    # Auto-generate output name
    docker exec -it datadetox-backend-1 uv run python batch_testing/batch_test.py "$INPUT_CSV"
else
    # Use specified output name
    docker exec -it datadetox-backend-1 uv run python batch_testing/batch_test.py "$INPUT_CSV" "$OUTPUT_CSV"
fi

echo -e "\n${GREEN}✓ Batch test complete!${NC}"
echo -e "\n${YELLOW}To download results:${NC}"

# Figure out output filename
if [ -z "$OUTPUT_CSV" ]; then
    # Auto-generated name
    INPUT_STEM="${INPUT_CSV%.csv}"
    AUTO_OUTPUT="${INPUT_STEM}_results.csv"
    echo -e "  ./batch_test.sh --get ${AUTO_OUTPUT}"
else
    echo -e "  ./batch_test.sh --get ${OUTPUT_CSV}"
fi
