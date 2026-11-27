import os
os.environ["MUJOCO_GL"] = "egl"
import mujoco, imageio

model = mujoco.MjModel.from_xml_path("mujoco_menagerie/franka_emika_panda/scene.xml")
model.vis.global_.offwidth = 1280
model.vis.global_.offheight = 720
data = mujoco.MjData(model)
mujoco.mj_resetDataKeyframe(model, data, 0)   # "home" pose
mujoco.mj_forward(model, data)

renderer = mujoco.Renderer(model, 720, 1280)
cam = mujoco.MjvCamera()
cam.distance, cam.azimuth, cam.elevation = 2.0, 130, -20
cam.lookat[:] = [0, 0, 0.4]

renderer.update_scene(data, camera=cam)
imageio.imwrite("panda.png", renderer.render())
print("joints:", model.njnt, "| actuators:", model.nu)
renderer.close()
