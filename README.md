# Draw.io Styler

Draw.io Styler allows you to use data from a CSV to quickly update styles for objects within an existing diagram.

The steps to updating styles are:

1. Prepare the Draw.io file for updating
2. Prepare the CSV file with the new style values
3. Use `drawiostyler` Python script to apply the values

## Prepare the Draw.io file for updating

From: https://www.drawio.com/blog/data-driven-diagrams

For each shape that will dynamically update based on a data source, you should override the auto-assigned shape ID to make it easier to refer to later.

1. Right-click on a shape and select Edit Data. Alternatively, select a shape and press Ctrl+M or Cmd+M.
2. Hold down Shift and double click on the ID string at the top.
3. Change the shape ID to something more memorable - make sure it is unique.
4. Click Apply to save the new shape ID, then click Apply to save the shape data.

## Prepare the CSV file with the new style values

Prepare a CSV with the new style values to be applied to your Draw.io file.

The first CSV column should be `id`. The values supplied here need to align with the IDs assigned in the Draw.io file for the style values to be updated.

The remaining columns need to be named after the key/value pairs to be included in the style attribute. Names are expected to be case sensitive. The values supplied in the CSV rows will be added or updated to the `style` for the relevant `object` in the Draw.io output file.

Example CSV content is included below.

```csv
id,fillColor,fontColor,strokeColor
Box_1,#a20025,#ffffff,#ffffff
```

An example of the Draw.io element that would have its content updated:

```xml
<object label="1" id="Box_1">
    <mxCell style="rounded=0;whiteSpace=wrap;html=1;fillColor=#a20025;fontColor=#ffffff;strokeColor=#6F0000;" parent="1" vertex="1">
```

## Use `drawiostyler` Python script to apply the values

Use the Python script to apply the CSV file to the input Draw.io file, to produce the output Draw.io file.

Example command line (MacOS):

```sh
python3 drawiostyler.py -i testdata/input.drawio -o out/output.drawio -d testdata/data.csv
```

The arguments used by the script:

| Purpose | Argument | File from Example |
| --- | --- | --- |
| Data CSV file | -d, --data | `testdata/data.csv` |
| Input Draw.io file | -i, --input | `testdata/input.drawio` |
| Output Draw.io file | -o, --output | `out/output.drawio` |
