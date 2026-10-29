# Improvement Changelog

| Stage       | What we tried and why                                                                                                                  | Evidence                                                        | Decision / Learning                                                                                                                      |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Baseline    | Implemented basic missing-value and duplicate-row checks to establish a deterministic starting point.                                  | `baseline/baseline.py` and baseline evaluation output           | Basic checks are useful but do not capture semantic or cross-column issues.                                                              |
| Iteration 1 | Added numeric outlier detection, date validity checks, category-alias detection, cross-column consistency checks, and quality scoring. | `evaluation/` cases and evaluation output                       | Broader deterministic coverage identifies more measurable quality issues without relying on AI for arithmetic.                           |
| Iteration 2 | Added a Research Agent for findings requiring semantic or contextual interpretation.                                                   | Representative files in `trajectories/`                         | AI is useful for interpreting ambiguous findings, but should not replace deterministic evidence.                                         |
| Iteration 3 | Added a skeptical Verification Agent to independently review research and findings.                                                    | Agent trajectory JSON and Agent Review output                   | A second review layer helps distinguish supported findings from ambiguous cases and reduces false-positive risk.                         |
| Final       | Combined deterministic analysis, targeted research, skeptical verification, and decision-ready reporting into one workflow.            | Final evaluation results, trajectory JSON, and application demo | The strongest design is an evidence-first workflow where agents interpret and verify rather than perform core data-quality calculations. |

## Main Failure Mode

A statistical outlier is not automatically a confirmed data-quality error. Unusual values may be legitimate business cases, so the system surfaces them for contextual review instead of automatically deleting or correcting them.

## Hot Take

The strongest agentic data-quality architecture is not the one that flags the most anomalies. It is the one that provides reliable deterministic evidence, researches only where useful, verifies ambiguous findings, and preserves uncertainty before a human makes an irreversible correction.
