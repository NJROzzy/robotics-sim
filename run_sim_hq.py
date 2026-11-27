import os
os.environ["MUJOCO_GL"] = "egl"   # use "osmesa" if EGL fails
import mujoco, imageio

xml = """
<mujoco>
  <visual>
    <global offwidth="1920" offheight="1080"/>
    <quality shadowsize="4096" offsamples="8"/>
    <headlight ambient=".4 .4 .4" diffuse=".6 .6 .6"/>
  </visual>
  <asset>
    <texture type="skybox" builtin="gradient" rgb1=".4 .6 .8" rgb2="0 0 0" width="512" height="3072"/>
    <texture name="grid" type="2d" builtin="checker" rgb1=".2 .3 .4" rgb2=".1 .2 .3" width="300" height="300"/>
    <material name="grid" texture="grid" texrepeat="6 6" reflectance=".25"/>
  </asset>
  <worldbody>
    <light pos="1 -1 4" dir="-.3 .3 -1" diffuse=".9 .9 .9" castshadow="true"/>
    <geom type="plane" size="3 3 .1" material="grid"/>
    <body pos="0 0 1.2">
      <freejoint/>
      <geom type="sphere" size=".12" rgba="1 .3 .2 1" solref="0.01 0.2"/>
    </body>
  </worldbody>
</mujoco>
"""
model = mujoco.MjModel.from_xml_string(xml)
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model, 1080, 1920)   # height, width

cam = mujoco.MjvCamera()
cam.distance, cam.azimuth, cam.elevation = 2.5, 135, -20
cam.lookat[:] = [0, 0, 0.4]

FPS = 60
frames = []
while data.time < 4:
    mujoco.mj_step(model, data)
    if len(frames) < data.time * FPS:
        renderer.update_scene(data, camera=cam)
        frames.append(renderer.render())

imageio.mimsave("ball_hq.mp4", frames, fps=FPS, quality=9)
print("saved ball_hq.mp4,", len(frames), "frames")
