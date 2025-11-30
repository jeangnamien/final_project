# PNG to SVG Hexagon Converter

Convert PNG images to scalable SVG wallpapers using hexagonal patterns.

## Installation
```bash
poetry install --no-root
```

## Usage
```bash
poetry run python main.py --input file.png --output file.svg --hex_per_row 100
```

## Parameters

- `--input`: Input PNG file
- `--output`: Output SVG file
- `--hex_per_row`: Number of hexagons per row (default: 100)

## Examples
```bash
# High resolution
poetry run python main.py --input file.png --output file.svg --hex_per_row 200

# Low resolution (faster)
poetry run python main.py --input file.png --output file.svg --hex_per_row 50
```

## Author

Jean Gnamien