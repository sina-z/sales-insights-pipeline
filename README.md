# Sales Insights Pipeline

![CI/CD](https://github.com/sina-z/sales-insights-pipeline/actions/workflows/ci.yml/badge.svg)

A small analytics project with a full CI/CD pipeline. Every pull request is
linted (ruff) and tested (pytest) by GitHub Actions; merges to `main` that pass
all checks automatically build and deploy an HTML sales report to GitHub Pages.

**Live report:** https://sina-z.github.io/sales-insights-pipeline/

## Run locally

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    pip install -e .
    pytest
    python -m sales_insights.report