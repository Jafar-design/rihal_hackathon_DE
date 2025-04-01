#!/bin/bash

# Exit immediately if a command fails
set -e

echo "🔄 Installing dbt dependencies..."
dbt deps

echo "🚀 Running dbt transformations..."
dbt run 

echo "✅ dbt run completed successfully."

echo "🔄 Generating documentation..."
dbt docs generate 

echo "✅ dbt documentation generated successfully."

cp -r target/* docs/

echo "🔄 Generating lineage..."

dbt docs serve --port 8081

echo "🔄 dbt lineage formed successfully."


# Keep the container running to allow logs inspection (optional)
tail -f /dev/null
