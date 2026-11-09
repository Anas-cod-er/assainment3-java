# Lecture 3 Lab - Task B. Independent from the array experiment.
# Break BEFORE word_stored, bytes_changed and lab_done instructions.
.data
.align 2
sample: .word 0
.text
.globl main
main:
    la   t0, sample
    li   t1, 0x12345678
    sw   t1, 0(t0)
word_stored:
    addi t2, x0, -17
    sb   t2, 1(t0)
bytes_changed:
    lw   t3, 0(t0)
    lb   t4, 1(t0)
    lbu  t5, 1(t0)
lab_done:
    addi x0, x0, 0
    addi a7, x0, 10
    ecall
