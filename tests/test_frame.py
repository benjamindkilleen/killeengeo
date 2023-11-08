import numpy as np
import killeengeo as kg
import pyvista as pv
import matplotlib.pyplot as plt
from pytransform3d.transformations import plot_transform
from pytransform3d.plot_utils import make_3d_axis


a = kg.point(1, 2, 3)
b = kg.point(4, 5, 6)

world_from_A = kg.FrameTransform.from_pd(a, b - a)
world_from_B = kg.FrameTransform.from_rt(rotation=world_from_A.R, translation=b)

ax = make_3d_axis(ax_s=200, unit="m", n_ticks=6)
plot_transform(A2B=np.array(world_from_A), ax=ax, s=0.5, name="A")
plot_transform(A2B=np.array(world_from_B), ax=ax, s=0.5, name="B")
plt.show()
