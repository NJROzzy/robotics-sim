import mujoco

model = mujoco.MjModel.from_xml_path("mujoco_menagerie/boston_dynamics_spot/scene.xml")
print("total mass (kg):", round(sum(model.body_mass), 1))
print("joints:", model.njnt, "| actuators:", model.nu, "| keyframes:", model.nkey)
print("\nactuators (name, control range):")
for i in range(model.nu):
    name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, i)
    lo, hi = model.actuator_ctrlrange[i]
    print(f"  {i:2d} {name:24s} [{lo:6.2f}, {hi:6.2f}]  kp={model.actuator_gainprm[i][0]:.0f}")
print("\nkeyframes:", [mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_KEY, k) for k in range(model.nkey)])