"""Turn analysis results into readable natural-language answers (NewsBot 2.0, Module D)."""


class ResponseGenerator:
    def format(self, intent: str, result) -> str:
        if intent == "classify":
            return f"This looks like {result.get('category')} news (confidence {result.get('confidence')})."
        if intent == "sentiment":
            return f"The overall tone is {result.get('label')} (compound score {result.get('compound')}, emotion: {result.get('emotion')})."
        if intent == "entities":
            ents = ", ".join(f"{t} ({l})" for t, l in result) if result else "none found"
            return f"Entities detected: {ents}."
        if intent == "summarize":
            return f"Summary: {result}"
        if intent == "search":
            if not result:
                return "No matching articles found."
            lines = [f"  #{i} (score {s}): {snippet.strip()}..." for i, s, snippet in result]
            return "Top matches:\n" + "\n".join(lines)
        if intent == "topics":
            return "Discovered topics:\n" + "\n".join(f"  Topic {k}: {', '.join(w)}" for k, w in result.items())
        return str(result)
