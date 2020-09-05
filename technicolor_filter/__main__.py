import argparse
from . import read_image


def str2inttuple(value):
    value = value.strip(")(")
    return [int(num.strip()) for num in value.split(",")]


parser = argparse.ArgumentParser()
parser.add_argument("--in_filename", help="file name to the photo to process", type=str)
parser.add_argument(
    "--cyan",
    default="Cyan",
    help="select shade of cyan enter color name or a tuple of RGB values",
    type=str,
)
parser.add_argument(
    "--magenta",
    default="Magenta",
    help="select shade of magenta enter color name or a tuple of RGB values",
    type=str,
)
parser.add_argument(
    "--yellow",
    default="Yellow",
    help="select shade of yellow enter color name or a tuple of RGB values",
    type=str,
)
parser.add_argument("--key", default=0.0, help="select the key level", type=float)
args, unparsed = parser.parse_known_args()
filename = "./" + args.in_filename.split("/")[-1]
parser.add_argument(
    "--out_filename",
    default=filename,
    help="file name to output the processed photo defaule to current directory same name as input",
    type=str,
)

args, unparsed = parser.parse_known_args()

# process color strings
if args.cyan[0] == "(":
    cyan = str2inttuple(args.cyan)
else:
    cyan = args.cyan
if args.magenta[0] == "(":
    magenta = str2inttuple(args.magenta)
else:
    magenta = args.magenta
if args.yellow[0] == "(":
    yellow = str2inttuple(args.yellow)
else:
    yellow = args.yellow

img = read_image(args.in_filename)
img.set_all_color([cyan, magenta, yellow])
img.set_key_level(args.key)
img.save(args.out_filename)
