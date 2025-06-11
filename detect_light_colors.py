import re

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = "".join([c*2 for c in hex_color])
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return None

def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(rgb_color[0], rgb_color[1], rgb_color[2])

def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df / mx
    v = mx
    return h, s, v

def hsv_to_rgb(h, s, v):
    i = int(h/60) % 6
    f = (h/60) - i
    p = v * (1 - s)
    q = v * (1 - f*s)
    t = v * (1 - (1 - f)*s)
    if i == 0: r, g, b = v, t, p
    elif i == 1: r, g, b = q, v, p
    elif i == 2: r, g, b = p, v, t
    elif i == 3: r, g, b = p, q, v
    elif i == 4: r, g, b = t, p, v
    elif i == 5: r, g, b = v, p, q
    return int(r*255), int(g*255), int(b*255)

def invert_color(r, g, b):
    h, s, v = rgb_to_hsv(r, g, b)

    # Perceived brightness (luminance) - common formula
    luminance = 0.299 * r + 0.587 * g + 0.114 * b

    if luminance > 128:  # If the color is perceived as light
        # Option 1: Simple inversion and desaturation for very light colors
        if v > 0.8 and s < 0.3: # Very light, low saturation (e.g., whites, light grays)
            new_v = 0.1 + (1 - v) * 0.2 # Map to a dark gray range
            new_s = s * 0.5 # Reduce saturation further
        else:
            # Invert value (brightness)
            new_v = 1.0 - v
            # Adjust saturation: make it a bit higher for dark themes if it's too low
            new_s = s
            if new_s < 0.3:
                new_s = min(1.0, s + 0.2)
            elif new_s > 0.7:
                new_s = max(0, s - 0.1) # Slightly desaturate very saturated colors
            
            # Optionally, slightly shift hue for better dark theme aesthetics
            # h = (h + 10) % 360 # Example: slight hue shift

        # Ensure new_v is dark enough
        new_v = min(new_v, 0.5) # Cap brightness to be at most 50%
        new_v = max(new_v, 0.1) # Ensure some minimum brightness

    else:  # If the color is already perceived as dark
        # Option 1: Make it slightly darker or adjust saturation
        new_v = v * 0.8 # Make it a bit darker
        new_s = s
        if new_s > 0.6:
            new_s = max(0, s - 0.15) # Slightly desaturate if very saturated
        else:
            new_s = min(1.0, s + 0.1) # Slightly saturate if not very saturated
        
        # Ensure it's not too dark
        new_v = max(new_v, 0.05)

    return hsv_to_rgb(h, new_s, new_v)

def process_color_match(match):
    original_color_str = match.group(0)
    r, g, b, a = None, None, None, None

    # Try to parse rgba
    rgba_match = re.match(r'rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d\.]+)\)', original_color_str)
    if rgba_match:
        r, g, b, a = int(rgba_match.group(1)), int(rgba_match.group(2)), int(rgba_match.group(3)), float(rgba_match.group(4))
        inverted_r, inverted_g, inverted_b = invert_color(r, g, b)
        return f'rgba({inverted_r},{inverted_g},{inverted_b},{a})'

    # Try to parse rgb
    rgb_match = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', original_color_str)
    if rgb_match:
        r, g, b = int(rgb_match.group(1)), int(rgb_match.group(2)), int(rgb_match.group(3))
        inverted_r, inverted_g, inverted_b = invert_color(r, g, b)
        return f'rgb({inverted_r},{inverted_g},{inverted_b})'

    # Try to parse hex
    hex_match = re.match(r'#([A-Fa-f0-9]{3,6})', original_color_str)
    if hex_match:
        hex_val = hex_match.group(1)
        rgb_val = hex_to_rgb(hex_val)
        if rgb_val:
            r, g, b = rgb_val
            inverted_r, inverted_g, inverted_b = invert_color(r, g, b)
            inverted_hex = rgb_to_hex((inverted_r, inverted_g, inverted_b))
            # Preserve original hex length if it was a shorthand
            if len(hex_val) == 3 and inverted_hex[1]==inverted_hex[2] and inverted_hex[3]==inverted_hex[4] and inverted_hex[5]==inverted_hex[6]:
                 return f'#{inverted_hex[1]}{inverted_hex[3]}{inverted_hex[5]}'
            return inverted_hex

    # If no color format matched, return original string
    return original_color_str

def main():
    input_css_file = 'main.css'
    output_css_file = 'dark_main.css'
    # More robust regex to find colors, including those not at the start of a property value
    color_regex = re.compile(r'rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(?:,\s*[\d\.]+\s*)?\)|#[0-9a-fA-F]{3,6}')

    try:
        with open(input_css_file, 'r', encoding='utf-8') as f_in:
            css_content = f_in.read()
    except FileNotFoundError:
        print(f"错误：输入文件 '{input_css_file}' 未找到。");
        return
    except Exception as e:
        print(f"读取文件时发生错误 '{input_css_file}': {e}")
        return

    modified_css_content = color_regex.sub(process_color_match, css_content)

    try:
        with open(output_css_file, 'w', encoding='utf-8') as f_out:
            f_out.write(modified_css_content)
        print(f"成功将反色后的CSS写入 '{output_css_file}'")
    except Exception as e:
        print(f"写入文件时发生错误 '{output_css_file}': {e}")

if __name__ == '__main__':
    main()