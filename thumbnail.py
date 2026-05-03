import textwrap
from svgtopng import svg_to_png
def generate_thumbnail(title, output_filename="thumbnail_final.svg"):
    # 1. Conservative Layout Settings
    # These widths are calibrated for Arial Black to prevent robot overlap
    title=title.strip()
    MAX_LINES = 4
    length = len(title)
    
    if length < 12:
        font_size = 115
        wrap_width = 9   # Very few characters per line at this size
        line_height = 125
    elif length < 25:
        font_size = 95
        wrap_width = 12 
        line_height = 105
    elif length < 45:
        font_size = 75
        wrap_width = 16
        line_height = 85
    else:
        font_size = 60
        wrap_width = 22
        line_height = 70

    # 2. Text Wrapping
    wrapper = textwrap.TextWrapper(width=wrap_width, break_long_words=False)
    lines = wrapper.wrap(title)
    
    # Cap the lines to prevent vertical overflow
    if len(lines) > MAX_LINES:
        lines = lines[:MAX_LINES]
        lines[-1] += "..."

    # 3. Vertical Centering
    total_height = len(lines) * line_height
    start_y_offset = -(total_height / 2) + (line_height / 4)

    # 4. Generate SVG Text Block
    text_elements = []
    for line in lines:
        # Added a text-shadow directly to the style for better readability
        tspan = f'<tspan x="0" dy="{line_height}">{line}</tspan>'
        text_elements.append(tspan)

    joined_tspans = "".join(text_elements)
    
    svg_text_block = f'''
    <text font-family="Arial Black, sans-serif" font-weight="900" font-size="{font_size}" fill="#ffffff" style="filter: drop-shadow(4px 4px 4px rgba(0,0,0,0.7));">
      <tspan dy="{start_y_offset}"></tspan> 
      {joined_tspans}
    </text>
    '''

    # 5. Injection Logic
    try:
        with open("template.svg", "r") as f:
            svg_content = f.read()
            
        start_marker = '<g id="title-group" transform="translate(140, 360)">'
        end_marker = '</g>'
        
        start_index = svg_content.find(start_marker)
        end_index = svg_content.find(end_marker, start_index) + len(end_marker)
        
        if start_index != -1:
            new_content = (
                svg_content[:start_index] + 
                start_marker + 
                svg_text_block + 
                end_marker + 
                svg_content[end_index:]
            )
            
            with open(output_filename, "w") as out:
                out.write(new_content)
            svg_to_png(output_filename, output_filename.replace('.svg', '.png'))
            print(f"Done! Check {output_filename}")
        else:
            print("Error: Could not find the title-group in template.svg")

    except FileNotFoundError:
        print("Error: template.svg not found.")

