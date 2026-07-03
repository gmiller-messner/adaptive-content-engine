---
title: "Part 2: What AI Reintroduces in Service Code"
layout: default
nav_order: 2
parent: "Reviewing AI-Generated Backend Code: The Failure Modes Your Review Muscle Misses"
grand_parent: Lessons
---

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

<div class="lesson-nav">
<a href="../part-1/" class="lesson-nav-prev">← Part 1: Why Fluent Code Disarms You</a><a href="../part-3/" class="lesson-nav-next">Part 3: The "What's Missing" Discipline →</a>
</div>

