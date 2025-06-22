#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Install system dependencies for WeasyPrint PDF support
sudo apt-get update
sudo apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 libcairo2 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

echo "Installing development requirements..."
python -m pip install -r .devcontainer/requirements_dev.txt

echo "Installing documentation requirements..."
python -m pip install -r .devcontainer/requirements_docs.txt

echo "Setup complete!"
