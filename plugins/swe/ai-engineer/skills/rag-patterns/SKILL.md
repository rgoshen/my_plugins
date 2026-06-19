---
name: rag-patterns
description: Use when building RAG pipelines, choosing chunking strategy, selecting a vector store, designing retrieval, handling retrieval misses, evaluating RAG quality, or deciding between RAG and fine-tuning. Also for embedding model selection, hybrid search, re-ranking, or context window management for retrieved documents.
---

# RAG Patterns

Reference for implementing Retrieval-Augmented Generation systems.

## When RAG is the Right Pattern

Use when:
- Knowledge changes frequently (policies, product docs, legal filings)
- Data is private or proprietary — can't bake into a model via fine-tuning
- You need citation or provenance
- Model hallucinates on domain-specific questions not in its training data

**When it isn't:** general knowledge already in the model; context window can hold all relevant info; task doesn't require document grounding; retrieval latency breaks UX.

## Document Processing

| Decision | Options | Tradeoffs |
|---|---|---|
| **Chunking strategy** | Fixed-size, recursive/hierarchical, semantic, document-aware | Fixed-size splits thoughts mid-sentence. Semantic preserves meaning but produces variable-size chunks. Document-aware is best but requires format-specific parsers. |
| **Chunk size** | 256–2048 tokens typical | Smaller = more precise retrieval, risk splitting answers across chunks. Larger = more context per result, lower precision. |
| **Chunk overlap** | 0–20% of chunk size | Reduces chance of splitting key passages at boundaries. Too much wastes storage. |
| **Metadata** | Source, section, date, author, document type | Enables filtered retrieval and citation. Extract at ingestion, not query time. |

## Embedding Model Selection

- Match the embedding model to your domain. General-purpose (`text-embedding-3-small`, `all-MiniLM-L6-v2`) works for broad content. Domain-specific content (legal, medical, code) may need a domain-trained embedder.
- Dimensionality: higher captures more nuance, costs more to store and search. 384–1536 covers most cases.
- Test retrieval quality before committing: embed a sample, run representative queries, check top-k results. One hour of testing prevents weeks of debugging a generation problem that's really a retrieval problem.

## Vector Store Options

| Option | Best for | Watch out for |
|---|---|---|
| **FAISS** | Local, in-memory, fast prototyping | No persistence by default, no metadata filtering |
| **Chroma** | Local dev, simple API, metadata support | Performance at scale |
| **pgvector** | Teams already on PostgreSQL, hybrid SQL + vector queries | Requires PostgreSQL ops, indexing tuning |
| **Pinecone / Weaviate / Qdrant** | Managed, production scale, filtered search | Vendor lock-in, cost at scale |

## Retrieval Strategy

- **Top-k**: simple baseline. Start k=3–5, adjust for context window budget.
- **Hybrid search** (dense + sparse BM25): catches exact term matches semantic similarity misses. Worth the complexity for queries with specific identifiers or product codes.
- **Re-ranking**: retrieve top-20, re-rank with cross-encoder to get best top-5. Adds latency, meaningfully improves precision.
- **Context window budget**: retrieved chunks compete with system prompt, conversation history, and generation budget. Budget explicitly.
- **Retrieval misses**: when no chunk scores above threshold, say "I don't have enough information" rather than hallucinate. Requires a deliberate threshold, not hope.

## RAG Evaluation

RAG fails in two independent ways — measure both separately:

| Failure type | What went wrong | How to measure |
|---|---|---|
| **Bad retrieval** | Right document wasn't retrieved | Recall@k, MRR, precision@k — against labeled query-to-document mapping |
| **Bad generation** | Right document retrieved but model hallucinated or ignored it | Faithfulness, relevance, attribution accuracy |

Build separate eval sets for retrieval quality and end-to-end quality. A generation problem is often a retrieval problem in disguise — measure retrieval first.
