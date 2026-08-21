Yes. With wheels now **officially added**, this is the updated Makad capability list, with each item defined at roughly the same level as the locomotion point:

1. **Makad will have a cute, expressive animated face on its screen.**
   The display will be its primary emotional interface: animated eyes, blinking, squinting, widening, looking around, sleeping/waking states, happiness, confusion, curiosity, annoyance, surprise, etc. The face should not just switch between static emoji-like images; it should continuously animate so Makad feels alive even while doing nothing.

2. **Makad will have natural, expressive head movement.**
   Its head will be able to turn, tilt and bob rather than remaining rigid. Movements should include looking toward people, small idle adjustments, nodding, tilting inquisitively, recoiling slightly, looking down/up, and subtle micro-motions. The goal is not simply “servo goes from 20° to 50°,” but motion profiles with acceleration/deceleration and coordinated timing that resemble an animated character.

3. **Makad will use its entire upper body for physical expression.**
   Expression will not be limited to the screen. Depending on the final mechanical design, the head/neck/body can lean, settle, bounce, recoil or shift slightly. For example, surprise might mean widened eyes + head jerk backward; curiosity might mean tilted eyes + tilted head + slight forward lean. The physical body therefore becomes part of the animation system.

4. **Makad will continuously listen for spoken interaction.**
   It will have microphones that allow it to detect when somebody is talking to it and capture speech clearly enough for processing. The eventual system should distinguish between idle environmental sound and intentional interaction rather than requiring keyboard/buttons for normal use.

5. **Makad will understand spoken language with low latency.**
   Speech will be converted to text quickly enough that conversations do not feel like “speak → wait ten seconds → robot responds.” The pipeline will be optimized around responsiveness, including speech detection, streaming/fast STT where appropriate, and interruption/turn-taking behavior.

6. **Makad will hold natural voice conversations.**
   Once it understands what was said, it will generate a response and speak it aloud. The objective is a lightweight companion-style conversation rather than a robot that only understands fixed commands such as “move left” or “tell weather.” Its conversational system should preserve enough context for short natural interactions.

7. **Makad will communicate with non-verbal robot/pet sounds as well as speech.**
   It will have a library/system for chirps, whistles, beeps, trills and other R2-D2/pet-like noises. These will be used for acknowledgement, curiosity, excitement, confusion, boredom, waking up, noticing someone, etc. Sometimes Makad should respond with a sound and motion rather than unnecessarily speaking a full sentence.

8. **Makad will see its surroundings through a camera.**
   The camera will not merely exist for demonstration. Makad will process its visual input and use it as part of its behaviour. At minimum this means understanding whether a person is present and roughly where relevant things are in its field of view.

9. **Makad will detect and visually track people/faces.**
   If someone moves from the left side of the room to the right, Makad should be capable of keeping attention on them using its eyes, head and—where appropriate—its mobile base. This creates the sensation that Makad is actually looking at you rather than simply having a camera mounted on it.

10. **Makad will have useful basic visual understanding beyond face tracking.**
    The CV system should be capable of recognising basic objects or scene information whenever required by its behaviours or utility functions. We are **not** trying to turn Makad into a giant VLM research project; perception exists so the robot can understand enough of its immediate environment to behave intelligently.

11. **Makad will react to people entering, leaving and interacting with its space.**
    Its behaviour should be event-driven. Someone approaches → Makad notices them. Someone calls it → it turns toward the source/person. Someone leaves → it can watch them go and eventually return to idle behaviour. Presence itself therefore becomes an input to the character rather than interaction beginning only after a command.

12. **Makad will have autonomous idle behaviour so it feels alive when nobody is controlling it.**
    It should never resemble a powered-off device merely because nobody is speaking. While idle it can blink, glance around, move its head slightly, make occasional noises, inspect something, reposition itself, become “sleepy,” wake when activity occurs, etc. These behaviours will be governed by a small behaviour/state system rather than purely random servo movements.

13. **Makad will coordinate its face, head, body, sound and movement into unified emotions/actions.**
    This is one of the most important software pieces. “Happy” should not independently trigger a happy face, random chirp and unrelated servo movement. A behaviour controller should orchestrate them together: eyes change → head perks up → body rolls forward slightly → chirp plays → animation settles. This coordination is what makes Makad feel like one creature instead of several demos bolted together.

14. **Makad will have a small utility interface on its display in addition to the animated face.**
    The screen can temporarily transition away from the character face when useful—for example to show information, controls, status or another small GUI—then return to the character. The expressive face remains the default identity of the robot; we are not making Makad primarily into a touchscreen tablet.

15. **Makad will perform a limited set of genuinely useful desktop/companion-assistant tasks.**
    This exists so the robot is more than a character demonstration. Voice, vision and the GUI can expose a small group of useful functions. We have intentionally **not frozen the exact utility feature set yet**, because those functions should be selected later based on time and what strengthens the final project rather than bloating the robot now.

16. **Makad will move autonomously using a wheeled differential-drive base.**
    It will use **two independently powered, encoder-equipped wheels plus a passive caster**, so it remains mechanically stable and does not need self-balancing. The drive system will allow Makad to move forward/backward, turn in arcs and rotate almost in place. This will support behaviours such as approaching someone, following them slowly, turning its entire body toward them, backing away, roaming locally and repositioning itself.

17. **Makad will use locomotion itself as part of its personality.**
    The wheels are not being added simply so Makad can travel from coordinate A to coordinate B. Motion will become another expressive channel: excited little spins, hesitant forward movements, backing away when “startled,” tiny side-to-side motions, turning dramatically when called, rolling closer when curious, etc. Acceleration and braking will be deliberately smoothed, and the head can counter-move during starts/stops to create some of that BB-8-style physical character.

18. **Makad will avoid basic collisions while moving around.**
    It will have simple short-range environmental sensing—likely ToF/proximity-type sensing combined with its camera—so autonomous motion doesn't mean blindly driving into furniture. Version 1 does **not** require full SLAM. Makad should be able to detect something in front of it, stop, back away/turn and continue safely.

19. **Makad will use perception to control locomotion.**
    Vision and movement won't live as separate demonstrations. If Makad sees the person it is interacting with off to one side, it can turn toward them. If that person moves farther away, it may follow. If something blocks its path, it reacts. This closes the robotics loop of **sense → decide → act → observe again**.

20. **Makad will run all of these capabilities through one central behaviour system.**
    At any given instant, something must decide what Makad should actually be doing. The behaviour layer will arbitrate between conversation, person tracking, idle behaviour, emotional reactions, locomotion, obstacle avoidance, screen animation and sound. For example, obstacle avoidance must temporarily override “follow person,” while someone speaking should interrupt an idle animation. This is what turns all of our individual subsystems into **one autonomous robot**.

So the final high-level definition is now:

> **Makad is a small expressive mobile companion robot that can see and track people, hear and converse with them, communicate through speech and cute robot sounds, express emotion through its animated face and natural physical movements, autonomously behave when left alone, move around on a differential-drive wheeled base, avoid basic obstacles, approach/follow/orient toward people, and coordinate all of those capabilities through one integrated behaviour system.**

And importantly, we're still **not** adding arms, manipulation, walking legs, self-balancing, full-house SLAM/navigation, or the actual BB-8 spherical mechanism. Those would change the scope enormously.

**This 20-point list is the scope I'd use as our Makad master feature definition going forward.**
