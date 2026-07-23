# Solution Report: Vanguard Call Center Quantum Optimization

## Executive Summary

This project proposes a hybrid quantum-classical optimizer for call center workforce
planning. The system forecasts hourly call volume, estimates required agents, converts
staffing choices into a QUBO-style decision model, and validates the schedule using a
simulation.

## Business Objective

Minimize operating cost while maintaining service levels for Vanguard clients.

## Optimization Target

```text
Minimize staffing cost
+ understaffing penalty
+ overstaffing penalty
+ service-level risk penalty
```

## Quantum Optimization Fit

Call center staffing is combinatorial because each hour can have many possible staffing
levels. Across many queues, skills, geographies, and shifts, the search space grows very
quickly. QUBO and QAOA are suitable because staffing selections can be encoded as binary
variables.

## Recommended Pilot

Start with one service queue, one region, and hourly planning. After validation, extend
to multi-skill routing, agent shift preferences, and real-time re-optimization.
