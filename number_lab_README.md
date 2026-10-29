# Number representation console experiments

Use Python 3.8 or later. No extra packages, compiler, simulator, or internet connection are needed. Open a terminal in the folder containing `number_lab.py`. On some systems the command is `python` or `py -3` instead of `python3`.

Predict and explain an answer on paper before running an experiment. The program computes results for your input; it contains no worksheet answer file.

```sh
python3 number_lab.py --help
python3 number_lab.py bases 173
python3 number_lab.py fraction 10.625
python3 number_lab.py signed --value -37
python3 number_lab.py interpret 10110110
python3 number_lab.py add 96 40
python3 number_lab.py add -70 -80
python3 number_lab.py add 96 -40
python3 number_lab.py text 'Hi!'
python3 number_lab.py fixed --bits 11110101
python3 number_lab.py fixed --value 5.25
python3 number_lab.py fixed --value -5.25
python3 number_lab.py float 13.25
python3 number_lab.py float 0.1
python3 number_lab.py precision
```

- `bases`: decimal integers 0..255; binary is padded to 8 bits, hex to 2 digits, and octal uses its shortest form without leading zeros.
- `fraction`: non-negative plain decimal strings 0..65535 whose reduced denominator is a power of two; at most 32 binary fractional places. It reads the decimal exactly using `Fraction`. Try `0.3125`; `0.1` is rejected because its binary expansion does not terminate.
- `signed`: values -128..128, the combined range of the four formats. Each row reports its own range and any value it cannot represent. Zero is encoded as positive zero.
- `interpret`: exactly eight binary digits; sign-and-magnitude and ones' complement preserve negative zero in their printed interpretations. Excess-127 means unsigned pattern minus 127.
- `add`: signed decimal operands -128..127. This explicitly models an 8-bit twos' complement adder: store the low 8 bits, report carry out from the unsigned bit patterns, and check signed overflow separately. It is a mathematical model, not a claim about C signed-overflow behavior.
- `text`: up to 128 characters. ASCII rows are padded to 8 bits without adding parity. Non-ASCII input reports why ASCII encoding fails and still prints valid UTF-8 bytes. Try `text 'é'`.
- `fixed`: use either `--bits` followed by exactly 8 bits or `--value` followed by an exact decimal multiple of 0.25 in -32..31.75. The signed 8-bit integer is divided by 4, so the assumed point separates six bits from two bits.
- `float`: parses a finite decimal as Python `float`, then uses `struct.pack('>f')` and `struct.unpack('>f')` to quantize and inspect binary32. Byte order is explicit. Output includes both the exact stored rational value and the full exact stored decimal; the 9-significant-digit decimal is a rounded display. Zero and subnormal values are identified separately. Values that would overflow binary32 are rejected.
- `precision`: rounds each operand to binary32 before adding, then rounds the result to binary32. Python's ordinary float expression and the intermediate sum are printed separately, so they are not mistaken for binary32 arithmetic.

Use `python3 number_lab.py COMMAND --help` for a command's input form.

For a negative float written with an exponent, use `python3 number_lab.py float -- -1e-40`. The `--` tells the command-line parser that the next item is a value.
