DROP DATABASE IF EXISTS rag;
CREATE DATABASE rag;

\c rag;

CREATE TABLE text_embedding_metadata (
  id SERIAL PRIMARY KEY,
  parent_id VARCHAR(255) NULL,
  datatype VARCHAR(255) NULL,
  label VARCHAR(255) NOT NULL,
  summary TEXT NOT NULL
);

CREATE INDEX index_rag_text_embedding_metadata_ids ON text_embedding_metadata (id);
