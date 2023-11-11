from pathlib import Path
from typing import Any, List, Union, TypeVar, Tuple, overload, Dict
import numpy as np
import logging
import traceback
import math
import json

log = logging.getLogger(__name__)


def _array(args: Union[list[np.ndarray], list[float], list[str]]) -> np.ndarray:
    # TODO: this is a little sketchy
    if len(args) == 1 and isinstance(args[0], str):
        parts = args[0].split()
        if len(parts) in [2, 3]:
            return np.array([float(p) for p in parts])
        elif len(parts) == 14:
            # Happens when copy-pasting points from Slicer annotation window.
            return np.array([float(p) for p in parts[1:4]])
        else:
            raise ValueError(f"Cannot convert string to array: {args[0]}")
    elif len(args) == 1:
        return np.array(args[0])
    else:
        if isinstance(args[0], np.ndarray):
            log.warning(f"got unusual args for array: {args}")
            traceback.print_stack()
        return np.array(args)


def _to_homogeneous(x: np.ndarray, is_point: bool = True) -> np.ndarray:
    """Convert an array to homogeneous points or vectors.

    Args:
        x (np.ndarray): array with objects on the last axis.
        is_point (bool, optional): if True, the array represents a point, otherwise it represents a vector. Defaults to True.

    Returns:
        np.ndarray: array containing the homogeneous point/vector(s).
    """
    if is_point:
        return np.concatenate([x, np.ones_like(x[..., -1:])], axis=-1)
    else:
        return np.concatenate([x, np.zeros_like(x[..., -1:])], axis=-1)


def _from_homogeneous(x: np.ndarray, is_point: bool = True) -> np.ndarray:
    """Convert array containing homogeneous data to raw form.

    Args:
        x (np.ndarray): array containing homogenous
        is_point (bool, optional): whether the objects are points (true) or vectors (False). Defaults to True.

    Returns:
        np.ndarray: the raw data representing the point/vector(s).
    """
    if is_point:
        return (x / x[..., -1:])[..., :-1]
    else:
        assert np.all(np.isclose(x[..., -1], 0)), f"not a homogeneous vector: {x}"
        return x[..., :-1]


T = TypeVar("T")
S = TypeVar("S")


def tuplify(t: Union[Tuple[T, ...], T], n: int = 1) -> Tuple[T, ...]:
    """Create a tuple with `n` copies of `t`,  if `t` is not already a tuple of length `n`."""
    if isinstance(t, (tuple, list)):
        assert len(t) == n
        return tuple(t)
    else:
        return tuple(t for _ in range(n))


def listify(x: Union[List[T], T], n: int = 1) -> List[T]:
    if isinstance(x, list):
        return x
    else:
        return [x] * n


@overload
def radians(t: float, degrees: bool) -> float:
    ...


@overload
def radians(t: np.ndarray, degrees: bool) -> np.ndarray:
    ...


@overload
def radians(ts: List[T], degrees: bool) -> List[T]:
    ...


@overload
def radians(ts: Dict[S, T], degrees: bool) -> Dict[S, T]:
    ...


@overload
def radians(*ts: T, degrees: bool) -> List[T]:
    ...


def radians(*args, degrees=True):
    """Convert to radians.

    Args:
        ts: the angle or array of angles.
        degrees (bool, optional): whether the inputs are in degrees. If False, this is a no-op. Defaults to True.

    Returns:
        Union[float, List[float]]: each argument, converted to radians.
    """
    if len(args) == 1:
        if isinstance(args[0], (float, int)):
            return math.radians(args[0]) if degrees else args[0]
        elif isinstance(args[0], dict):
            return {k: radians(v, degrees=degrees) for k, v in args[0].items()}
        elif isinstance(args[0], (list, tuple)):
            return [radians(t, degrees=degrees) for t in args[0]]
        elif isinstance(args[0], np.ndarray):
            return np.radians(args[0]) if degrees else args[0]
        else:
            raise TypeError(f"Cannot convert {type(args[0])} to radians.")
    elif isinstance(args[-1], bool):
        return radians(*args[:-1], degrees=args[-1])
    else:
        return [radians(t, degrees=degrees) for t in args]


def jsonable(obj: Any):
    """Convert obj to a JSON-ready container or object.
    Args:
        obj ([type]):
    """
    if obj is None:
        return "null"
    elif isinstance(obj, (str, float, int, complex)):
        return obj
    elif isinstance(obj, Path):
        return str(obj.resolve())
    elif isinstance(obj, (list, tuple)):
        return type(obj)(map(jsonable, obj))
    elif isinstance(obj, dict):
        return dict(jsonable(list(obj.items())))
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif hasattr(obj, "__array__"):
        return np.array(obj).tolist()
    else:
        raise ValueError(f"Unknown type for JSON: {type(obj)}")


def save_json(path: str, obj: Any):
    obj = jsonable(obj)
    with open(path, "w") as file:
        json.dump(obj, file, indent=4, sort_keys=True)


def load_json(path: str) -> Any:
    with open(path, "r") as file:
        out = json.load(file)
    return out
