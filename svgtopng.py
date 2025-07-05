#make changes according os follow this link https://stackoverflow.com/questions/73637315/oserror-no-library-called-cairo-2-was-found-from-custom-widgets-import-proje/73913080#73913080
from dotenv import load_dotenv
load_dotenv()
from cairosvg import svg2png
from PIL import Image
import io
from delete_file import delete_file
def svg_to_png(input_svg_path, output_png_path, width=1920, height=1080):
    """
    Rasters the SVG at optional width/height (pixels) and writes a PNG.
    forces a particular size to the output PNG.
    """
    svg2png(
        url=input_svg_path,
        write_to=output_png_path,
        output_width=width,
        output_height=height
    )
    delete_file(input_svg_path)
    print(f"Written PNG: {output_png_path}")