# Reviewing AI-Generated Backend Code: The Failure Modes Your Review Muscle Misses

You already review code. You already know why concatenating user input into a query is a problem, why an endpoint needs an ownership check and not just an authenticated session, why deserializing untrusted bytes is a way to get owned. None of that is the gap. The gap is that AI-generated code reads clean enough to slip past the exact instinct that would fire on a messy pull request — and it does so at a volume that turns an occasional lapse into a systematic one. This lesson layers the AI-specific failure modes onto the review discipline you already have.

## Part 1: Why Fluent Code Disarms You

### The defect is in the logic, not the syntax

When a junior engineer sends you a handler with a hand-rolled query and inconsistent naming, your skepticism fires before you've finished reading. That reaction is doing real work — the surface mess is a proxy signal that tells you to slow down.

AI-generated code removes the proxy signal. It compiles, passes linting, follows your naming conventions, and reads as idiomatic Go or Python. What remains wrong is underneath: the missing authorization check, the ORM escape hatch, the deserialization path that trusts its input. The output is surface-clean and subtly unsound at the same time, and that combination is what makes it a distinct review problem rather than just more code in the queue.

[TERM: Automation bias — the tendency to apply less scrutiny to output that looks polished or comes from an automated system, exactly when the remaining errors are hardest to see.]

### Volume makes it systematic

Two forces compound. Fluent output invites more trust, so you scrutinize it less right when the errors are getting subtler. And generation volume means more code reaches your review than you have hours to absorb carefully. A single instance of "it reads fine, ship it" is a lapse. The same reflex applied across every generated PR you approve in a week is a systematic hole in your review coverage.

The discipline is to treat "it looks fine" as a prompt to check, not a conclusion — and to spend that check where the tools can't help you, which is the subject of the rest of this lesson.

## Part 2: What AI Reintroduces in Service Code

Models are trained on large bodies of public code, insecure patterns included, and they reproduce those patterns fluently. But not every class deserves equal attention. Assuming your org already runs secret scanning, SCA (Software Composition Analysis), and reasonable SAST in CI, the pattern-level classes are largely handled upstream. What's left for you is the class that depends on *your* rules — and that's where you should spend your review budget.

### Broken authorization — your highest-leverage catch

This is the one scanners structurally cannot catch, because the correct check depends on your business rules, not a general pattern. Generated handlers implement the happy path — they do the thing — and omit the check for whether *this caller* is allowed to do it.

The pattern to watch: an endpoint that authenticates but never authorizes. The caller has a valid token, so the handler proceeds, but nothing confirms they own the resource they're acting on.

```python
# Generated Django-style handler — authenticates, never authorizes
def get_invoice(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)   # any valid user, any invoice
    return JsonResponse(serialize(invoice))
```

The fix you're looking for is an ownership or tenancy scope — `Invoice.objects.get(id=invoice_id, org=request.user.org)` or an explicit policy check. The model won't write it unless the intended rule was in the prompt, because it doesn't know your rule. This is the class that sits near the top of real-world breach data, and it's the core of what you're reviewing for.

### Injection through ORM escape hatches

You know injection. What's worth naming is *how* the model reintroduces it in code that uses an ORM — precisely the place a SAST tool is most likely to miss it. The generated code usually parameterizes correctly on the common path, then drops into a raw escape hatch for anything dynamic.

Patterns to grep for:
- **Python:** `.raw()`, `.extra()`, `cursor.execute()` with an f-string or `%` interpolation
- **Go:** `db.Query(fmt.Sprintf(...))` instead of `db.Query(query, args...)` with placeholders
- **Java:** `Statement` with concatenation instead of `PreparedStatement`; JPA `createQuery` with string-built predicates

```go
// Generated Go — dynamic filter built by concatenation
q := fmt.Sprintf("SELECT * FROM orders WHERE status = '%s'", status)
rows, _ := db.Query(q)   // status flows straight in
```

The tell is dynamic query building — anywhere the model needed to assemble a query at runtime and reached for string assembly instead of placeholders or a query builder's parameter API.

### Insecure deserialization in parsing and messaging code

Generated parsing helpers and message consumers frequently deserialize untrusted input with an unsafe loader and no validation. In Python this shows up as `pickle.loads` or `yaml.load` (instead of `yaml.safe_load`) on data off a queue or an external call; in Java as native `ObjectInputStream` readObject on untrusted bytes. SAST catches some of this, but coverage is context-dependent, so it's worth your eye on any generated code that turns bytes from outside your trust boundary into objects.

### Sensitive data in responses and logs

Two service-shaped leaks the model produces without noticing:
- **Over-broad serializers** — a generated response serializer that returns the whole model, including `password_hash`, internal flags, or another tenant's fields, because the model serialized what was convenient rather than what the caller should see.
- **Secrets in structured logs** — a generated handler that logs the full request or a token at info level, which then lands in your log aggregation.

### What tooling already owns

Don't spend review time re-doing these by hand — confirm the pipeline flagged them:
- **Hardcoded secrets** — secret scanning and pre-commit hooks catch most of it.
- **Known-vulnerable or outdated dependencies** — SCA and an internal registry handle the known-CVE and version cases.

The one dependency issue worth your own glance is a **hallucinated or typosquatted package name** — a plausible-looking import the model invented or misspelled toward a malicious lookalike. It's a supply-chain vector scanners may miss because the package is new rather than known-bad, not because your tooling is weak.

## Part 3: The "What's Missing" Discipline

Your existing review reflex is tuned to find what's *wrong* — the malformed line, the off-by-one. AI-generated defects are more often what's *absent*: the check that should be there and isn't. That requires a different pass.

### Establish intent before reading lines

Before you read the handler line by line, decide what "right" looks like: what should this endpoint be allowed to do, and for whom? What result is correct, and what would make it unsafe? Reviewers who skip straight to reading catch typos and miss the code that does the wrong thing convincingly. You can't spot an absent authorization check if you haven't decided what the authorization rule should be.

This is the same principle as writing the test before you trust the implementation — you need the spec in your head to see where the code quietly diverges from it.

### Trace the untrusted input path

Follow each input from entry to use. At every sink — the query, the shell call, the deserialize, the downstream service call, the file path — confirm it's handled safely. In a generated handler this is a short, targeted trace, not a full re-read: entry point, into the service layer, into the query. You're checking the specific hops where the model tends to cut corners.

### Look for the absent check first

Ask the authorization question before the injection question, because it's the higher-leverage catch: does this code confirm the caller is allowed to do what it does, against *your* rule? Then check input validation, error handling, and output encoding as the next possible absences. The mental move is "what should be here that isn't," not only "what here is wrong."

### Verify parameterization by pattern, not by reading

You don't need to re-read every query. You need to know the exact patterns where models cut corners — the escape hatches from Part 2 — and search for them directly: `raw(`, `execute(`, `fmt.Sprintf` near a `Query`, `Statement` without `Prepared`. That's a targeted scan you can run in seconds per PR, which is what makes it survivable at volume.

## Part 4: Tests and Merge Decisions

### Don't count green

Generated tests tend to assert the happy path: the endpoint returns 200 for valid input. They skip the cases that define your actual risk surface, and worse, they often encode the *same* misunderstanding of intent the code does — so they pass while the logic is wrong. A passing suite is not evidence of safety or of correctness.

For a backend endpoint, the security cases the generated suite almost certainly skipped:
- **Another user's resource ID** — call with a valid token but someone else's `invoice_id`; the ownership check should reject it.
- **No token** — confirm the unauthenticated path is actually closed.
- **Wrong scope or tenant** — a token valid for a different role or tenant should not succeed.

Reason about what the tests check, not how many are green. Use the gaps to drive what you require before merge.

### Fast, consistent merge/block calls

At volume, you need decisions that don't require re-litigating each time. A workable default:

**Unconditional merge-stoppers:**
- **Missing or bypassable authorization** — an endpoint that authenticates but doesn't check ownership or scope.
- **Unparameterized query construction** — any user-influenced value assembled into a query by string interpolation.

**Blockers with a clear remediation path:**
- **Data exposure in responses or logs** — over-broad serializers, secrets or tokens in structured logs. Block, name the field, point at the fix.

**Fix-forward — don't hold the review:**
- **Overly broad error messages, suboptimal retry logic, style nits.** Real, but they don't gate the merge.

Drawing this line consistently is what keeps your review both fast and safe. The stoppers are exactly the classes where the tools are weakest and the blast radius is largest; the fix-forward items are where a later PR is fine.

[TAKEAWAYS]
- Fluent AI output suppresses the skepticism that surface-messy code triggers; at review volume, that suppression becomes a systematic gap, not an occasional one.
- Your highest-leverage catch is broken authorization — the authenticated-but-not-authorized endpoint — because it depends on your business rules and scanners structurally can't find it.
- Injection reappears through ORM escape hatches (`raw()`, `execute()`, `fmt.Sprintf` into a query, `Statement` concatenation); scan for those patterns directly rather than re-reading every line.
- Review by intent and absence: decide what the endpoint should be allowed to do, trace untrusted input to its sinks, and look first for the missing check, not the malformed one.
- Generated tests assert the happy path and encode the same intent errors as the code; require the ownership, no-token, and wrong-scope cases before merge.
- Treat missing/bypassable authorization and unparameterized queries as unconditional merge-stoppers; data exposure as a blocker with a fix; error messages and retry logic as fix-forward.
- Let secret scanning and SCA own hardcoded secrets and known-bad dependencies; keep your own eye only on hallucinated or typosquatted package names.
[/TAKEAWAYS]