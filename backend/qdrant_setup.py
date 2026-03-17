from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")
collection_name = "knowba-3"

def ensure_collection():
    collections = [c.name for c in client.get_collections().collections]
    if collection_name not in collections:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=3, distance=models.Distance.COSINE),
        )

# Add points to collection (POST /collections/:collection_name/points)
def upsert_points(points: list[models.PointStruct]):
    client.upsert(
        collection_name=collection_name,
        points=points
    )

# set extra payload for points (POST /collections/:collection_name/points/payload)
def set_payload(payload: dict, points: list[int]):
    client.set_payload(
        collection_name=collection_name,
        payload=payload,
        points=points
    )

def query_points(query, prefetch=None):
    return client.query_points(
        collection_name=collection_name,
        prefetch=prefetch,
        query=query
    )

# search points (POST /collections/:collection_name/points/search)
# curl  -X POST   'http://localhost:6333/collections/knowba-3/points/search'   --
# header 'Content-Type: application/json'   --data-raw '{
#   "vector": [
#     0.2,
#     0.1,
#     0.9
#   ],
#   "limit": 1,
#   "filter": {
#     "must": [
#       {
#         "key": "color",
#         "match": {
#           "value": "blue"
#         }
#       }
#     ]
#   }
#}'