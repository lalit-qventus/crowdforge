import meilisearch
from django.conf import settings


def get_meilisearch_client():
    return meilisearch.Client(
        settings.MEILISEARCH_URL,
        settings.MEILISEARCH_API_KEY,
    )


def sync_project(project):
    client = get_meilisearch_client()
    index = client.index("projects")
    doc = {
        "id": str(project.id),
        "title": project.title,
        "slug": project.slug,
        "one_liner": project.one_liner,
        "problem": project.problem,
        "solution": project.solution,
        "tech_stack_tags": project.tech_stack_tags,
        "lifecycle_stage": project.lifecycle_stage,
    }
    index.add_documents([doc])


def sync_task(task):
    client = get_meilisearch_client()
    index = client.index("tasks")
    doc = {
        "id": str(task.id),
        "title": task.title,
        "description": task.description,
        "project_id": str(task.project_id),
        "status": task.status,
    }
    index.add_documents([doc])


def sync_user(user):
    client = get_meilisearch_client()
    index = client.index("users")
    doc = {
        "id": str(user.id),
        "username": user.username,
        "is_ai_agent": user.is_ai_agent,
        "trust_level": user.trust_level,
    }
    index.add_documents([doc])


def search(query, index=None, limit=20, offset=0) -> dict:
    client = get_meilisearch_client()
    params = {"limit": limit, "offset": offset}

    if index:
        result = client.index(index).search(query, params)
        hits = [
            {
                "id": str(hit.get("id", "")),
                "index": index,
                "title": hit.get("title", hit.get("username", "")),
                "snippet": hit.get("one_liner", hit.get("description", "")),
                "score": hit.get("_rankingScore", 0.0),
            }
            for hit in result.get("hits", [])
        ]
        return {
            "hits": hits,
            "total": result.get("estimatedTotalHits", len(hits)),
            "query": query,
        }

    # Multi-index search
    all_hits = []
    total = 0
    for idx_name in ("projects", "tasks", "users"):
        result = client.index(idx_name).search(query, params)
        for hit in result.get("hits", []):
            all_hits.append({
                "id": str(hit.get("id", "")),
                "index": idx_name,
                "title": hit.get("title", hit.get("username", "")),
                "snippet": hit.get("one_liner", hit.get("description", "")),
                "score": hit.get("_rankingScore", 0.0),
            })
        total += result.get("estimatedTotalHits", 0)

    return {
        "hits": all_hits[:limit],
        "total": total,
        "query": query,
    }


def delete_document(index, doc_id):
    client = get_meilisearch_client()
    client.index(index).delete_document(str(doc_id))
