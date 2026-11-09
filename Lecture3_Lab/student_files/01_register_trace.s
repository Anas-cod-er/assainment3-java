# Lecture 3 Lab - Task A. RARS 1.6, RV32 mode.
# Predict first. Break at trace_start and lab_done (before the nop).
.text
.globl main
main:
    addi x5, x0, 9
    addi x6, x0, 4
    addi x7, x0, 0
trace_start:
    sub  x7, x5, x6
    addi x5, x7, -1
    add  x6, x5, x7
    add  x0, x5, x6
lab_done:
    addi x0, x0, 0
    addi a7, x0, 10
    ecall
