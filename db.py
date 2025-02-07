from typing import List

import psycopg2
import json

def create_default_connection():
    return create_connection("rag")

def create_connection(db_name: str):
    conn = psycopg2.connect(
        host="localhost",
        database=db_name,
        user="geluso"
    )
    return conn

def reset_db(conn):
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM text_embedding_metadata",
        )
    conn.commit()

def create_text_embedding_metadata(conn, parent_id, datatype, label, summary=''):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO text_embedding_metadata (parent_id, datatype, label, summary) VALUES (%s, %s, %s, %s)",
            (parent_id, datatype, label, summary)
        )
    conn.commit()

def add_summary(conn, id, summary):
  pass

def find_one_text_embedding_metadata(conn, label):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM text_embedding_metadata WHERE label = '%s'
        """, label)
        row_id, parent_id, datatype, label, summary = cur.fetchone()
        return row_id, parent_id, datatype, label, summary

def get_all_text_embedding_metadata(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM text_embedding_metadata 
        """)
        rows = cur.fetchall()
        return rows
