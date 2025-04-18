#!/usr/bin/env bash

# Install all Python dependencies
pip install -r requirements.txt

# Optional: Manually link spaCy model (good practice)
python -m spacy link en_core_web_sm en_core_web_sm
