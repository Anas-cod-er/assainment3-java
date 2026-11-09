# Lecture 3 Lab - Task C. Standalone execution trace, not an ABI function.
# x8 is s0; it is intentionally used as in the lecture's standalone trace.
# RARS allocates the actual base address. Do not hard-code 0x1000.
.data
.align 2
array: .word 3, -1, 4
.text
.globl main
main:
    la   x10, array
    addi x11, x0, 3       # INPUT_N: test 0, 1, 2, 3 only
    addi x8, x0, 0        # Sentinel outside the counted region
trace_start:
    addi x5, x0, 0        # sum = 0
    addi x6, x0, 0        # i = 0
    addi x7, x10, 0       # pointer = base
loop:
    beq  x6, x11, end     # Check BEFORE load
    lw   x8, 0(x7)
    add  x5, x5, x8
    addi x7, x7, 4
    addi x6, x6, 1
    jal  x0, loop
end:
    addi x0, x0, 0        # STOP BEFORE this instruction
    addi a7, x0, 10       # Simulator exit; outside the count
    ecall
