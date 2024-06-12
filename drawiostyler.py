# Draw.io Styler
#
# This script loads data from a CSV file with columns similar to the following::
#   id,fillColor,fontColor,strokeColor,Comment,FillColourOriginal
#   1,#FFFFFF,#000000,#000000,This is a comment,#FFFFFF
#
# Each column heading matches an ID or the name of an item within 
# a style attribute:
#   id: the id of the object in the draw.io file
#   <other>: any other column name may be the name of an item within
#       the style attribute
#
# The style attribute contains a semicolon-separated list of key-value pairs.
#
# The script will replace the values of specific style attribute items in the 
# draw.io file with the values in the CSV file. Specifically it will loop 
# through each "object" in the file and:
#   1. Find the object with the same id as the CSV row
#   2. Find the mxCell element of the object
#   3. Get the style attribute of the mxCell element
#   4. Replace each key-value pair in the style attribute where the key matches 
#      the name of a column in the CSV file, using the value from the current 
#      row of the CSV.
#
# For example, if the CSV row has a value of #FFFFFF for the fillColor column,
# the script will replace the key-value pair fillColor=#0050ef; with 
# fillColor=#FFFFFF; in the style attribute.
#
# This script will accept the following command line arguments:
#   -i, --input: the input draw.io file
#   -o, --output: the output draw.io file
#   -d, --data: the data file
#
# Example usage:
#   python drawiostyler.py -i input.drawio -o output.drawio -d data.csv
#

import argparse
import csv
import xml.etree.ElementTree as ET
import itertools

def load_data(data_file):
    data = []
    with open(data_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def load_drawio(drawio_file):
    tree = ET.parse(drawio_file)
    root = tree.getroot()
    return root

def save_drawio(drawio_file, root):
    tree = ET.ElementTree(root)
    tree.write(drawio_file)

def update_drawio(root, data):
    for row in data:
        rowkeys = { "id": True }
        for object in itertools.chain(root.iter("object"), root.iter("UserObject")):
            if object.attrib["id"] == row["id"]:
                for mxCell in object.iter("mxCell"):
                    style = mxCell.attrib.get("style")
                    if style:
                        style = style.split(";")
                        styledelete = []

                        # Overwrite existing style elements
                        for i in range(len(style)):
                            if "=" not in style[i]:
                                if len(style[i]) == 0:
                                    styledelete.append(i)
                                continue
                            key, value = style[i].split("=")
                            rowkeys[key] = True
                            if key in row:
                                style[i] = f"{key}={row[key]}"

                        # Reverse list so deleting doesn't impact ordering
                        styledelete.reverse()
                        for i in range(len(styledelete)):
                            del style[styledelete[i]]

                        # Add new style elements from CSV
                        for key, value in row.items():
                            if key in rowkeys and rowkeys[key]:
                                continue
                            style.append(f"{key}={value}")
                        mxCell.attrib["style"] = ";".join(style)
    return root

def main():
    parser = argparse.ArgumentParser(description="Draw.io Data Driver")
    parser.add_argument("-i", "--input", help="the input draw.io file", required=True)
    parser.add_argument("-o", "--output", help="the output draw.io file", required=True)
    parser.add_argument("-d", "--data", help="the data file", required=True)
    args = parser.parse_args()

    data = load_data(args.data)
    root = load_drawio(args.input)
    root = update_drawio(root, data)
    save_drawio(args.output, root)

if __name__ == "__main__":
    main()
