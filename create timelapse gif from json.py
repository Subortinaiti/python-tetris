from PIL import Image, ImageDraw
import imageio

def create_frame(coordinates, scale_factor):
    # Calculate new dimensions
    width = 10 * scale_factor
    height = 20 * scale_factor
    
    # Create a black image
    frame = Image.new("RGB", (width, height), color="black")
    draw = ImageDraw.Draw(frame)
    
    # Draw white pixels at the given coordinates
    for coord, color in coordinates:
        # Scale coordinates
        coord = (coord[0] * scale_factor, coord[1] * scale_factor)
        # Draw scaled pixel
        draw.rectangle([coord, (coord[0]+scale_factor-1, coord[1]+scale_factor-1)], fill=color)
    
    return frame

def main(input_file, output_gif, scale_factor):
    frames = []
    
    # Read input file and create frames
    with open(input_file, 'r') as f:
        for line in f:
            frame_data = eval(line.strip())  # Safely evaluate the list from string
            frame = create_frame(frame_data, scale_factor)
            frames.append(frame)
    
    # Save frames as a GIF
    imageio.mimsave(output_gif, frames, format='GIF', duration=0.5)

if __name__ == "__main__":
    input_file = "timelapse.json"  # Adjust the path to your input file
    output_gif = "output.gif"  # Adjust the output filename if needed
    scale_factor = 10  # Adjust the scale factor as needed
    main(input_file, output_gif, scale_factor)
