---
mode: solo
source: RP-01 layout-03 physics lock, beginner bottom-up
started: 2026-09-11
---

# Teaching: Make RP-01 head math/physics bulletproof

## Progress: 8/8 concepts confirmed

### 0. What "bulletproof" means here
- [x] Paper physics answers *class of solution*, not "this servo is frozen"
- [x] Every number has a source grade: W / D / E / U
- [x] Layout-03 D/E tree is usable for screening, not for actuator freeze

### 1. Frames, chain, distal membership
- [x] Three rigid bodies: R (rolls), P (pitches+yaws), Y (yaws only)
- [x] A joint carries everything distal to it: roll ⊂ pitch ⊂ yaw
- [x] Actuator housing often does *not* rotate about the axis it drives
- [x] Layout-03 trap: roll XC330 is P, pitch XC330 is Y

### 2. Per-part mass inventory
- [x] One owner per physical part; no double-count of envelopes vs allowances
- [x] Why CAD-volume × PLA 1.24 is E, not W (infill, finish, real modules)

### 3. Per-part CoM, then composite CoM
- [x] CoM is mass-weighted average, not geometric center
- [x] Composite CoM of a set = Σ(m·r) / Σm

### 4. An axis is a line; d is perpendicular distance
- [x] Roll = line along +X through (0, roll_y, roll_z)
- [x] Pitch = line along +Y through (pitch_x, 0, pitch_z)
- [x] Yaw = line along +Z through (pitch_x, 0, −60)
- [x] A0 means estimated CoM on that line at neutral, not "gravity is always zero"

### 5. Gravity torque (pitch and roll first)
- [x] τ_g = m g × lever of CoM about the axis; sign preserved
- [x] Perfect A0 ⇒ τ_g=0 at all single-axis angles; residuals and combined tilts are the real gravity cases
- [x] Yaw about vertical has no gravity restoring term at this approximation

### 6. Inertia about the axis (J_com + m d²)
- [x] Intrinsic (about own CoM) vs parallel-axis term
- [x] Current layout-03 J is box/diagonal E, not a measured tensor
- [x] Dynamic torque J·α using storyboard α; peak ≠ RMS

### 7. Combined load, friction/cable, then actuator envelope
- [x] Each axis at worst pose of the other two (cheap 3-DOF)
- [x] Peak vs continuous/RMS vs torque-speed at voltage; not stall at 0 rpm
- [x] Resonance / backlash / reflected inertia only after J exists

---
*Last updated: 2026-09-12T11:15+0530*
*Session complete: all checklist items confirmed.*
