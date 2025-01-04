from PIL import Image, ImageDraw

def create_icon(size):
    # Create a new image with a transparent background
    image = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # Calculate dimensions
    padding = size // 8
    
    # Draw gradient-like background (layered circles)
    colors = ['#4A90E2', '#357ABD', '#2C6AA8']
    for i, color in enumerate(colors):
        offset = i * (padding // 2)
        draw.ellipse(
            [offset, offset, size - offset, size - offset],
            fill=color
        )
    
    # Draw stylized 'N' for News
    n_width = size // 2
    n_height = size // 1.5
    n_x = (size - n_width) // 2
    n_y = (size - n_height) // 2
    
    # Draw the N shape in white
    points = [
        (n_x, n_y + n_height),  # bottom left
        (n_x, n_y),  # top left
        (n_x + n_width, n_y + n_height),  # bottom right
        (n_x + n_width, n_y)  # top right
    ]
    
    # Draw N shape
    draw.line([points[0], points[1]], fill='white', width=max(2, size // 8))  # left line
    draw.line([points[1], points[2]], fill='white', width=max(2, size // 8))  # diagonal
    draw.line([points[2], points[3]], fill='white', width=max(2, size // 8))  # right line
    
    # Draw perspective dots
    dot_radius = max(1, size // 16)
    dot_positions = [
        (size - dot_radius * 2, size // 2),
        (size - dot_radius * 4, size // 2),
        (size - dot_radius * 6, size // 2)
    ]
    
    for x, y in dot_positions:
        draw.ellipse(
            [x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius],
            fill='white'
        )
    
    # Save the image
    image.save(f'icon{size}.png', 'PNG')

# Generate icons in different sizes
for size in [16, 48, 128]:
    create_icon(size)
