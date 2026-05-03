-- HGEM PostgreSQL schema
-- Role: T1 immutable constants, experiment event log, and conflict log.
-- Run after creating the `hgem_research` database.

CREATE TABLE IF NOT EXISTS tier1_immutable (
    constant_key TEXT PRIMARY KEY,
    value_text TEXT NOT NULL,
    unit TEXT,
    domain TEXT,
    source TEXT,
    created_by TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS experiment_events (
    event_id BIGSERIAL PRIMARY KEY,
    session_id TEXT NOT NULL,
    step_number INTEGER,
    event_type TEXT NOT NULL,
    condition TEXT,
    benchmark TEXT,
    model_version TEXT,
    temperature NUMERIC,
    random_seed BIGINT,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_experiment_events_session_step
    ON experiment_events (session_id, step_number);

CREATE INDEX IF NOT EXISTS idx_experiment_events_type
    ON experiment_events (event_type);

CREATE TABLE IF NOT EXISTS conflict_log (
    conflict_id BIGSERIAL PRIMARY KEY,
    session_id TEXT NOT NULL,
    step_number INTEGER,
    candidate_text TEXT NOT NULL,
    conflicting_node_id TEXT,
    conflict_type TEXT NOT NULL,
    human_resolution TEXT,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_conflict_log_session_step
    ON conflict_log (session_id, step_number);

