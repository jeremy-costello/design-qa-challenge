def build_prompt(
    system_prompt: str,
    question: str,
    rule_texts_map: dict[str, list[str]] | None = None,
    mech_texts_map: dict[str, list[str]] | None = None,
) -> str:
    parts = [system_prompt]

    if rule_texts_map:
        for rule_num, texts in rule_texts_map.items():
            for t in texts:
                parts.append(f"Rule {rule_num}: {t}")

    if mech_texts_map:
        for term, texts in mech_texts_map.items():
            parts.append(f"Mechanical Context (related to '{term}'):")
            for t in texts:
                parts.append(t)

    parts.append(f"\nQuestion: {question}")
    return "\n\n".join(parts)
