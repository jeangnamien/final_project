import marimo

__generated_with = "0.18.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from PIL import Image
    import math
    from io import BytesIO
    return Image, math, mo


@app.cell
def _(mo):
    mo.md("""
    # 🎨 Hexagonal Wallpaper Generator
    """)
    return


@app.cell
def _(math):
    # Helper functions
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

    def generate_svg(image, hex_per_row=100, stroke_width=0):
        import math
        image_width, image_height = image.size

        hexagon_size = image_width / (hex_per_row * 1.5 + 0.5)
        hexagon_width = hexagon_size * 2
        hexagon_height = math.sqrt(3) * hexagon_size

        num_hexagons_x = int(image_width / (hexagon_width * 0.75)) + 1
        num_hexagons_y = int(image_height / hexagon_height) + 1

        h_space = hexagon_size * 1.5
        v_space = hexagon_height

        svg_content = []
        svg_content.append(f'<svg width="{image_width}" height="{image_height}" viewBox="0 0 {image_width} {image_height}" xmlns="http://www.w3.org/2000/svg">')

        for row in range(num_hexagons_y):
            for col in range(num_hexagons_x):
                center_x, center_y = get_hexagon_center(row, col, h_space, v_space, hexagon_size)

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
        return "\n".join(svg_content)

    return (generate_svg,)


@app.cell
def _(mo):
    # Input widgets
    uploaded_file = mo.ui.file(
        filetypes=[".png", ".jpg", ".jpeg"],
        label="📁 Upload an image",
        multiple=False
    )

    hex_per_row = mo.ui.slider(
        start=20, 
        stop=300, 
        step=10, 
        value=100,
        label="🔢 Hexagons per row"
    )

    stroke_width = mo.ui.slider(
        start=0,
        stop=2,
        step=0.1,
        value=0,
        label="✏️ Stroke width"
    )

    return hex_per_row, stroke_width, uploaded_file


@app.cell
def _(hex_per_row, mo, stroke_width, uploaded_file):
    mo.md(f"""
    ## ⚙️ Settings

    {uploaded_file}

    {hex_per_row}

    {stroke_width}
    """)
    return


@app.cell
def _(Image, generate_svg, hex_per_row, mo, stroke_width, uploaded_file):
    # Process image when uploaded
    if uploaded_file.value is not None and len(uploaded_file.value) > 0:
        try:
            import tempfile
            import os

            # Get the first uploaded file
            file_data = uploaded_file.value[0]

            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                tmp_file.write(file_data.contents)
                tmp_path = tmp_file.name

            # Open image from file
            image = Image.open(tmp_path).convert("RGB")

            # Generate SVG
            svg_content = generate_svg(
                image, 
                hex_per_row=hex_per_row.value,
                stroke_width=stroke_width.value
            )

            # Clean up temp file
            os.unlink(tmp_path)

            # Save to file
            output_path = "preview.svg"
            with open(output_path, 'w') as f:
                f.write(svg_content)

            result = mo.md(f"""
            ## ✅ Result Generated!

            **Image size:** {image.size[0]} × {image.size[1]} pixels

            **Hexagons per row:** {hex_per_row.value}

            **Total hexagons:** ~{int((image.size[0] / (hex_per_row.value * 1.5)) * (image.size[1] / (image.size[0] / hex_per_row.value)))}

            ### 🖼️ Preview

            {mo.Html(svg_content)}

            ---

            💾 Saved as `{output_path}`
            """)
        except Exception as e:
            import traceback
            result = mo.md(f"""
            ## ❌ Error

            ```
            {str(e)}

            {traceback.format_exc()}
            ```

            Please try uploading a different image.
            """)
    else:
        result = mo.md("""
        ## 👆 Get Started

        Upload an image above to convert it into a hexagonal SVG wallpaper!

        **Tips:**
        - Lower hexagons per row = faster processing, less detail
        - Higher hexagons per row = slower processing, more detail
        - Try values between 50-150 for best results
        """)

    result
    return


if __name__ == "__main__":
    app.run()
