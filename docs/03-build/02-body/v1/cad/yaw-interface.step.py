"""Head turntable (translucent) seated on the body yaw stage (D-044/D-048/D-052)."""
from yaw_interface_scene import scene


def gen_step():
    return {"shape": scene(exploded=False)}
