# Lecture 3 Lab Report

Name: __  Student ID: __  Partner: __  Date: __
Simulator version / RV32 setting: __

## A Register trace
Record x5, x6, x7 and x0 after every instruction from trace_start.
Add the observed PC before and after the first instruction.
Explain which instruction first changes each register and why x0 stays zero.

## B Memory and byte transfers
Actual sample address M: __
| Checkpoint | M | M+1 | M+2 | M+3 |
|---|---|---|---|---|
| After sw | | | | |
| After sb | | | | |

Final t3, t4 and t5 in 8-digit hexadecimal: __
Signed decimal t4 and unsigned decimal t5: __
Explain why the two byte loads differ and whether t0 changes.

## C Array sum
Actual base address B: __  trace_start S: __
Predict before running, then record observations separately.
| n | Predicted sum | Observed sum | x6 | x7 | x8 | Last load address | Count |
|---|---|---|---|---|---|---|---|
| 0 | | | | | | | |
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |

For n=3 record the four snapshots immediately before loop's beq.
Derive the dynamic instruction count using setup, tests and loop body.
Explain why a final pointer of B+12 does not prove a fourth load happened.
Transfer test: array=[5,-2,9], n=2. Predict and observe sum, pointer,
last load address, and count. Is the value 9 read?

## D Debugging
For each of D1-D3: mutation, exposing test, first incorrect state or access,
repair, and result after reassembly. Include one useful screenshot/trace.

## E Function
Submit your completed 04_sum_function.s. Record a0 for n=0,1,2,3.
Show that s0=123, s1=456 and sp are preserved. Identify the address in ra
at function entry and the instruction that returns to it.
Explain why this leaf function needs no stack frame when it uses only
caller-saved working registers. Explain why replacing t3 with x8 is unsafe.

## Exit ticket
1. What does lw x8,0(x7) place in x8?
2. Does advancing x7 load memory?
3. How many real instructions execute in Task C when n=2, under our boundary?
4. What observation proves that n=0 performs no array load?
