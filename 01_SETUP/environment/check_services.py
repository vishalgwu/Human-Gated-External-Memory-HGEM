from __future__ import annotations

import os
from pathlib import Path

import chromadb
import psycopg
import redis
from dotenv import load_dotenv
from neo4j import GraphDatabase
from openai import OpenAI


REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = REPO_ROOT / "01_SETUP" / "credentials" / ".env"


def env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def check_postgres() -> None:
    conninfo = (
        f"host={env('POSTGRES_HOST', 'localhost')} "
        f"port={env('POSTGRES_PORT', '5432')} "
        f"dbname={env('POSTGRES_DB', 'hgem_research')} "
        f"user={env('POSTGRES_USER', 'hgem_app')} "
        f"password={env('POSTGRES_PASSWORD')}"
    )
    with psycopg.connect(conninfo) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            cur.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
                """
            )
            tables = [row[0] for row in cur.fetchall()]
    print(f"PostgreSQL OK: {version.split(',')[0]}")
    print(f"PostgreSQL tables: {', '.join(tables)}")


def check_neo4j() -> None:
    driver = GraphDatabase.driver(
        env("NEO4J_URI", "bolt://localhost:7687"),
        auth=(env("NEO4J_USER", "neo4j"), env("NEO4J_PASSWORD")),
    )
    try:
        driver.verify_connectivity()
        with driver.session(database=env("NEO4J_DATABASE", "neo4j")) as session:
            result = session.run(
                """
                CALL dbms.components()
                YIELD name, versions, edition
                RETURN name, versions[0] AS version, edition
                """
            )
            component = result.single()
            constraints = session.run("SHOW CONSTRAINTS YIELD name RETURN name ORDER BY name")
            constraint_names = [record["name"] for record in constraints]
        print(
            f"Neo4j OK: {component['name']} {component['version']} "
            f"({component['edition']})"
        )
        print(f"Neo4j constraints: {', '.join(constraint_names)}")
    finally:
        driver.close()


def check_redis() -> None:
    client = redis.Redis(
        host=env("REDIS_HOST", "localhost"),
        port=int(env("REDIS_PORT", "6379")),
        db=int(env("REDIS_DB", "0")),
        decode_responses=True,
    )
    pong = client.ping()
    info = client.info("server")
    print(f"Redis OK: {info['redis_version']} ping={pong}")


def check_chromadb() -> None:
    configured_path = env(
        "CHROMA_PERSIST_DIRECTORY",
        "03_SYSTEM/database/chromadb/chroma_store",
    )
    path = (REPO_ROOT / configured_path).resolve()
    client = chromadb.PersistentClient(path=str(path))
    heartbeat = client.heartbeat()
    print(f"ChromaDB OK: heartbeat={heartbeat} path={path}")


def check_openai_env() -> None:
    api_key = env("OPENAI_API_KEY")
    model = env("OPENAI_MODEL", "gpt-4o-2024-08-06")
    if api_key:
        client = OpenAI(api_key=api_key)
        models = client.models.list()
        first_model = models.data[0].id if models.data else "no-models-returned"
        print(
            f"OpenAI auth OK: model={model}, "
            f"models endpoint reachable, first_model={first_model}"
        )
    else:
        print(f"OpenAI env SKIPPED: model={model}, API key missing")


def main() -> None:
    load_dotenv(ENV_PATH)
    print(f"Using env file: {ENV_PATH}")
    check_openai_env()
    check_postgres()
    check_neo4j()
    check_redis()
    check_chromadb()


if __name__ == "__main__":
    main()
