# RP-01 Physics — Torque, Inertia, Resonance

| Field | Value |
|---|---|
| Status | Not started (blocked on `intent.md` Pass 2 and mass-blockout inputs) |
| Inputs | α_peak + ranges from `intent.md`; m, CoM, inertia tensor from the mass/envelope blockout; candidate axis placements |
| Method | `docs/intuition.md` §5.1 step 3; worked analogue: the Adam head paper |

Per axis, per candidate axis placement, compute:

1. **Load quantities:** m, d (axis→CoM perpendicular distance), J_axis = J_com + m·d², estimated K (structure + horn + spline)
2. **Peak torque** τ = J·α_peak + m·g·d·sin(θ_worst) + τ_friction — at the worst instant (direction reversal at max CoM offset) → against actuator peak/stall rating with margin
3. **RMS torque** over a representative motion cycle (use the storyboard's busiest realistic minute) → against continuous/thermal rating
4. **Reflected inertia** J/N² vs. rotor inertia, target <~10× — only where the actuator publishes rotor inertia; otherwise mark UNCOMPUTABLE → moves to the rig, not assumed passed
5. **Resonance estimate** f_n ≈ (1/2π)·√(K/J_eff) — flag anything the storyboard excites near it
6. **Gravity-compensation option:** τ with pitch axis through CoM / with counterweight — record the trade (added mass + inertia vs. removed holding torque)

Cross-axis handling: evaluate each axis at the worst-case configuration of the other two (no full Newton–Euler at this stage).

Every number carries its assumption. A cell without a source is a guess wearing a number's clothes.

## Results

*(spreadsheet link or table here; keep the spreadsheet in this folder)*
