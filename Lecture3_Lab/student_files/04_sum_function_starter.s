# Lecture 3 Lab - Task E. Interface: a0=base, a1=n; result in a0.
# n must be nonnegative and no larger than the allocated element count.
.data
.align 2
array: .word 3, -1, 4
.text
.globl main
main:
    andi sp, sp, -16      # Align simulator startup stack before the call
    addi s0, x0, 123      # Caller values must survive
    addi s1, x0, 456
    la   a0, array
    addi a1, x0, 3        # INPUT_N: test 0, 1, 2, 3
    jal  ra, sum_array
after_call:
    addi x0, x0, 0        # Break here; inspect a0, ra, sp, s0, s1
    addi a7, x0, 10
    ecall
sum_array:

    # TODO: use t0=sum, t1=i, t2=pointer, t3=loaded value.
    # Initialize, check n before lw, accumulate, advance, repeat.
    # Replace the placeholder below with your implementation.
    addi a0, x0, 0        # PLACEHOLDER: returns zero for every input
    jalr x0, 0(ra)
