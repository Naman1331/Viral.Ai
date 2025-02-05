import subprocess
import re

def concatenate_mp4(files, output_file):
    timestamps = []
    current_time_stamp = 0
    for i in range(len(files)-1):
        new_time_stamp = current_time_stamp + get_mp4_length(files[i])
        timestamps.append(new_time_stamp)
    str_timestamps = [len(timestamps)]
    for i in range(len(timestamps)):
        timestamps[i] = round(timestamps[i])
        minutes = str((timestamps[i]//60))
        seconds = str((timestamps[i]%60))
        if len(seconds) == 1:
            seconds = '0' + seconds
        str_timestamps[i] = minutes + ':' + seconds

        
    # Create a list of input files formatted for ffmpeg
    input_files = '|'.join(files)
    
    # Run ffmpeg command to concatenate files
    command = f'ffmpeg -i "concat:{input_files}" -c copy {output_file}'
    subprocess.call(command, shell=True)
    return(output_file, str_timestamps)

def get_mp4_length(file):
    command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    duration_str = result.stdout.strip()
    duration = float(duration_str)
    return duration

# Example usage
input_files = ["src/new_video.mp4", "src/old_video.mp4"]  # List of MP4 files to concatenate
output_file = "src/concatenated.mp4"  # Output file name

print(concatenate_mp4(input_files, output_file))