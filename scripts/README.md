# Scripts

## Fog icon generator

`generate_fog_icon.py` generates fog/dust-cloud animations for the LED matrix weather icons. It simulates **multiple soft clouds** that appear, drift slightly, **merge** where they overlap, and disappear. Output is written in the `.icon.toml` format used by the app.

- **Smooth playback:** Frame-to-frame change is limited (no sudden jumps).
- **Seamless loop:** Extra transition frames step the last frame back toward the first so the cycle has no visible jump.

### Run

From the project root:

```bash
python scripts/generate_fog_icon.py
```

This overwrites `src/assets/weather/fog_light.icon.toml` with the default (16×8, 60 frames, 1 fps).

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--output`, `-o` | `src/assets/weather/fog_light.icon.toml` | Output path |
| `--preset` | (none) | `light` \| `moderate` \| `severe` — cloud count, size, and density |
| `--fps` | 1.0 | FPS in the generated config |
| `--frames` | 80 | Number of main animation frames (before loop transition) |
| `--width` | 16 | Grid width |
| `--height` | 8 | Grid height |
| `--no-smooth` | off | Disable per-cell smooth constraint (may cause jumps) |
| `--transition-max` | 40 | Max frames used to step last frame → first for loop |

### Generate all three fog icons

From the project root:

```bash
python scripts/generate_fog_icon.py --preset light   -o src/assets/weather/fog_light.icon.toml --frames 60
python scripts/generate_fog_icon.py --preset moderate -o src/assets/weather/fog_moderate.icon.toml --frames 70
python scripts/generate_fog_icon.py --preset severe   -o src/assets/weather/fog_severe.icon.toml --frames 80
```

- **Light:** fewer, smaller clouds (3 clouds, radius 1.6–2.8).
- **Moderate:** medium density (5 clouds, radius 2.2–3.5).
- **Severe:** more, larger clouds and denser quantization (6 clouds, radius 2.5–4.0).

To tweak density beyond presets, edit `NUM_CLOUDS`, `CLOUD_RADIUS_*`, and `density_to_level()` / `density_to_level_severe()` in `generate_fog_icon.py`.
