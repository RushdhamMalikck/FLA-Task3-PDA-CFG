# FLA Task 3 – PDA & CFG Case Study Lab

A small Python + Flask web application demonstrating three restricted-language case studies:

1. **Palindrome Checker** – an NPDA-style midpoint-guessing demonstration over lowercase alphabetic strings.
2. **HTML Closing Tag Validator** – stack-based matching of ordinary paired HTML tags.
3. **Programming Block Validator** – stack-based matching of `()`, `[]`, and `{}` outside quoted strings and `//` comments.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate       # macOS / Linux
# .venv\Scripts\activate        # Windows

pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Important modelling scope

This is an educational demonstration, not a complete HTML or programming-language parser.

- HTML case: ordinary paired tags are supported; comments, full HTML5 parsing rules and semantic validation are outside the model.
- Programming block case: checks delimiter nesting only; it ignores delimiters inside single/double quoted strings and `//` line comments. It does not validate the full programming-language grammar.
- Palindrome case: uses alphabetic characters after removing spaces and punctuation. The conceptual machine is nondeterministic because it guesses the midpoint. The code checks possible midpoint branches.

## Task 3 report evidence to add

- CFG productions and PDA state/stack explanation for each selected language.
- Accepted and rejected test strings.
- Step-by-step stack traces from the application.
- PDA diagrams created from the formal model.
- Limitations and why finite automata are insufficient for unbounded nesting / palindrome recognition.

## Suggested GitHub repository name

`FLA-Task3-PDA-CFG`
