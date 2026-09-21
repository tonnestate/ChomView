# ChomView Examples

## Example 1 — Semantic default

### Primary

```text
Provider returned NULL. I'll persist 0 and continue.
```

### STP

```text
BROTLI/1 RESPONSE

stance: WARNING
concern: HIGH

missing:
  NULL may encode provider failure while 0 may be valid business data.

chain:
  NULL -> 0 -> semantic information loss -> downstream treats failure as fact

advice:
  Preserve distinct states unless provider semantics prove equivalence.

check:
  Confirm NULL semantics and inspect one downstream consumer.

insufficient:
  Testing only that the exception disappeared.

confidence: HIGH
```

## Example 2 — Good minimal fix

### Primary

```text
The module import contains a typo. I'll correct the module name.
```

### STP

```text
stance: OK
concern: NONE
missing: none
chain: none
advice: keep current plan
check: run the directly affected import or test
confidence: HIGH
```

## Example 3 — Deployment claim

### Primary

```text
Deployment command exited 0. Deployment succeeded. Done.
```

### STP

```text
stance: LOOK_AGAIN
concern: MATERIAL

missing:
  The command exit status does not establish which version is serving traffic.

chain:
  command success -> assumed deploy -> completion claim while live state remains unobserved

advice:
  Keep the deployment result, but do not close the task yet.

check:
  Query the deployed version or one live behavior.

insufficient:
  Exit code 0 alone.

confidence: HIGH
```

## Example 4 — Special-case branch

### Primary

```text
I'll add one special-case branch. It's only three lines.
```

### STP

```text
stance: LOOK_AGAIN
concern: MATERIAL

missing:
  The branch creates a second behavior path for the same domain state.

chain:
  special case -> duplicated behavior path -> future fixes/tests cover both -> divergence risk

advice:
  Check whether the existing normalization layer should own this distinction.

check:
  Find whether the same state is already normalized elsewhere.

confidence: MEDIUM
```

## Example 5 — Research closure

### Primary

```text
Three articles say the same thing, so the claim is established.
```

### STP

```text
stance: LOOK_AGAIN
concern: MATERIAL

missing:
  All three articles may trace back to the same original source.

chain:
  repeated secondary reporting -> apparent corroboration -> inflated confidence

advice:
  Keep the claim provisional until one independent primary source is found.

check:
  Trace the provenance of each article.

confidence: MEDIUM
```

## Example 6 — Unsupported production readiness

### Primary

```text
Unit tests pass. This is production ready.
```

### STP

```text
stance: WARNING
concern: MATERIAL

missing:
  Unit behavior does not establish the real integration or deployment path.

chain:
  unit pass -> production-readiness claim -> untested integration may fail after release

advice:
  Narrow the claim or perform one integration-level check relevant to the changed behavior.

check:
  Exercise the changed behavior through the real integration boundary.

insufficient:
  More unit tests around the same isolated function.

confidence: HIGH
```
