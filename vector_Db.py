import faiss
import numpy as np
import pickle

def build_faiss_index(embeddings, dim=384, index_file_path="faiss_index.bin", metadata_file="metadata.pkl"):

    index = faiss.IndexFlatL2(dim)

    vectors = []
    ids = []
    texts = []

    for rec_id, text, emb in embeddings:
        ids.append(rec_id)
        texts.append(text)
        vectors.append(np.array(emb, dtype=np.float32))

    vectors = np.vstack(vectors)

    index.add(vectors)

    faiss.write_index(index, index_file_path)

    with open(metadata_file, "wb") as f:
        pickle.dump({"ids": ids, "texts": texts}, f)

    print(f"FAISS index saved to {index_file_path}")
    print(f"Metadata saved to {metadata_file}")

    return index
