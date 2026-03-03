from retrieval.retrieve import retrieve


def detect_query_type(query: str):
    q = query.lower()

    visual_keywords = ["image", "picture", "graph", "chart", "shown", "displayed", "color"]
    numeric_keywords = ["how many", "number", "total", "sum", "count", "percentage"]

    if any(k in q for k in visual_keywords):
        return "visual"

    if any(k in q for k in numeric_keywords):
        return "numeric"

    return "textual"


def orchestrate(query, doc_id):
    # 🔹 Retrieve filtered by doc_id
    texts, images = retrieve(query, doc_id)

    query_type = detect_query_type(query)

    context = []

    # 🔹 Preserve your modality logic behavior
    if query_type == "visual":
        # prioritize images
        for img in images:
            context.append({
                "type": "image",
                "content": img["path"],
                "description": img.get("caption", "")
            })
        for txt in texts:
            context.append({"type": "text", "content": txt})

    elif query_type == "numeric":
        # prioritize text
        for txt in texts:
            context.append({"type": "text", "content": txt})
        for img in images:
            context.append({"type": "image", "content": img})

    else:
        # balanced
        for txt in texts:
            context.append({"type": "text", "content": txt})
        for img in images:
            context.append({"type": "image", "content": img})

    return {
        "query_type": query_type,
        "context": context
    }