from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
import os

# Load the video
video_name = "meal_plan_demo"
video = VideoFileClip(video_name + ".mov")

# Define the segments to remove (in seconds) as tuples (start, end)
segments_to_remove = [(7, 25), (55, 74), (99, int(video.duration))]

# Create a list to hold the subclips
subclips = []

# Initial start of the first clip
start = 0
for (start_remove, end_remove) in segments_to_remove:
    # Add subclip before the segment to remove
    subclips.append(video.subclip(start, start_remove))
    # Update the start for the next subclip
    start = end_remove

# Add the last subclip after the final segment to remove
subclips.append(video.subclip(start))

# Concatenate all the subclips
final_clip = concatenate_videoclips(subclips)

# Speed up the video
final_clip = final_clip.fx(vfx.speedx, 2)  # 2x speed

# Write the result to a file
output_video = video_name + "_2x.mov"
final_clip.write_videofile(output_video, codec='libx264')

# Generate palette for high-quality GIF
os.system(f"ffmpeg -i {output_video} -vf \"fps=10,scale=1080:-1:flags=bicubic,palettegen\" -y palette.png")

# Create the GIF using the generated palette
output_gif = video_name + "_2x.gif"
os.system(f"rm {output_gif}")
os.system(f"ffmpeg -i {output_video} -i palette.png -lavfi \"fps=10,scale=1080:-1:flags=bicubic [x]; [x][1:v] paletteuse\" {output_gif}")