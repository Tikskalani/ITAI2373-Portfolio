"""Report and result export helpers for NewsBot 2.0."""
import json, os


def save_json(obj, path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    json.dump(obj, open(path, "w", encoding="utf-8"), indent=2, default=str)
    return path


def dict_to_markdown(d, title="Results"):
    lines = [f"# {title}", ""]
    for k, v in d.items():
        lines.append(f"- **{k}:** {v}")
    return "\n".join(lines)
