"""Source-keyed, per-part BRep cache for head inspection checks."""

import hashlib
import io
import json
import os
import shutil
import tempfile
from pathlib import Path

from OCP.BinTools import BinTools
from OCP.TopoDS import TopoDS_Shape
from build123d import Compound

import layout_model


ROOT = Path(__file__).resolve().parent
CACHE = ROOT / ".cache"
SOURCES = (
    "layout_model.py", "details.py", "feetech.py", "layout_axes.py",
    "motion-envelope.json", "motion_envelope.py", "harness.py", "optics.py",
    "inspection_scene.py", "relief_worker.py",
)


def source_key(catalog=False, reliefs=True):
    digest = hashlib.sha256()
    for path in sorted([ROOT / name for name in SOURCES if (ROOT / name).exists()]
                       + list((ROOT / "purchased").rglob("*"))):
        if not path.is_file():
            continue
        digest.update(str(path.relative_to(ROOT)).encode())
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    digest.update(json.dumps({"catalog": catalog, "reliefs": reliefs}, sort_keys=True).encode())
    return digest.hexdigest()


def _encode(shape):
    stream = io.BytesIO()
    BinTools.Write_s(shape.wrapped, stream)
    return stream.getvalue()


def _decode(raw):
    topods = TopoDS_Shape()
    BinTools.Read_s(topods, io.BytesIO(raw))
    if topods.IsNull():
        raise ValueError("empty cached BRep")
    return Compound.cast(topods)


def _read(directory):
    manifest = json.loads((directory / "manifest.json").read_text())
    if manifest["key"] != directory.name:
        raise ValueError("cache key mismatch")
    parts = {}
    for index, item in enumerate(manifest["parts"]):
        shape = _decode((directory / f"{index:04d}.brep").read_bytes())
        shape = layout_model.tint(shape, item["name"], item["color"], item["alpha"])
        parts[item["name"]] = dict(shape=shape, frame=item["frame"],
                                   kind=item["kind"], owner=item["owner"],
                                   color=item["color"], alpha=item["alpha"])
    return parts


def load_parts(catalog=False, reliefs=True, *, bypass=False):
    """Load exact BReps, building once when source bytes or options change.

    A complete directory is published only after every shape and the manifest
    have been written. Corrupt or partial entries are rebuilt.
    """
    if bypass or os.environ.get("MAKAD_BYPASS_CAD_CACHE") == "1":
        return layout_model.build_parts(catalog=catalog, reliefs=reliefs)
    key = source_key(catalog, reliefs)
    directory = CACHE / key
    if directory.exists():
        try:
            return _read(directory)
        except (OSError, ValueError, RuntimeError, KeyError):
            shutil.rmtree(directory)
    parts = layout_model.build_parts(catalog=catalog, reliefs=reliefs)
    CACHE.mkdir(exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=key + ".", dir=CACHE))
    try:
        manifest = []
        for index, (name, item) in enumerate(parts.items()):
            (temporary / f"{index:04d}.brep").write_bytes(_encode(item["shape"]))
            manifest.append({"name": name, **{field: item[field] for field in
                                           ("frame", "kind", "owner", "color", "alpha")}})
        (temporary / "manifest.json").write_text(json.dumps({"key": key, "parts": manifest}))
        if not directory.exists():
            try:
                temporary.rename(directory)
            except OSError:
                if not directory.exists():
                    raise
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return parts


def load_meshes(catalog=False, reliefs=True, *, parts=None):
    """Return one 0.05 mm / 0.2 rad tessellation per cached part.

    The array archive is derived from the same source key as the BReps and is
    published atomically. Faces retain build123d's zero-based vertex indices.
    """
    import numpy as np

    if parts is None:
        parts = load_parts(catalog=catalog, reliefs=reliefs)
    directory = CACHE / source_key(catalog, reliefs)
    archive = directory / "meshes.npz"
    names = list(parts)
    if not archive.is_file():
        arrays = {}
        for index, item in enumerate(parts.values()):
            vertices, faces = item["shape"].tessellate(0.05, 0.2)
            arrays[f"v{index:04d}"] = np.asarray([tuple(v) for v in vertices], dtype=np.float64)
            arrays[f"f{index:04d}"] = np.asarray(faces, dtype=np.int32)
        with tempfile.NamedTemporaryFile(dir=directory, suffix=".npz", delete=False) as tmp:
            temporary = Path(tmp.name)
            np.savez(tmp, **arrays)
        try:
            os.replace(temporary, archive)
        finally:
            temporary.unlink(missing_ok=True)
    try:
        with np.load(archive, allow_pickle=False) as arrays:
            return {name: (arrays[f"v{index:04d}"], arrays[f"f{index:04d}"])
                    for index, name in enumerate(names)}
    except (OSError, ValueError, KeyError):
        archive.unlink(missing_ok=True)
        return load_meshes(catalog=catalog, reliefs=reliefs, parts=parts)
