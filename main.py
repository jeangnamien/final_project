from PIL import Image
import math
import argparse

def calculate_hexagon_grid(image_width, image_height, hex_per_row):
    hexagon_size = image_width / (hex_per_row * 1.5 + 0.5)
    hexagon_width = hexagon_size * 2
    hexagon_height = math.sqrt(3) * hexagon_size

    num_hexagons_x = int(image_width / (hexagon_width * 0.75)) + 1
    num_hexagons_y = int(image_height / hexagon_height) + 1
    
    h_space = hexagon_size * 1.5
    v_space = hexagon_height
    
    return num_hexagons_x, num_hexagons_y, hexagon_width, hexagon_height, h_space, v_space, hexagon_size

def create_hexagon_points(center_x, center_y, hexagon_size):
    points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.radians(angle_deg)
        x = center_x + hexagon_size * math.cos(angle_rad)
        y = center_y + hexagon_size * math.sin(angle_rad)
        points.append((x, y))
    return points

def get_hexagon_center(row, col, h_space, v_space, hexagon_size):
    x = float(col * h_space + hexagon_size)
    y = float(row * v_space + hexagon_size)
    if col % 2 == 1:
        y += v_space / 2
    return (x, y)

def get_hexagon_color(image, center_x, center_y, hexagon_size, sample_size=10):
    pixels = image.load()
    width, height = image.size
    total_color = [0, 0, 0]
    count = 0
    for dx in range(-sample_size, sample_size + 1):
        for dy in range(-sample_size, sample_size + 1):
            x = min(max(int(center_x + dx), 0), width - 1)
            y = min(max(int(center_y + dy), 0), height - 1)
            distance = math.sqrt(dx**2 + dy**2)
            if distance <= hexagon_size:
                r, g, b = pixels[x, y][:3]
                total_color[0] += r
                total_color[1] += g
                total_color[2] += b
                count += 1
    if count == 0:
        return (255, 255, 255)
    avg_color = tuple(c // count for c in total_color)
    return avg_color

def generate_svg(image, output_file_name="output.svg", hex_per_row=100, stroke_width=0):
    image_width, image_height = image.size
    (num_hexagons_x, num_hexagons_y, hexagon_width, hexagon_height, 
     h_space, v_space, hexagon_size) = calculate_hexagon_grid(image_width, image_height, hex_per_row)
    
    svg_content = []
    svg_content.append(f'<svg width="{image_width}" height="{image_height}" viewBox="0 0 {image_width} {image_height}" xmlns="http://www.w3.org/2000/svg">')
    
    for row in range(num_hexagons_y):
        for col in range(num_hexagons_x):
            center_x, center_y = get_hexagon_center(row, col, h_space, v_space, hexagon_size)
            
            # skip if completely out of bounds (rare)
            if center_x + hexagon_size < 0 or center_x - hexagon_size > image_width:
                continue
            if center_y + hexagon_size < 0 or center_y - hexagon_size > image_height:
                continue
            
            points = create_hexagon_points(center_x, center_y, hexagon_size)
            points_str = " ".join(f"{round(x,2)},{round(y,2)}" for x, y in points)
            color = get_hexagon_color(image, center_x, center_y, hexagon_size)
            color_str = f"rgb({color[0]},{color[1]},{color[2]})"
            
            svg_content.append(f'<polygon points="{points_str}" fill="{color_str}" stroke="none" stroke-width="{stroke_width}"/>')
    
    svg_content.append('</svg>')
    
    try:
        with open(output_file_name, 'w') as f:
            f.write("\n".join(svg_content))
        print(f"✅ Successfully wrote SVG to {output_file_name}")
    except Exception as e:
        print(f"❌ Error writing SVG file: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Convert PNG to hexagon-based SVG")
    parser.add_argument("--input", type=str, default="file.png", help="Input PNG file")
    parser.add_argument("--output", type=str, default="output.svg", help="Output SVG file")
    parser.add_argument("--hex_per_row", type=int, default=100, help="Number of hexagons per row")
    args = parser.parse_args()
    
    try:
        image = Image.open(args.input).convert("RGB")
        print(f"📷 Image '{args.input}' loaded successfully. Size: {image.size}")
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return

    try:
        generate_svg(image, output_file_name=args.output, hex_per_row=args.hex_per_row)
        print("🎨 SVG generation completed.")
    except Exception as e:
        print(f"❌ Error generating SVG: {e}")

if __name__ == "__main__":
    main()
