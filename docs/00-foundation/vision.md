# Makad V1 Vision

| Field | Value |
|---|---|
| Status | Approved |
| Version | 1.1 |
| Owner | Project builder |
| Last reviewed | 2026-08-14 |
| Decision authority | Approved by the project builder and recorded in `MEMORY.md` |

## Identity

**Makad**, technical designation **M4K4-D** and shortened to **M4**, is a personal droid.

M4 is intended to occupy the kind of role R2-D2 occupied for Luke Skywalker: a distinctive droid companion with recognizable behaviour, loyalty, presence, and personality. Makad should therefore be referred to as a **droid**, not primarily as a desktop assistant, smart speaker, or generic social robot.

## Product thesis

Makad's defining advantage is **expressiveness**. Expressiveness is not a decorative layer placed over mechanics; it emerges from what Makad understands, what it sees and hears, and how well it coordinates its display, physical motion, sound, and timing.

The top V1 priority is:

> **Makad should feel alive.**

General usefulness is secondary because utility features can be added through software later. The hardware and behaviour work should first establish the droid's presence.

## Intended experience

When a person encounters Makad, they should be able to read its attention and basic intent without an explanation. Makad should:

- have a recognizable character while idle;
- understand natural spoken interaction;
- notice and visually react to nearby people;
- express attention through its display and head/body orientation;
- use powered roll, pitch, and yaw head motion for readable three-axis attention and expression;
- use a controllable status light beside the head camera as an additional droid-like visual cue;
- communicate in its own authored astromech-style language;
- answer a small set of useful requests through its display and connected services;
- approach and follow its person on the floor when asked;
- coordinate perception, display animation, physical movement, audio, and timing as one character;
- move with deliberate anticipation, follow-through, and settling rather than like disconnected actuator tests;
- remain inspectable, repairable, and visibly built rather than pretending to be a sealed consumer appliance.

The best V1 demonstration is a coherent encounter with M4, not a tour through unrelated subsystem demonstrations.

## Character and visual direction

Makad's aesthetic direction is explicitly inspired by Star Wars droids, combined with cyberpunk, rugged, and somewhat scrappy construction. The desired appearance is:

- mechanical and unmistakably droid-like;
- compact enough to remain approachable, without optimizing for the smallest possible size;
- rugged, used, and characterful rather than glossy and appliance-like;
- visibly assembled, with screws, panels, seams, and service access contributing to the personality;
- subtly monkey-linked where silhouette or motion makes that useful, without becoming a literal animal robot.

The existing renders are starting references, not a frozen industrial design. Exact proportions, face geometry, ear forms, shell language, colours, finish, and component placement remain open to redesign.

## Expressive quality bar

The following combination should receive the highest quality effort in V1:

1. display expression;
2. physical head/body movement;
3. the timing and composition connecting perception, display, movement, and sound.

These channels must support the same perceived thought or intention. A polished isolated animation or mechanism is insufficient if the combined response feels incoherent.

## Companion tracking and following

Makad should be able to acquire a person's face, maintain attention as the person moves, approach when called, and follow them in a pet-like way. This is part of the approved Core companion experience.

This behaviour couples sustained visual tracking, person localization, locomotion, obstacle avoidance, following distance, reacquisition, and failure handling. Its difficulty is acknowledged as an engineering risk, but the risk does not demote it from Core. The system may use visual search or another later-selected localization method; Core does not require spatial audio.

Powered roll, pitch, and yaw are all part of the Core expressive-head requirement. The exact joint order, actuator, transmission, sensing, support, range, and control implementation remain engineering decisions, but V1 is not complete with a two-axis yaw/pitch head.

## Learning thesis

Makad is also an embodied-robotics learning project. V1 should require genuine integration across mechanical design, electronics, control, sensing, perception, embedded/software systems, and character behaviour.

Complexity is valuable only when it strengthens the intended droid experience or teaches something central to embodied robotics. Familiar software features should not displace the harder physical integration work merely because they are easier to add.

## Design principles

1. **Droid coherence over feature count.** A few convincing coordinated behaviours are more valuable than many disconnected capabilities.
2. **Understanding drives expression.** Visual and audio perception should give Makad something meaningful to react to.
3. **Character is a system property.** Display, sound, sensing, head motion, base motion, and timing should express the same intent.
4. **Hardware earns its place.** A mechanism or sensor must support the V1 experience, plausible hazards, or a named learning objective.
5. **Evidence before commitment.** Exploratory specs, renders, architectures, and components become decisions only through review and prototyping.
6. **Build for iteration.** Parts should be inspectable, replaceable, and practical to modify during the project.
7. **Failure remains bounded.** A sensing, controller, or service failure should not create uncontrolled motion or physical damage.

## Anti-vision

Makad V1 is not intended to be:

- a polished consumer product;
- a generic voice assistant with a robot shell;
- a collection of disconnected AI or hardware demonstrations;
- a design frozen around the current renders or exploratory specsheets;
- optimized for minimum size, minimum cost, or maximum feature count at the expense of M4's character.

No permanent list of all future exclusions is defined yet. Capabilities outside the approved V1 Core and Targets are simply uncommitted until there is a reason to evaluate them.

## Open implementation decisions

- [ ] Approve the final visual direction after a revised concept pass.
- [ ] Select and validate the three-axis roll/pitch/yaw head mechanism and motion-control approach.
- [ ] Select the technical approach for person localization, tracking, loss, and reacquisition.
- [ ] Define the detailed astromech vocabulary and grammar.

### Review notes

Approved by the project builder on 2026-08-14. Version 1.1 promotes powered roll into the Core three-axis head requirement. Open implementation decisions do not reopen the approved identity, priorities, or Core experience.
