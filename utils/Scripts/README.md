## Scripting Area

Utilities for lesson clustering, review, and retrieval.

### Layout
- `outputs/` — intermediate JSONL/MD (clusters, human passes, reviews)
- `Embeddings/` — semantic search artifacts
  - `lessons.txt` — one lesson per line
  - `lessons_e5_small_v2.npz` — packed embeddings index
  - `README.md` — schema/version
- `make_lessons_txt.py` — human-pass JSONL → lessons.txt
- `build_embeddings.py` — build E5 embeddings from lessons.txt
- `search_lessons.py` — search with a query

### Model
- `intfloat/e5-small-v2` (Hugging Face). Asymmetric prefixes:
  - Passages: `passage: <text>`
  - Queries: `query: <text>`
- Embeddings are L2-normalized, so cosine similarity = dot product.

### Quick usage
1) Make lessons.txt from human pass:
```
python utils/Scripts/make_lessons_txt.py utils/Scripts/outputs/humanpass_pt2.jsonl \
  -o utils/Scripts/Embeddings/lessons.txt
```
2) Build embeddings:
```
python utils/Scripts/build_embeddings.py utils/Scripts/Embeddings/lessons.txt \
  --emb-path utils/Scripts/Embeddings/lessons_e5_small_v2.npz
```
3) Search:
```
python utils/Scripts/search_lessons.py "I feel anxious before a big meeting" --topk 10 \
  --emb-path utils/Scripts/Embeddings/lessons_e5_small_v2.npz
```

### `.npz` schema
- `embeddings` — float32, shape `(N, 384)`
- `ids` — int32, shape `(N,)` (sequential 0..N-1)
- `texts` — object array of original lines (len `N`)
- `model` — string, `intfloat/e5-small-v2`
- `source` — lessons.txt path
- `hash` — SHA256 of input lines




