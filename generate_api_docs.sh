#!/bin/bash
# Telemedicine API Documentation Generator - Linux/Mac Script
# Usage: chmod +x generate_api_docs.sh && ./generate_api_docs.sh

set -e

echo ""
echo "========================================================================"
echo ""
echo "  TELEMEDICINE API DOCUMENTATION GENERATOR"
echo ""
echo "========================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo ""
    echo "Please install Python 3.7+ from https://www.python.org"
    echo ""
    exit 1
fi

echo "[*] Python version:"
python3 --version
echo ""

# Run the quick generator
echo "[*] Running API documentation generator..."
echo ""

python3 quick_generate_docs.py

exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo ""
    echo "[ERROR] Generator failed. Check the output above."
    exit 1
fi

echo ""
echo "[SUCCESS] All documentation files generated!"
echo ""

# Try to open HTML file
if command -v open &> /dev/null; then
    # macOS
    if [ -f "API_DOCS.html" ]; then
        echo "[*] Opening API_DOCS.html in default browser..."
        open API_DOCS.html
    fi
elif command -v xdg-open &> /dev/null; then
    # Linux
    if [ -f "API_DOCS.html" ]; then
        echo "[*] Opening API_DOCS.html in default browser..."
        xdg-open API_DOCS.html &
    fi
fi

echo ""
echo "[*] Generated files:"
echo "    - SWAGGER_SPEC.json (OpenAPI 3.0)"
echo "    - POSTMAN_COLLECTION.json"
echo "    - API_DOCS_AUTO_GENERATED.md"
echo "    - API_DOCS.html"
echo ""
echo "Done!"
echo ""
