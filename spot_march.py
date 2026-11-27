import time, math, numpy as np, mujoco, mujoco.viewer

model = mujoco.MjModel.from_xml_path("mujoco_menagerie/boston_dynamics_spot/scene.xml")
data = mujoco.MjData(model)
mujoco.mj_resetDataKeyframe(model, data, 0)
home = data.ctrl.copy()
print("home targets:", [round(float(c), 2) for c in home])

names = [mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, i) for i in range(model.nu)]
idx = {n: i for i, n in enumerate(names)}
PAIR_A, PAIR_B = ("fl", "hr"), ("fr", "hl")      # diagonal pairs move together

FREQ = 1.5          # steps per second
HIP_LIFT = 0.30     # extra hip flexion when a leg lifts (rad)
KNEE_LIFT = -0.50   # extra knee bend when a leg lifts (rad)

lo, hi = model.actuator_ctrlrange[:, 0], model.actuator_ctrlrange[:, 1]

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        ctrl = home.copy()
        phase = 2 * math.pi * FREQ * data.time
        for pair, shift in ((PAIR_A, 0.0), (PAIR_B, math.pi)):
            lift = max(math.sin(phase + shift), 0.0)      # only lift for half the cycle
            for leg in pair:
                ctrl[idx[f"{leg}_hy"]] += HIP_LIFT * lift
                ctrl[idx[f"{leg}_kn"]] += KNEE_LIFT * lift
        data.ctrl[:] = np.clip(ctrl, lo, hi)
        mujoco.mj_step(model, data)
        viewer.sync()
        time.sleep(model.opt.timestep)