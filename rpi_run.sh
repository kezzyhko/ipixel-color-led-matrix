LOG_DIR="$HOME/Desktop/logs"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d-%H-%M).log.txt"

cd "$HOME/Desktop/led-matrix"
conda activate led-matrix

mkdir -p "$LOG_DIR"
python ./src/main.py -c config.cfg | tee "$LOG_FILE"
