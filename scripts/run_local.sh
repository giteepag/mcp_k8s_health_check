#!/bin/bash
export PROMETHEUS_URL="http://us6sxlx01893.corpnet2.com:9090"
uvicorn app.main:app --reload --port 8000
streamlit run ui.py