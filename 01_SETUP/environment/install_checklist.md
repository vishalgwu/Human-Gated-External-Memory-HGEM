# HGEM Step 1 Install Checklist

Use this checklist before moving to Step 2.

## Python Environment

- [x] Python 3.10+ available
- [x] Virtual environment created at repo root: `HGEM`
- [x] Virtual environment activated successfully
- [x] `pip` upgraded inside the virtual environment
- [x] Dependencies installed from `01_SETUP/environment/requirements.txt`
- [x] `pip freeze` exported after install

## Required Services

- [ ] PostgreSQL 15+ installed
- [ ] PostgreSQL database `hgem_research` created
- [ ] PostgreSQL tables planned: `tier1_immutable`, `experiment_events`, `conflict_log`
- [ ] Neo4j 5.x installed or available
- [ ] Neo4j database/service available for T2 graph memory
- [ ] Redis installed or available on port `6379`
- [x] ChromaDB Python package installed for local measurement index

## Credentials

- [x] `01_SETUP/credentials/.env.template` reviewed
- [x] Local `.env` created from template, with real values only on local machine
- [x] `.env` ignored by Git
- [ ] OpenAI API key added only to local `.env`

## HGEM Experiment Constants

- [x] Experiment model documented as `gpt-4o-2024-08-06`
- [x] Temperature documented as `0.0`
- [ ] GPT model version will be logged on every API call
- [ ] All database connection strings recorded locally, not committed

## Gate Before Step 2

- [x] Folder structure exists
- [x] `versions.txt` filled
- [x] `.env.template` created with key names only
- [x] All service clients import successfully in Python
- [x] PostgreSQL, Neo4j, Redis, and ChromaDB are in the setup plan
