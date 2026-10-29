

import argparse
from decimal import Decimal
from fractions import Fraction
import math
import re
import struct


def decimal_integer(text):
    if len(text) > 16 or not re.fullmatch(r"[+-]?[0-9]+", text):
        raise argparse.ArgumentTypeError("use a decimal integer, for example 173 or -37")
    return int(text, 10)


def bounded_integer(text, low, high):
    value = decimal_integer(text)
    if not low <= value <= high:
        raise argparse.ArgumentTypeError("value must be in {}..{}".format(low, high))
    return value


def byte_integer(text):
    return bounded_integer(text, 0, 255)


def signed_integer(text):
    return bounded_integer(text, -128, 127)


def encoding_integer(text):
    # Union of the four encodings' ranges. Each row checks its own range.
    return bounded_integer(text, -128, 128)


def eight_bits(text):
    if not re.fullmatch(r"[01]{8}", text):
        raise argparse.ArgumentTypeError("supply exactly eight binary digits, for example 10110110")
    return text


def exact_decimal(text):
    if len(text) > 128 or not re.fullmatch(r"[+]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)", text):
        raise argparse.ArgumentTypeError("use a non-negative plain decimal, for example 10.625")
    value = Fraction(text)
    if value > 65535:
        raise argparse.ArgumentTypeError("fraction input must be in 0..65535")
    denominator = value.denominator
    if denominator & (denominator - 1):
        raise argparse.ArgumentTypeError("this experiment requires a terminating binary fraction; try 10.625 or 0.3125")
    if denominator > 2 ** 32:
        raise argparse.ArgumentTypeError("use a value requiring at most 32 binary fractional places")
    return value


def float_input(text):
    if len(text) > 128:
        raise argparse.ArgumentTypeError("floating-point input is too long")
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError("use a finite decimal value, for example 13.25 or 0.1")
    if not math.isfinite(value):
        raise argparse.ArgumentTypeError("use a finite value; NaN and infinity are outside this experiment")
    try:
        struct.pack(">f", value)
    except (OverflowError, struct.error):
        raise argparse.ArgumentTypeError("value is outside the finite binary32 range")
    return text


def short_text(text):
    if len(text) > 128:
        raise argparse.ArgumentTypeError("use at most 128 characters")
    return text


def fixed_value(text):
    if len(text) > 128 or not re.fullmatch(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)", text):
        raise argparse.ArgumentTypeError("use a plain decimal value, for example 5.25 or -5.25")
    value = Fraction(text)
    if not -32 <= value <= Fraction(127, 4):
        raise argparse.ArgumentTypeError("fixed-point value must be in -32..31.75")
    if (value * 4).denominator != 1:
        raise argparse.ArgumentTypeError("fixed-point value must be an exact multiple of 0.25")
    return value


def bits8(value):
    return format(value & 0xFF, "08b")


def signed8(value):
    return value if value < 128 else value - 256


def f32(value):
    """Quantize to binary32, then decode exactly into a Python float."""
    return struct.unpack(">f", struct.pack(">f", value))[0]


def f32_hex(value):
    return "0x" + struct.pack(">f", value).hex().upper()


def show_bases(args):
    value = args.number
    print("decimal (base 10): {}".format(value))
    print("binary (8 bits):   {}".format(bits8(value)))
    print("hex (2 digits):    {:02X}".format(value))
    print("octal (base 8):    {:o}".format(value))


def show_fraction(args):
    value = args.number
    whole, remainder = divmod(value.numerator, value.denominator)
    fractional_bits = []
    while remainder:
        remainder *= 2
        bit, remainder = divmod(remainder, value.denominator)
        fractional_bits.append(str(bit))
    fraction_part = "".join(fractional_bits) or "0"
    print("exact decimal input: {}".format(args.decimal_text))
    print("exact fraction:      {}".format(value))
    print("integer part:        {}".format(format(whole, "b")))
    print("fractional part:     .{}".format(fraction_part))
    print("binary value:        {}.{}".format(format(whole, "b"), fraction_part))


def show_signed(args):
    value = args.value
    print("decimal value: {}".format(value))
    encodings = [
        ("sign-and-magnitude", -127, 127, (0x80 if value < 0 else 0) | abs(value)),
        ("ones' complement", -127, 127, value if value >= 0 else (~abs(value) & 0xFF)),
        ("twos' complement", -128, 127, value & 0xFF),
        ("excess-127", -127, 128, value + 127),
    ]
    for name, low, high, pattern in encodings:
        representation = bits8(pattern) if low <= value <= high else "not representable"
        print("{:<20} {:<17} range {}..{}".format(name + ":", representation, low, high))
    if value == 0:
        print("Zero above is +0. Negative zero: sign-and-magnitude 10000000; ones' complement 11111111.")


def show_interpret(args):
    pattern = int(args.bits, 2)
    magnitude = pattern & 0x7F
    sign_magnitude = "-{}".format(magnitude) if pattern & 0x80 else str(magnitude)
    ones = "-{}".format((~pattern) & 0xFF) if pattern & 0x80 else str(pattern)
    print("same eight bits:     {} (hex {:02X})".format(args.bits, pattern))
    print("unsigned:            {}".format(pattern))
    print("sign-and-magnitude:  {}".format(sign_magnitude))
    print("ones' complement:    {}".format(ones))
    print("twos' complement:    {}".format(signed8(pattern)))
    print("excess-127:          {}".format(pattern - 127))


def add_details(left, right):
    unsigned_sum = (left & 0xFF) + (right & 0xFF)
    stored = unsigned_sum & 0xFF
    mathematical_sum = left + right
    return {
        "left": left, "right": right,
        "left_bits": bits8(left), "right_bits": bits8(right),
        "mathematical_sum": mathematical_sum,
        "unsigned_pattern_sum": unsigned_sum,
        "carry_out": unsigned_sum >> 8,
        "result_bits": bits8(stored),
        "stored_unsigned": stored,
        "stored_signed": signed8(stored),
        "signed_overflow": not -128 <= mathematical_sum <= 127,
    }


def show_add(args):
    result = add_details(args.left, args.right)
    print("8-bit twos' complement addition (explicit modulo-256 model)")
    print("left:                 {} ({})".format(result["left_bits"], args.left))
    print("right:                {} ({})".format(result["right_bits"], args.right))
    print("unsigned-pattern sum: {:09b}".format(result["unsigned_pattern_sum"]))
    print("carry out:            {}".format(result["carry_out"]))
    print("stored eight bits:    {}".format(result["result_bits"]))
    print("stored unsigned:      {}".format(result["stored_unsigned"]))
    print("stored signed:        {}".format(result["stored_signed"]))
    print("mathematical sum:     {}".format(result["mathematical_sum"]))
    print("signed overflow:      {}".format("yes" if result["signed_overflow"] else "no"))
    print("Carry out and signed overflow are separate checks.")


def show_text(args):
    text = args.message
    print("text: {}".format(repr(text)))
    print("ASCII uses 7 bits; ASCII rows below are padded to 8 bits, with no parity bit added.")
    for character in text:
        value = ord(character)
        if value <= 127:
            print("{!r}: ASCII decimal {:3d}, hex {:02X}, bits {}".format(character, value, value, bits8(value)))
        else:
            print("{!r}: U+{:04X}; no ASCII code".format(character, value))
    try:
        text.encode("ascii")
        print("ASCII encoding: OK")
    except UnicodeEncodeError:
        print("ASCII encoding: error (at least one character is outside 0..127)")
    data = text.encode("utf-8")
    print("UTF-8 byte count: {}".format(len(data)))
    print("UTF-8 hex bytes:  {}".format(" ".join("{:02X}".format(byte) for byte in data) or "(empty)"))
    print("UTF-8 bit bytes:  {}".format(" ".join(bits8(byte) for byte in data) or "(empty)"))


def show_fixed(args):
    stored = int(args.bits, 2) if args.bits is not None else int(args.value * 4) & 0xFF
    scaled_integer = signed8(stored)
    value = Fraction(scaled_integer, 4)
    pattern = bits8(stored)
    print("8-bit twos' complement fixed point; 2 fractional bits")
    print("stored eight bits:    {}".format(pattern))
    print("assumed binary point: {}.{}".format(pattern[:6], pattern[6:]))
    print("signed scaled integer: {}".format(scaled_integer))
    print("scale:                divide signed integer by 4")
    print("exact value:          {}".format(value))
    print("decimal value:        {}".format(format(float(value), ".2f").rstrip("0").rstrip(".")))
    print("range:                -32..31.75 in steps of 0.25")


def float_details(decimal_text):
    parsed = float(decimal_text)
    packed = struct.pack(">f", parsed)
    decoded = struct.unpack(">f", packed)[0]
    pattern = int.from_bytes(packed, "big")
    bit_string = format(pattern, "032b")
    exponent = (pattern >> 23) & 0xFF
    fraction_field = pattern & 0x7FFFFF
    classification = "normal" if exponent else ("subnormal" if fraction_field else "zero")
    return {
        "input": decimal_text, "python_float_input": format(parsed, ".17g"),
        "bits": bit_string, "hex": "0x" + packed.hex().upper(),
        "sign_bit": bit_string[0], "exponent_bits": bit_string[1:9],
        "fraction_bits": bit_string[9:], "stored_exponent": exponent,
        "classification": classification,
        "unbiased_exponent": exponent - 127 if exponent else (-126 if fraction_field else None),
        "exact_fraction": str(Fraction.from_float(decoded)),
        "exact_decimal": format(Decimal.from_float(decoded), "f"),
        "decoded_decimal_9_digits": format(decoded, ".9g"),
        "decoded_python_float": format(decoded, ".17g"),
    }


def show_float(args):
    result = float_details(args.number)
    print("Input is parsed as Python float, then rounded to IEEE 754 binary32.")
    print("input decimal:        {}".format(result["input"]))
    print("binary32 bits:        {}".format(result["bits"]))
    print("binary32 hex:         {}".format(result["hex"]))
    print("sign bit:             {}".format(result["sign_bit"]))
    print("exponent bits:        {} (stored {})".format(result["exponent_bits"], result["stored_exponent"]))
    print("fraction bits:        {}".format(result["fraction_bits"]))
    print("classification:       {}".format(result["classification"]))
    if result["classification"] == "normal":
        print("unbiased exponent:    {} (stored exponent - 127)".format(result["unbiased_exponent"]))
        print("implicit leading bit: 1")
    elif result["classification"] == "subnormal":
        print("effective exponent:   -126 (implicit leading bit is 0)")
    else:
        print("unbiased exponent:    not applicable to zero")
    print("exact stored fraction: {}".format(result["exact_fraction"]))
    print("exact stored decimal:  {}".format(result["exact_decimal"]))
    print("decoded decimal (9 significant digits): {}".format(result["decoded_decimal_9_digits"]))
    print("decoded as Python float: {}".format(result["decoded_python_float"]))


def precision_details(left, right):
    left32, right32 = f32(left), f32(right)
    intermediate = left32 + right32
    result32 = f32(intermediate)
    return {
        "python_expression": format(left + right, ".17g"),
        "left32": format(left32, ".17g"), "left32_hex": f32_hex(left32),
        "right32": format(right32, ".17g"), "right32_hex": f32_hex(right32),
        "sum_before_result_rounding": format(intermediate, ".17g"),
        "result32": format(result32, ".17g"), "result32_hex": f32_hex(result32),
        "result32_exact_fraction": str(Fraction.from_float(result32)),
    }


def show_precision(args):
    print("Python float arithmetic uses binary64 on ordinary Python 3 installations.")
    print("Binary32 experiments quantize EACH operand and then quantize the sum.")
    for label, left, right in [("16777216 + 1", 16777216.0, 1.0), ("0.1 + 0.2", 0.1, 0.2)]:
        result = precision_details(left, right)
        print("\nexperiment: {}".format(label))
        print("Python float expression:       {}".format(result["python_expression"]))
        print("binary32 left operand:         {} ({})".format(result["left32"], result["left32_hex"]))
        print("binary32 right operand:        {} ({})".format(result["right32"], result["right32_hex"]))
        print("Python sum of binary32 operands: {}".format(result["sum_before_result_rounding"]))
        print("binary32 rounded result:       {} ({})".format(result["result32"], result["result32_hex"]))
        print("exact binary32 result:         {}".format(result["result32_exact_fraction"]))


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    sub = subparsers.add_parser("bases", help="write an unsigned byte in bases 10, 2, 16 and 8")
    sub.add_argument("number", type=byte_integer, metavar="N")
    sub.set_defaults(action=show_bases)
    sub = subparsers.add_parser("fraction", help="convert an exact terminating decimal fraction to binary")
    sub.add_argument("decimal_text", type=str, metavar="DECIMAL")
    sub.set_defaults(action=show_fraction)
    sub = subparsers.add_parser("signed", help="encode a decimal value in four 8-bit formats")
    sub.add_argument("--value", required=True, type=encoding_integer, metavar="N")
    sub.set_defaults(action=show_signed)
    sub = subparsers.add_parser("interpret", help="read the same eight bits in several encodings")
    sub.add_argument("bits", type=eight_bits, metavar="BITS")
    sub.set_defaults(action=show_interpret)
    sub = subparsers.add_parser("add", help="add two signed bytes; inspect carry and signed overflow")
    sub.add_argument("left", type=signed_integer, metavar="A")
    sub.add_argument("right", type=signed_integer, metavar="B")
    sub.set_defaults(action=show_add)
    sub = subparsers.add_parser("text", help="inspect ASCII character codes and UTF-8 bytes")
    sub.add_argument("message", type=short_text, metavar="TEXT")
    sub.set_defaults(action=show_text)
    sub = subparsers.add_parser("fixed", help="encode or decode signed fixed point with two fractional bits")
    group = sub.add_mutually_exclusive_group(required=True)
    group.add_argument("--bits", type=eight_bits, metavar="BITS")
    group.add_argument("--value", type=fixed_value, metavar="DECIMAL")
    sub.set_defaults(action=show_fixed)
    sub = subparsers.add_parser("float", help="inspect a finite IEEE 754 binary32 value")
    sub.add_argument("number", type=float_input, metavar="DECIMAL")
    sub.set_defaults(action=show_float)
    sub = subparsers.add_parser("precision", help="compare Python float and explicitly rounded binary32 sums")
    sub.set_defaults(action=show_precision)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "fraction":
        try:
            args.number = exact_decimal(args.decimal_text)
        except argparse.ArgumentTypeError as error:
            parser.error(str(error))
    args.action(args)


if __name__ == "__main__":
    main()
