"""
Three restricted-language demonstrations for Formal Language and Automata.

1) Palindrome: an NPDA-style midpoint-guessing simulation over a finite alphabet of lowercase letters.
2) HTML: stack-based matching of ordinary opening/closing tags.
3) Programming blocks: stack-based matching of (), [] and {} outside strings/comments.

These are educational subsets, not complete HTML or programming-language parsers.
"""

import re


def check_palindrome(raw):
    # The application accepts case-insensitive ASCII letters and ignores
    # punctuation/whitespace. The formal language itself is over {a,b} in
    # the worked case study; the recognizer generalises this to ASCII letters.
    value = "".join(ch.lower() for ch in raw if ch.isascii() and ch.isalpha())

    
    # Nondeterministic PDA idea:
    # For every possible midpoint, push the first half, then compare/pop
    # the second half. The NPDA accepts if at least one branch succeeds.
    branches = []
    n = len(value)
    accepted_midpoint = None

    for midpoint in range(n + 1):
        stack = []
        trace = [f"Branch guesses midpoint after position {midpoint}."]
        for ch in value[:midpoint]:
            stack.append(ch)
            trace.append(f"Read '{ch}' before midpoint: PUSH '{ch}' -> stack {stack}")
        ok = True
        for ch in value[midpoint:]:
            if not stack:
                # Odd-length strings need one centre symbol to be skipped.
                # This branch handles the centre by considering midpoint+1
                # as another possible guess; this branch itself fails.
                ok = False
                trace.append(f"Read '{ch}' but stack is empty -> branch rejects.")
                break
            top = stack.pop()
            trace.append(f"Read '{ch}': POP '{top}' -> stack {stack}")
            if ch != top:
                ok = False
                trace.append(f"Mismatch: input '{ch}' != stack symbol '{top}'.")
                break
        if ok and not stack:
            # The split is valid only when second half is reverse(first half).
            # For odd lengths, the midpoint branch is represented by a
            # separate branch that skips the centre symbol.
            if value[:midpoint] == value[midpoint:][::-1]:
                accepted_midpoint = midpoint
                branches = trace + ["Stack is empty and both halves match: ACCEPT."]
                break

    # Explicitly test odd-length midpoint guesses by skipping the centre.
    if accepted_midpoint is None:
        for centre in range(n):
            left = value[:centre]
            right = value[centre + 1:]
            if left == right[::-1]:
                stack = []
                trace = [f"Branch guesses '{value[centre]}' as the middle symbol."]
                for ch in left:
                    stack.append(ch)
                    trace.append(f"Read '{ch}': PUSH -> stack {stack}")
                for ch in right:
                    top = stack.pop()
                    trace.append(f"Read '{ch}': POP '{top}' -> stack {stack}")
                    if ch != top:
                        break
                if not stack:
                    accepted_midpoint = centre
                    branches = trace + ["Middle symbol skipped; remaining halves match: ACCEPT."]
                    break

    if accepted_midpoint is None and value == "":
        accepted_midpoint = 0

    if accepted_midpoint is None:
        # Empty string is also a palindrome, but blank input is rejected above.
        return {
            "accepted": False,
            "title": "Rejected",
            "message": f"'{value}' is not a palindrome.",
            "steps": [f"Input: {value}",
                      "The NPDA tried possible midpoint positions.",
                      "Every branch found a mismatch or leftover stack symbol.",
                      "Therefore, the input is rejected."],
            "model": "NPDA-style palindrome recognizer"
        }

    return {
        "accepted": True,
        "title": "Accepted",
        "message": f"'{value}' is a palindrome.",
        "steps": [f"Input: {value}"] + branches,
        "model": "NPDA-style palindrome recognizer"
    }


def check_html(source):
    # Deliberately limited tag language. A finite tag alphabet is required
    # for a classical PDA model; real HTML has many additional lexical rules.
    token_re = re.compile(r"</?([A-Za-z][A-Za-z0-9-]*)\b[^>]*>")
    allowed_tags = {"article", "div", "li", "p", "section", "span", "ul"}
    stack = []
    steps = []
    pos = 0
    tokens = list(token_re.finditer(source))

    if not source.strip():
        return {
            "accepted": False, "title": "Rejected",
            "message": "Enter an HTML fragment to validate.",
            "steps": ["No HTML input was provided."],
            "model": "PDA stack model for a finite set of nested tags"
        }

    # Ensure every angle-bracket tag-like region is tokenized in this subset.
    for match in tokens:
        between = source[pos:match.start()]
        if "<" in between or ">" in between:
            return {
                "accepted": False, "title": "Rejected",
                "message": "Malformed or unsupported tag syntax was found.",
                "steps": [f"Unexpected tag syntax near: {between.strip()}"],
                "model": "PDA stack model for a finite set of nested tags"
            }
        pos = match.end()

    if "<" in source[pos:] or ">" in source[pos:]:
        return {
            "accepted": False, "title": "Rejected",
            "message": "Malformed or unsupported tag syntax was found.",
            "steps": ["The remaining input contains an unmatched '<' or '>'."],
            "model": "PDA stack model for a finite set of nested tags"
        }

    for match in tokens:
        token = match.group(0)
        tag = match.group(1).lower()
        is_closing = token.startswith("</")
        is_self_closing = token.rstrip().endswith("/>")

        if tag not in allowed_tags:
            steps.append(f"{token}: tag is outside the supported finite alphabet -> REJECT.")
            return {
                "accepted": False, "title": "Rejected",
                "message": f"Tag <{tag}> is not in the supported tag set.",
                "steps": steps, "model": "PDA stack model for a finite set of nested tags"
            }

        if is_self_closing:
            steps.append(f"{token}: self-closing tags are outside the supported model -> REJECT.")
            return {
                "accepted": False, "title": "Rejected",
                "message": "Self-closing tags are outside this case study's language.",
                "steps": steps, "model": "PDA stack model for a finite set of nested tags"
            }

        if is_closing:
            if not stack:
                steps.append(f"{token}: stack empty, no opening tag to match -> REJECT.")
                return {
                    "accepted": False, "title": "Rejected",
                    "message": f"Closing tag </{tag}> has no matching opening tag.",
                    "steps": steps, "model": "PDA stack model for a finite set of nested tags"
                }
            top = stack[-1]
            if top != tag:
                steps.append(f"{token}: top of stack is <{top}>; mismatch -> REJECT.")
                return {
                    "accepted": False, "title": "Rejected",
                    "message": f"Tag mismatch: expected </{top}> but found </{tag}>.",
                    "steps": steps, "model": "PDA stack model for a finite set of nested tags"
                }
            stack.pop()
            steps.append(f"{token}: POP '{tag}' -> stack {stack}")
        else:
            stack.append(tag)
            steps.append(f"{token}: PUSH '{tag}' -> stack {stack}")

    if stack:
        return {
            "accepted": False, "title": "Rejected",
            "message": "One or more opening tags were not closed.",
            "steps": steps + [f"Input ended with unclosed tags: {stack}"],
            "model": "PDA stack model for a finite set of nested tags"
        }

    return {
        "accepted": True, "title": "Accepted",
        "message": "All supported tags are properly nested and closed.",
        "steps": steps + ["Input ended with an empty stack: ACCEPT."],
        "model": "PDA stack model for a finite set of nested tags"
    }


def check_blocks(source):
    # Restricted programming-block checker:
    # validates (), [], {} nesting and ignores delimiters inside quoted
    # strings and // line comments. It does not parse full program syntax.
    pairs = {")": "(", "]": "[", "}": "{"}
    opening = set(pairs.values())
    stack = []
    steps = []
    i = 0
    quote = None
    escaped = False
    in_line_comment = False

    if not source.strip():
        return {
            "accepted": False, "title": "Rejected",
            "message": "Enter a code fragment to validate.",
            "steps": ["No program text was provided."],
            "model": "PDA stack model for programming delimiters"
        }

    while i < len(source):
        ch = source[i]
        nxt = source[i + 1] if i + 1 < len(source) else ""

        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
            i += 1
            continue

        if quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
            i += 1
            continue

        if ch == "/" and nxt == "/":
            in_line_comment = True
            i += 2
            continue
        if ch in ("'", '"'):
            quote = ch
            i += 1
            continue

        if ch in opening:
            stack.append(ch)
            steps.append(f"Read '{ch}': PUSH -> stack {stack}")
        elif ch in pairs:
            if not stack:
                steps.append(f"Read '{ch}': stack empty -> REJECT.")
                return {
                    "accepted": False, "title": "Rejected",
                    "message": f"Closing symbol '{ch}' has no opening match.",
                    "steps": steps, "model": "PDA stack model for programming delimiters"
                }
            top = stack[-1]
            if top != pairs[ch]:
                steps.append(f"Read '{ch}': expected close for '{top}' is mismatched -> REJECT.")
                return {
                    "accepted": False, "title": "Rejected",
                    "message": f"'{ch}' does not match the most recent opening symbol '{top}'.",
                    "steps": steps, "model": "PDA stack model for programming delimiters"
                }
            stack.pop()
            steps.append(f"Read '{ch}': POP '{top}' -> stack {stack}")
        i += 1

    if quote:
        return {
            "accepted": False, "title": "Rejected",
            "message": "A string literal was not closed.",
            "steps": steps + ["Input ended while inside a quoted string."],
            "model": "PDA stack model for programming delimiters"
        }

    if stack:
        return {
            "accepted": False, "title": "Rejected",
            "message": f"Unclosed opening symbols remain: {stack}.",
            "steps": steps + [f"Input ended with non-empty stack: {stack}"],
            "model": "PDA stack model for programming delimiters"
        }

    return {
        "accepted": True, "title": "Accepted",
        "message": "All supported programming delimiters are correctly nested.",
        "steps": steps + ["Input ended with an empty stack: ACCEPT."],
        "model": "PDA stack model for programming delimiters"
    }
