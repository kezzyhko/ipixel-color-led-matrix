#!/usr/bin/env python3
"""
Generate fog/dust-cloud icon animations for .icon.toml format.

Simulates multiple soft clouds that appear, drift slightly, merge where they
overlap, and disappear. Uses smooth frame-to-frame constraints so there are
no sudden jumps. Output is written as [configuration], [palette], [[frames]].

Usage:
  python scripts/generate_fog_icon.py [--output path] [--fps N] [--frames N] [--width W] [--height H]
  Default output: src/assets/weather/fog_light.icon.toml

  For a denser "moderate" fog, use more clouds and/or larger radius, e.g.:
  python scripts/generate_fog_icon.py -o src/assets/weather/fog_moderate.icon.toml --frames 80
  (Edit NUM_CLOUDS / CLOUD_RADIUS_* in script for density.)
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

# Grid and palette
WIDTH = 16
HEIGHT = 8
CHARS = (" ", "-", "+", "=")  # 0=empty, 1=light, 2=mid, 3=dense

# Cloud simulation
NUM_CLOUDS = 5
CLOUD_RADIUS_MIN = 2.0
CLOUD_RADIUS_MAX = 3.5
RADIUS_START_FRAC = 0.35   # cloud starts at this fraction of full radius, then grows
APPEAR_FRAMES = 10   # frames to go small -> full size and 0 -> 1 intensity
STABLE_FRAMES = 6    # frames at full before starting to disappear
DISAPPEAR_FRAMES = 10
DRIFT_PER_FRAME = 0.18   # drift so clouds move enough to merge and separate
DRIFT_WIGGLE = 0.04     # random nudge per frame for less linear motion
TOTAL_FRAMES = 80

# Smoothness: max change in density level (0-3) per cell per frame
MAX_LEVEL_CHANGE_PER_FRAME = 1

# Irregular shading within each blob (in blob-local coords so it moves with the blob)
BLOB_NOISE_AMOUNT = 0.38   # multiplier variation: 1 ± this within blob


def blob_local_noise(dx: float, dy: float) -> float:
    """Noise in blob-local (dx, dy). Same offset from center = same shade; moves with blob."""
    t = (
        math.sin(dx * 1.31 + dy * 1.97) * 0.5
        + math.sin(dx * 2.71 - dy * 1.41) * 0.35
        + math.sin((dx + dy) * 1.11) * 0.35
    )
    return max(-1.0, min(1.0, t)) * BLOB_NOISE_AMOUNT


def soft_blob_value(dx: float, dy: float, radius: float) -> float:
    """Contribution of a blob at (0,0) to a cell at (dx, dy). 0 outside radius."""
    d = math.hypot(dx, dy)
    if d >= radius:
        return 0.0
    # Smooth falloff: 1 at center, 0 at radius
    return 1.0 - (d / radius) ** 1.5


class Cloud:
    def __init__(self, x: float, y: float, radius_max: float, start_frame: float):
        self.x = x
        self.y = y
        self.radius_max = radius_max
        self.start_frame = start_frame
        self.intensity = 0.0  # 0..1
        self.phase = "appearing"
        self._pick_velocity()

    def _pick_velocity(self) -> None:
        self.vx = (random.random() - 0.5) * 2 * DRIFT_PER_FRAME
        self.vy = (random.random() - 0.5) * 2 * DRIFT_PER_FRAME

    def _current_radius(self, frame: float) -> float:
        """Radius grows from small to full when appearing; full when stable; shrinks when disappearing."""
        if self.phase == "appearing":
            life = frame - self.start_frame
            t = min(1.0, life / APPEAR_FRAMES)
            return self.radius_max * (RADIUS_START_FRAC + (1.0 - RADIUS_START_FRAC) * t)
        if self.phase == "stable":
            return self.radius_max
        if self.phase == "disappearing":
            elapsed = frame - self._disappear_start
            t = min(1.0, elapsed / DISAPPEAR_FRAMES)
            return self.radius_max * (1.0 - t)
        return 0.0

    def respawn(self, frame: float) -> None:
        self.x = random.uniform(2, WIDTH - 3)
        self.y = random.uniform(1, HEIGHT - 2)
        self.start_frame = frame
        self.intensity = 0.0
        self.phase = "appearing"
        self._pick_velocity()

    def advance(self, frame: float) -> None:
        life = frame - self.start_frame
        if life < 0:
            return
        if self.phase == "appearing":
            self.intensity = min(1.0, life / APPEAR_FRAMES)
            if self.intensity >= 1.0:
                self.phase = "stable"
                self._stable_until = frame + STABLE_FRAMES
        elif self.phase == "stable":
            if frame >= self._stable_until:
                self.phase = "disappearing"
                self._disappear_start = frame
        elif self.phase == "disappearing":
            elapsed = frame - self._disappear_start
            self.intensity = max(0.0, 1.0 - elapsed / DISAPPEAR_FRAMES)
            if self.intensity <= 0.0:
                self.phase = "gone"
        # Drift (with small random wiggle so clouds don't move in straight lines)
        if self.phase != "gone":
            wx = (random.random() - 0.5) * 2 * DRIFT_WIGGLE
            wy = (random.random() - 0.5) * 2 * DRIFT_WIGGLE
            self.x = (self.x + self.vx + wx) % WIDTH
            self.y = (self.y + self.vy + wy) % HEIGHT

    def contribute(self, grid: list[list[float]], frame: float) -> None:
        if self.phase == "gone" or self.intensity <= 0:
            return
        r = self._current_radius(frame)
        if r <= 0:
            return
        for iy in range(HEIGHT):
            for ix in range(WIDTH):
                dx = ix - self.x
                dy = iy - self.y
                base = self.intensity * soft_blob_value(dx, dy, r)
                # Irregular shading: modulate by noise in blob-local coords (moves with blob)
                v = base * (1.0 + blob_local_noise(dx, dy))
                grid[iy][ix] = min(1.0, grid[iy][ix] + max(0.0, v))


def density_to_level(d: float) -> int:
    """Map density 0..1 to level 0, 1, 2, 3."""
    if d <= 0.02:
        return 0
    if d <= 0.28:
        return 1
    if d <= 0.55:
        return 2
    return 3


def density_to_level_severe(d: float) -> int:
    """Denser mapping: more cells become + and =."""
    if d <= 0.01:
        return 0
    if d <= 0.18:
        return 1
    if d <= 0.45:
        return 2
    return 3


def run_simulation(
    num_frames: int,
    num_clouds: int | None = None,
    radius_min: float | None = None,
    radius_max: float | None = None,
    dense_quantize: bool = False,
) -> list[list[list[int]]]:
    """Run cloud simulation: clouds start small, grow, merge/separate, respawn when gone. No empty frames."""
    num_clouds = num_clouds if num_clouds is not None else NUM_CLOUDS
    radius_min = radius_min if radius_min is not None else CLOUD_RADIUS_MIN
    radius_max = radius_max if radius_max is not None else CLOUD_RADIUS_MAX
    to_level = density_to_level_severe if dense_quantize else density_to_level

    random.seed(42)
    clouds: list[Cloud] = []
    # First 2–3 clouds start already visible (negative start_frame) so frame 0 is never empty
    n_initial = min(3, num_clouds)
    for i in range(num_clouds):
        x = random.uniform(2, WIDTH - 3)
        y = random.uniform(1, HEIGHT - 2)
        r = random.uniform(radius_min, radius_max)
        if i < n_initial:
            # Already in stable phase at frame 0
            start = -STABLE_FRAMES - (n_initial - i) * (APPEAR_FRAMES + 2)
        else:
            start = (i - n_initial) * 8 + random.randint(0, 4)
        clouds.append(Cloud(x, y, r, float(start)))

    raw_frames: list[list[list[int]]] = []
    for frame in range(num_frames):
        for c in clouds:
            c.advance(float(frame))
        # Respawn any gone clouds so a new one appears where one disappeared
        for c in clouds:
            if c.phase == "gone":
                c.respawn(float(frame))
        grid = [[0.0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        for c in clouds:
            c.contribute(grid, float(frame))
        levels = [
            [to_level(grid[iy][ix]) for ix in range(WIDTH)]
            for iy in range(HEIGHT)
        ]
        raw_frames.append(levels)
    return raw_frames


def smooth_frames(raw_frames: list[list[list[int]]]) -> list[list[list[int]]]:
    """Constrain frame-to-frame change so no cell jumps by more than MAX_LEVEL_CHANGE_PER_FRAME."""
    if not raw_frames:
        return raw_frames
    out: list[list[list[int]]] = [raw_frames[0]]
    for raw in raw_frames[1:]:
        prev = out[-1]
        new_frame = []
        for iy in range(HEIGHT):
            row = []
            for ix in range(WIDTH):
                p = prev[iy][ix]
                t = raw[iy][ix]
                delta = max(-MAX_LEVEL_CHANGE_PER_FRAME, min(MAX_LEVEL_CHANGE_PER_FRAME, t - p))
                row.append(max(0, min(3, p + delta)))
            new_frame.append(row)
        out.append(new_frame)
    return out


def transition_to_first(
    frames: list[list[list[int]]], max_steps: int = 50
) -> list[list[list[int]]]:
    """Append frames that step from last toward first with ±1 per cell per frame (smooth loop)."""
    if len(frames) < 2:
        return frames
    first = [row[:] for row in frames[0]]
    result = list(frames)
    current = [row[:] for row in frames[-1]]
    step = 0
    while step < max_steps:
        done = True
        next_grid = []
        for iy in range(HEIGHT):
            row = []
            for ix in range(WIDTH):
                c = current[iy][ix]
                f = first[iy][ix]
                if c != f:
                    done = False
                    delta = max(-MAX_LEVEL_CHANGE_PER_FRAME, min(MAX_LEVEL_CHANGE_PER_FRAME, f - c))
                    c = max(0, min(3, c + delta))
                row.append(c)
            next_grid.append(row)
        current = next_grid
        result.append(next_grid)
        if done:
            break
        step += 1
    return result


def level_grid_to_bitmap(grid: list[list[int]]) -> str:
    """Convert level grid to multiline string (space-padded to WIDTH)."""
    lines = []
    for row in grid:
        line = "".join(CHARS[lev] for lev in row)
        line = line.ljust(WIDTH)
        lines.append(line)
    return "\n".join(lines)


def write_toml(
    out_path: Path,
    frames: list[list[list[int]]],
    fps: float = 1.0,
    palette: dict[str, str] | None = None,
) -> None:
    if palette is None:
        palette = {
            "-": "#8a99a6",
            "+": "#6e7d8a",
            "=": "#343b42",
        }
    lines = [
        "[configuration]",
        f"fps = {fps}",
        "",
        "[palette]",
    ]
    for ch, color in palette.items():
        lines.append(f'"{ch}" = "{color}"')
    lines.append("")
    for grid in frames:
        lines.append("[[frames]]")
        lines.append('bitmap = """')
        lines.append(level_grid_to_bitmap(grid))
        lines.append('"""')
        lines.append("")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {len(frames)} frames to {out_path}")


def main() -> None:
    global WIDTH, HEIGHT, TOTAL_FRAMES
    p = argparse.ArgumentParser(description="Generate fog icon .icon.toml with smooth cloud animation")
    p.add_argument(
        "--output", "-o",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "src" / "assets" / "weather" / "fog_light.icon.toml",
        help="Output .icon.toml path",
    )
    p.add_argument("--fps", type=float, default=5.0, help="Frames per second in config")
    p.add_argument("--frames", type=int, default=TOTAL_FRAMES, help="Number of output frames")
    p.add_argument("--width", type=int, default=WIDTH, help="Grid width")
    p.add_argument("--height", type=int, default=HEIGHT, help="Grid height")
    p.add_argument("--no-smooth", action="store_true", help="Disable per-cell smooth constraint")
    p.add_argument("--transition-max", type=int, default=40, help="Max frames to step end->first for loop")
    p.add_argument(
        "--preset",
        choices=("light", "moderate", "severe"),
        default=None,
        help="Preset: light (fewer/smaller clouds), moderate (default), severe (more/larger, denser)",
    )
    args = p.parse_args()

    WIDTH = args.width
    HEIGHT = args.height
    TOTAL_FRAMES = args.frames

    num_clouds = None
    radius_min = None
    radius_max = None
    dense_quantize = False
    if args.preset == "light":
        num_clouds = 3
        radius_min = 1.6
        radius_max = 2.8
    elif args.preset == "moderate":
        num_clouds = 5
        radius_min = 2.2
        radius_max = 3.5
    elif args.preset == "severe":
        num_clouds = 6
        radius_min = 2.5
        radius_max = 4.0
        dense_quantize = True

    raw = run_simulation(
        TOTAL_FRAMES,
        num_clouds=num_clouds,
        radius_min=radius_min,
        radius_max=radius_max,
        dense_quantize=dense_quantize,
    )
    if args.no_smooth:
        frames = raw
    else:
        frames = smooth_frames(raw)
    frames = transition_to_first(frames, max_steps=args.transition_max)
    write_toml(args.output, frames, fps=args.fps)


if __name__ == "__main__":
    main()
