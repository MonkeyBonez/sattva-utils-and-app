Schema for lessons_e5_small_v2.npz

- embeddings: float32, shape (N, 384)
- ids: int32, shape (N,)
- texts: object array of str, length N
- model: str, expected "intfloat/e5-small-v2"
- source: str path to lessons.txt
- hash: SHA256 of input lines

Notes:
- Embeddings are L2-normalized at build time; cosine = dot.
- Rebuild overwrites if input changed; use --skip-if-unchanged to avoid.



