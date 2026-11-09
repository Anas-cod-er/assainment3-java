# Lecture 3 Lab Session

Read Lecture3_Lab_Student_Handout.docx first. The session is 120 minutes.
Use RARS 1.6 in its default RV32 mode and Default memory configuration.
Official download: https://github.com/TheThirdOne/rars/releases/tag/v1.6
Launch with `java -jar rars1_6.jar` (use the name of your downloaded jar).
Open and assemble ONE source file at a time; disable directory/project assembly.
Save an edited copy and reassemble before every new test.

- 01_register_trace.s: complete program for prediction and single stepping.
- 02_memory_bytes.s: complete word/byte transfer experiment.
- 03_array_sum.s: complete lecture loop; vary n and data as instructed.
- 04_sum_function_starter.s: runnable scaffold with an intentionally incomplete function.
- report_template.md: copy and fill with predictions, observations and explanations.

Set breakpoints on the instruction following the named label. A label itself
is not executable. Breakpoints stop before their instruction executes.
At Task C, count only from trace_start through the final taken beq, stopping
before end. Exclude input setup, the end nop, and exit instructions.
Use the real assembled addresses. The lecture's 0x1000 data address and
zero-based instruction addresses are illustrative.

la and li are assembler pseudoinstructions. They can expand to multiple
machine instructions. The counted Task C region contains only real RV32I
instructions. The RARS exit service (a7=10; ecall) is simulator-specific.
Do not copy syscall conventions from a different simulator into these files.
RARS itself is not included in this package.
