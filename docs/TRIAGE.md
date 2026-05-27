# Triage

## Taxonomy [Observed]

`claude-code-fleet-support` uses a one-tier support taxonomy:

- **bug** — a defect against the product's documented contract
- **not_bug** — a support question, design discussion, or feature request
- **spam** — off-topic, abusive, or promotional material

This matches the locked architecture spec §4.

## Worked Example: `@eddyb_omon` [Observed]

The example comment from the architecture process:

> "A 3-char regression is the easy save. The hard ones are when the diff reads valid against every gate and the bug ships anyway. What does fleet do when Grok says ALLOW?"

Classification:

- [Observed] `not_bug`
- [Observed] Reason: this is a design-question or governance-question about fleet behavior, not a report that `claude-code-fleet-support` violated its documented contract.
- [Observed] No bug lock should be opened from this input.

## Confidence Gating [Observed]

- [Observed] The architecture requires bug-lock creation only on high-confidence bug classification or explicit owner confirmation.
- [Unknown] The exact calibrated confidence threshold may move after real-event calibration, even though the architecture starts from `0.90`.

## Skeleton Status [Observed]

- [Observed] The actual classifier implementation is deferred to task `product-triage`.
- [Observed] Current runtime stubs raise `NotImplementedError` instead of fabricating classifications.
