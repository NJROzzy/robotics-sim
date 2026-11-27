import os
os.environ["MUJOCO_GL"] = "egl"   # use "osmesa" if EGL fails
import mujoco, imageio

xml = """
<mujoco>
  <worldbody>
    <light pos="0 0 3"/>
    <geom type="plane" size="2 2 .1" rgba=".8 .8 .8 1"/>
    <body pos="0 0 1">
      <freejoint/>
      <geom type="sphere" size=".1" rgba="1 .3 .3 1"/>
    </body>
  </worldbody>
</mujoco>
"""
model = mujoco.MjModel.from_xml_string(xml)
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model, 480, 640)

frames = []
while data.time < 3:
    mujoco.mj_step(model, data)
    if len(frames) < data.time * 30:      # 30 fps video
        renderer.update_scene(data)
        frames.append(renderer.render())

imageio.mimsave("ball.mp4", frames, fps=30)
print("saved ball.mp4")
