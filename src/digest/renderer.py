
    Parameters
    ----------
    headline:
        One‑sentence summary of the overall status.
    items:
        List of :class:`DigestItem` objects.

    Returns
    -------
    str
        Markdown representation of the digest.
    """
    sorted_items = _sorted_and_truncated(items)

    lines: List[str] = [f"**{headline.strip()}**", ""]  # headline + blank line

    for idx, item in enumerate(sorted_items, start=1):
        author = item.author.strip()
        ts = _format_timestamp(item.timestamp)
        snippet = item.snippet.strip().replace("\r\n", "\n")

        # List item header
        lines.append(f"{idx}. **{author}** _{ts}_")

        # Indent each line of the snippet by three spaces
        for snippet_line in snippet.split("\n"):
            lines.append(f"   {snippet_line}")

        lines.append("")  # blank line between items

    # Remove the trailing blank line for a cleaner output
    if lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines)


def render_plain_text(headline: str, items: List[DigestItem]) -> str:
    """
    Render a digest as plain‑text (for email).

    The format mirrors the markdown version but without markdown syntax.
    """
    sorted_items = _sorted_and_truncated(items)

    lines: List[str] = [headline.strip(), ""]  # headline + blank line

    for idx, item in enumerate(sorted_items, start=1):
        author = item.author.strip()
        ts = _format_timestamp(item.timestamp)
        snippet = item.snippet.strip().replace("\r\n", "\n")

        lines.append(f"{idx}. {author} ({ts})")
        lines.append(snippet)
        lines.append("")  # blank line between items

    if lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines)