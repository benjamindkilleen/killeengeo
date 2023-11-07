<div align="center">

# KilleenGeo

<a href="https://pepy.tech/project/killeengeo">
<img src="https://pepy.tech/badge/killeengeo/month" alt="Downloads" />
</a>
<a href="https://github.com/benjamindkilleen/killeengeo/releases/">
<img src="https://img.shields.io/github/release/benjamindkilleen/killeengeo.svg" alt="GitHub release" />
</a>
<a href="https://pypi.org/project/killeengeo/">
<img src="https://img.shields.io/pypi/v/killeengeo" alt="PyPI" />
</a>
<a href="http://killeengeo.readthedocs.io/?badge=latest">
<img src="https://readthedocs.org/projects/killeengeo/badge/?version=latest" alt="Documentation Status" />
</a>
<a href="https://github.com/psf/black">
<img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black" />
</a>

</div>

2D and 3D geometry in Python. This library was originally a part of the
[DeepDRR](https://github.com/arcadelab/deepdrr) package, but has been split out into its own package
for easier use in other projects. It contains a lot of custom implementations with no overarching
design philosophy, other than getting me through my PhD.

The naming conventions and general approach to coordinate transforms adheres to [this](https://benjamindkilleen/files/frame_transforms.pdf) tutorial.

It is written solely in Python, and so is not particularly fast. It is also not particularly
well-tested, so use at your own risk.

## Installation

```bash
pip install killeengeo
```

## Usage

```python
import killeengeo as kg

# Define some points in a world coordinate frame
a = kg.point(1, 2, 3) # a point in 3D
b = kg.point(4, 5, 6) # another point in 3D
v = kg.vector(7, 8, 9) # vector
l = kg.line(a, b) # line connecting a and b
pl = kg.plane(a, v) # plane containing a, b, and normal v
# Also supported: line segments, rays

# Define some coordinate frames
world_from_A = kg.FrameTransform.from_translation(a) # coordinate frame with origin at a 
world_from_B = kg.FrameTransform.from_translation(b) # coordinate frame with origin at b

# Transforms to obtain points in those frames
B_from_world = world_from_B.inverse() # transform from B to world
A_from_world = world_from_A.inverse() # transform to A from world

# Transform between the new frames
A_from_B = A_from_world @ world_from_B # transform to B from A

# Objects in the new frame
a_in_A = A_from_world @ a
v_in_A = A_from_world @ v
l_in_A = A_from_world @ l
pl_in_A = A_from_world @ pl
```

Most of the time `kg` objects can be treated like numpy arrays, and they are converted to the expected form.

```python

import numpy as np

points = np.array([a, b]) # [2, 3] array where each row is a point
B2A = np.array(A_from_B) # [4, 4] array representing the transform from B to A
```

Above is the only use of the `X2Y` naming convention for frame transformations present here. For more information on why this variable naming convention is awful, see [this](https://benjamindkilleen/files/frame_transforms.pdf) tutorial.

## Documentation

Documentation is (maybe) available at [killeengeo.readthedocs.io](https://killeengeo.readthedocs.io/en/latest/).
