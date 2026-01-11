# LED matrix

## Quick start

### Conda
```
git clone https://github.com/kezzyhko/led-matrix
cd led-matrix
conda env create
conda activate led-matrix
python .\src\main.py -c example_config.cfg --debug
```

### Python

```
git clone https://github.com/kezzyhko/led-matrix
cd led-matrix
pip install -r requirements.txt
python .\src\main.py -c example_config.cfg --debug
```

## Honorable mentions

* `rpi-rgb-led-matrix-scene-composer`<br>
I relied on it as a guide in some parts of the code.<br>
Originally made by [@fredrikolis](https://github.com/fredrikolis). The original repo is gone, but you can find it on [PyPI](https://pypi.org/project/rpi-rgb-led-matrix-scene-composer/) or use [a reupload by @krruzic](https://github.com/krruzic/rpi-rgb-led-matrix-scene-composer).
