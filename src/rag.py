import re

def clean_id(std_id):
    # remove newline, extra spaces
    std_id = std_id.replace("\n", "").strip()
    
    # ensure format: IS XXXX
    match = re.search(r"IS\s*(\d+)", std_id)
    if match:
        return f"IS {match.group(1)}"
    
    return std_id


def generate_answer(query, retrieved_standards):
    seen = set()
    results = []

    query_lower = query.lower()

    for item in retrieved_standards:
        std_id = clean_id(item["standard_id"])

        if std_id in seen:
            continue

        text = item["text"]
        text_lower = text.lower()

        # Smart filtering
        if "cement" in query_lower:
            if not any(word in text_lower for word in ["cement", "opc", "portland"]):
                continue

        if "steel" in query_lower:
            if not any(word in text_lower for word in ["steel", "reinforcement", "bars"]):
                continue

        if "aggregate" in query_lower:
            if not any(word in text_lower for word in ["aggregate", "sand", "gravel"]):
                continue

        if "concrete" in query_lower:
            if not any(word in text_lower for word in ["concrete"]):
                continue

        seen.add(std_id)

        # Clean + short reason
        clean_text = text.split(".")[0]
        clean_text = clean_text.replace("\n", " ").strip()

    # remove weird symbols and extra spaces
        clean_text = re.sub(r"[^a-zA-Z0-9 :()\-]", "", clean_text)
        clean_text = re.sub(r"\s+", " ", clean_text)

    # make it short but not cut mid-word
        short_reason = " ".join(clean_text.split()[:12])

        results.append({
            "standard_id": std_id,
            "reason": short_reason
        })

    # Ensure at least 3 results (fallback if too strict)
    if len(results) < 3:
        for item in retrieved_standards:
            std_id = clean_id(item["standard_id"])
            if std_id not in seen:
                text = item["text"].split(".")[0][:80]
                results.append({
                    "standard_id": std_id,
                    "reason": text
                })
            if len(results) >= 3:
                break

    return results[:4]   