from typing import List, Optional, overload
import numpy as np
import logging

from .core import Vector3D, vector, Point3D, point

log = logging.getLogger(__name__)


def _sample_spherical(d_phi: float, n: int) -> np.ndarray:
    """Sample n vectors within `phi` radians of [0, 0, 1]."""
    theta = np.random.uniform(0, 2 * np.pi, n)

    phi = np.arccos(np.random.uniform(np.cos(d_phi), 1, n))

    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)

    return np.stack([x, y, z], axis=1)


@overload
def spherical_uniform(center: Vector3D, d_phi: float, n: int) -> List[Vector3D]: ...


@overload
def spherical_uniform(center: Vector3D, d_phi: float, n: None) -> Vector3D: ...


def spherical_uniform(center=vector(0, 0, 1), d_phi=np.pi, n=None):
    """Sample unit vectors on the surface of the sphere within `d_phi` radians of `v`."""
    v = vector(center).hat()
    points = _sample_spherical(d_phi, 1 if n is None else n)
    F = v.rotfrom(vector(0, 0, 1))
    if n is None:
        return F @ vector(points[0])
    else:
        return [F @ vector(p) for p in points]


@overload
def clipped_spherical_uniform(
    center: Vector3D,
    max_alpha: float,
    max_beta: float,
    max_theta: float,
    n: int,
) -> List[Vector3D]: ...


@overload
def clipped_spherical_uniform(
    center: Vector3D,
    max_alpha: float,
    max_beta: float,
    max_theta: float,
    n: None,
) -> Vector3D: ...


def clipped_spherical_uniform(
    center,
    max_alpha,
    max_beta,
    max_theta,
    n=None,
):
    """Sample unit vectors on the surface of the sphere within the surface defined by the two angles radians of `center`.

    If the patient is HFS, this assumes the Z axis is anterior, the X axis is left, and the Y axis is inferior.

    Args:
        center (Point3D): The center of the sphere.
        max_alpha (float): Upper bound for angulation in the left/right direction in radians.
        max_beta (float): Upper bound for angulation in the cranial/caudal direction in radians.
        max_theta (float): Upper bound for angulation in the yaw, for lateral views.
        n (int): The number of points to sample.

    """

    _n = 1 if n is None else n

    d_phi = max(max_alpha, max_beta)
    out = []
    while len(out) < _n:
        ds = np.array(spherical_uniform(center, d_phi, _n))

        alphas = np.arctan2(ds[:, 0], ds[:, 2])
        betas = np.arctan2(ds[:, 1], ds[:, 2])
        thetas = np.arctan2(ds[:, 1], ds[:, 0])

        # Sample only the points that are within the bounds.
        mask = np.logical_and(
            np.abs(alphas) <= max_alpha,
            np.logical_or(np.abs(betas) <= max_beta, np.abs(thetas) <= max_theta),
        )
        out.extend([vector(d) for d in ds[mask]])

    if n is None:
        return out[0]
    else:
        return out[:_n]


@overload
def normal(
    center: Point3D, scale: float, radius: Optional[float], n: int
) -> List[Point3D]: ...


@overload
def normal(
    center: Point3D, scale: float, radius: Optional[float], n: None
) -> Point3D: ...


def normal(center=point(0, 0, 0), scale=1, radius=None, n=None):
    """Sample points from a clipped normal distribution.

    Args:
        center (Point3D): The center of the distribution.
        scale (float): The standard deviation of the distribution.
        radius (float): The radius of the distribution.
        n (int): The number of points to sample.

    Returns:
        Point3D: The sampled point or points, if n is not None.
    """
    c = point(center)

    n_ = 1 if n is None else n
    points = np.empty((0, 3))
    while len(points) < n_:
        log.debug(f"Sampling {n_ - len(points)} points: {points.shape}")

        new_points = np.random.normal(0, scale, (n_ - len(points), 3))
        if radius is not None:
            new_points = new_points[np.linalg.norm(new_points, axis=1) <= radius]
        points = np.concatenate([points, new_points], axis=0)

    if n is None:
        return c + vector(points[0])
    else:
        return [c + vector(p) for p in points]


@overload
def uniform(center: Point3D, radius: float, n: int) -> List[Point3D]: ...


@overload
def uniform(center: Point3D, radius: float, n: None) -> Point3D: ...


def uniform(center=point(0, 0, 0), radius=1, n=None):
    """Sample points from a uniform distribution, bounded by a sphere.

    Args:
        center (Point3D): The center of the distribution.
        radius (float): The radius of the distribution. Defaults to 1.
        n (int): The number of points to sample. Defaults to None.

    Returns:
        Point3D: The sampled point or points, if n is not None.
    """
    c = point(center)

    n_ = 1 if n is None else n
    points = np.empty((0, 3))
    while len(points) < n_:
        log.debug(f"Sampling {n_ - len(points)} points: {points.shape}")

        new_points = np.random.uniform(-radius, radius, (n_ - len(points), 3))
        if radius is not None:
            new_points = new_points[np.linalg.norm(new_points, axis=1) <= radius]
        points = np.concatenate([points, new_points], axis=0)

    if n is None:
        return c + vector(points[0])
    else:
        return [c + vector(p) for p in points]
