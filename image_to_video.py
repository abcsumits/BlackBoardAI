import ffmpeg
from delete_file import delete_file
def image_to_video(input_image, output_video,duration):
    (
        ffmpeg
        .input(input_image, loop=1, t=duration+1)   # loop image, duration 1s
        .output(
            output_video,
            vcodec='libx264',
            pix_fmt='yuv420p',
            vf='scale=trunc(iw/2)*2:trunc(ih/2)*2'
        )
        .overwrite_output()
        .run()
    )
    delete_file(input_image)

    print(output_video+" created")
