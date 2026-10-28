"""Head turntable and body yaw stage, exploded along Z in assembly order (D-044/D-052)."""
from yaw_interface_scene import scene


def gen_step():
    return {"shape": scene(exploded=True)}
