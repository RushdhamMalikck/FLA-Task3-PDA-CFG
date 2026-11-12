# Case Study Report: Pushdown Automata and Context-Free Grammars

**21CSC301T Formal Language and Automata · CLA-2, Assessment Task 3**  
**Student:** Rushdham Malik

This report models three restricted validation tasks using context-free grammars (CFGs) and pushdown automata (PDAs). The models are defined over token alphabets; the Flask app supplies basic normalization and token recognition.

## 1. Palindrome checker

### Language and grammar

For the worked alphabet `{a,b}`, let `Lpal = {w ∈ {a,b}* | w = wᴿ}`. It contains the empty string.

```text
S → aSa | bSb | a | b | ε
```

The recursive rules add matching outer symbols. The base rules select an even or odd centre. The grammar is unambiguous: the first and last symbols determine the recursive rule, and length determines the base case.

### PDA

The machine nondeterministically chooses a midpoint. In its push phase it stores the first half, one symbol per stack symbol. An ε-transition chooses the comparison phase; for odd length, a competing transition consumes one centre symbol without changing the stack. The comparison phase reads each remaining symbol, checks it against the stack top, and pops. It accepts only when the input and stored half are exhausted together. See [palindrome NPDA](diagrams/palindrome-npda.svg).

For `abba`, a successful even-length branch is:

```text
(push, abba, Z0) ⊢ (push, bba, aZ0) ⊢ (push, ba, baZ0)
                 ⊢ (match, ba, baZ0) ⊢ (match, a, aZ0)
                 ⊢ (match, ε, Z0)  ACCEPT
```

A branch on `ab` that guesses the midpoint after `a` compares `b` with stack top `a`, so it rejects. Other branches either mismatch or finish with leftover stack symbols; therefore `ab` is rejected.

**Examples:** accepted `ε`, `abba`, `abcba`; rejected `ab`, `abc`, `abca`. The web app generalizes the alphabet to lowercase ASCII letters and ignores nonletters before checking.

## 2. Paired-tag checker

### Language and grammar

The token alphabet contains ordinary text and paired tags from finite set `T = {article, div, li, p, section, span, ul}`. Let `Ltag` contain token sequences where every opening tag closes with the same tag type in last-opened, first-closed order.

```text
S → text S | <t> S </t> S   for each t ∈ T
S → ε
```

A production consumes one text token or one complete nested element followed by a valid suffix. Given the stated tokenization, the first token uniquely determines the production, and a tag name fixes the matching close. Thus the grammar is unambiguous.

### PDA and traces

On `<t>`, push `t`. On `</t>`, require `t` at the stack top and pop it. Text does not change the stack. Accept at end with the bottom marker alone. A crossed, unmatched, or unsupported tag rejects. This is deterministic over the token alphabet. See [paired-tag PDA](diagrams/paired-tags-pda.svg).

For `<div><p>x</p></div>`:

```text
ε → push div → push p → ignore text → pop p → pop div → ACCEPT
Stack: [] → [div] → [div,p] → [div,p] → [div] → []
```

For `<div><p></div></p>`, `</div>` is encountered while `p` is on top; no valid transition exists, so it rejects.

**Examples:** accepted `<p></p>`, `<div><p>x</p></div>`, `<ul><li><span>x</span></li></ul>`; rejected `<p>`, `</p>`, `<div><p></div></p>`, `<main></main>`.

## 3. Programming delimiter checker

### Language and grammar

A lexical pass ignores ordinary text, string contents, and `//` comments. The remaining delimiter sequence is over `(`, `)`, `[`, `]`, `{`, `}` and must be correctly balanced and nested.

```text
S → (S)S | [S]S | {S}S | ε
```

A nonempty string has a unique first opener, its matching closer, and a remaining suffix. The grammar is unambiguous.

### PDA and traces

Push opening delimiters. A closing delimiter must match the top of the stack, which is then popped. A mismatch or empty-stack close rejects; end of input accepts only with an empty stack and no unterminated quoted string. The lexical filter has finite control, so composing it with the stack machine remains deterministic. See [delimiter PDA](diagrams/delimiters-pda.svg).

For `{[()]}`:

```text
ε → push { → push [ → push ( → pop ( → pop [ → pop { → ACCEPT
Stack: [] → [{] → [{,[] → [{,[,(] → [{,[] → [{] → []
```

For `([)]`, `)` finds `[` on top instead of `(` and rejects immediately.

**Examples:** accepted `()`, `{[()]}`, `if(a){x[0]=(b+c);}`, `call("["); // } ignored`; rejected `(`, `([)]`, `x]`, and an unterminated string such as `"unclosed`.

## Why use a stack?

For the balanced-parentheses language, suppose a DFA has pumping length `p`. In `(`^p`)`^p, any split `xyz` with `|xy| ≤ p` and `|y| > 0` places `y` entirely among the opening parentheses. Pumping `y` adds opening parentheses without matching closers, contradicting balance. Thus no finite automaton recognizes arbitrary nesting. A PDA's stack stores an unbounded sequence of unmatched openers. An unmarked palindrome similarly requires storing a prefix and comparing it in reverse; the NPDA also guesses where that prefix ends.

## Scope and limitations

- The app's palindrome policy lowercases ASCII letters and ignores punctuation and whitespace; the formal example uses `{a,b}` and includes ε.
- The tag model uses only the finite tag set above, ordinary paired tags, and ignored text. Self-closing tags, comments, full attribute syntax, void elements, and HTML5 parsing are outside its language.
- The programming model checks delimiter nesting and closed quoted strings while skipping `//` comments. It is not a parser for a complete programming language.
- The app simulates these checks in Python; it is not itself a literal nondeterministic PDA implementation.
