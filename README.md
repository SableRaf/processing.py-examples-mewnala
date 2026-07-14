> [!WARNING]
> This is not an official port of the Processing examples to mewnala, and it is not intended for teaching, learning, or production use.

# Processing.py Examples → mewnala

A mechanical port of Processing.py examples to [mewnala](https://github.com/mewnala/mewnala) for research purposes only. 

This repository started as a fork of the [Processing.py repository](https://github.com/jdf/processing.py/) with most files removed, leaving only the examples that were ported from the original Java examples. Visit the Processing.py examples repository for the [full list of Python examples](https://github.com/jdf/processing.py/tree/master/mode/examples).

## Limitations and motivation

The conversion is mechanical and not guaranteed to be correct. Some examples may not run as expected, and some may require manual adjustments. The goal is to provide a starting point for exploring mewnala and facilitate the development of libprocessing. This effort runs parallel to https://github.com/processing/processing-examples-mewnala/issues/1. It doesn't replace the need for a proper port of the original Processing examples to mewnala.

## Contents

- `examples-python-mode/` — Original Processing.py examples
- `examples-mewnala/` — Ported example sketches
- `convert_to_mewnala.py` — Conversion utility script


## License & Credit

The original [Processing examples](https://github.com/processing/processing-examples/) written in Java include the following credit line:

> The examples without a credit line were written by Casey Reas or Ben Fry and they are in the public domain. Daniel Shiffman's examples are in the public domain. We appreciate a link back to the original and/or an acknowledgement when they are used. The copyrights for other credited files remains with the original authors.

Processing Python mode was created by [Jonathan Feinberg](http://mrfeinberg.com/). See https://github.com/jdf/processing.py/ and https://github.com/jdf/processing.py/graphs/contributors for more information on the Processing.py project and its contributors.

To comply with the Processing.py licenses, all examples *not* ported from the original Java examples were removed from this repository. The ported examples are provided under the same license as the original Processing examples. We have done our best to remove all non-public domain examples, but if you encounter any issues, please let us know.

## AI disclosure

The conversion script was generated with the help of AI, specifically Anthropic's Claude Fable 5 for planning, and OpenAI's GPT-5.6 Sol for code generation. The script is provided as-is and may contain errors or inaccuracies. Users are encouraged to review and test the converted code before use.