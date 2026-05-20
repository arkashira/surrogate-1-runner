def run_review_engine(multi_issue_mode: bool = False) -> None:
    """
    Core review engine entry point.

    Parameters
    ----------
    multi_issue_mode:
        *True*  – run in “report all issues” (multi‑issue) mode.  
        *False* – run in the historic single‑issue mode.
    """
    if multi_issue_mode:
        print("Running review engine in multi-issue mode")
        # TODO: real multi‑issue implementation goes here.
    else:
        print("Running review engine in single-issue mode")
        # TODO: real single‑issue implementation goes here.