import json

def evaluate(pred_file, gt_file):
    with open(pred_file, "r") as f:
        preds = json.load(f)

    with open(gt_file, "r") as f:
        gt = json.load(f)

    hit_count = 0
    mrr_total = 0

    for p, g in zip(preds, gt):
        predicted = p["retrieved_standards"]
        expected = g["expected_standards"]

        # Hit@3
        if any(e in predicted[:3] for e in expected):
            hit_count += 1

        # MRR@5
        rank = 0
        for i, val in enumerate(predicted[:5]):
            if val in expected:
                rank = i + 1
                break
        if rank > 0:
            mrr_total += 1 / rank

    total = len(gt)

    hit_rate = hit_count / total
    mrr = mrr_total / total

    print(f"Hit Rate @3: {hit_rate:.2f}")
    print(f"MRR @5: {mrr:.2f}")

if __name__ == "__main__":
    evaluate("output.json", "public_test.json")