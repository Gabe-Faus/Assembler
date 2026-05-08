.data
A:    .word 13
B:    .word 11
RES:    .word 0

.text
main:
    lui  s0, %hi(A)
    addi s0, s0, %lo(A)
    lw   a0, 0(s0)
    lui  s1, %hi(B)
    addi s1, s1, %lo(B)
    lw   a1, 0(s1)
    jal  ra, MULT
    lui  s2, %hi(RES)
    addi s2, s2, %lo(RES)
    sw   a0, 0(s2)
FIM:
    jal  x0, FIM
MULT:
    addi t0, x0, 0
    addi t1, x0, 32
LOOP:
    andi t2, a1, 1
    beq  t2, x0, SHIFT
    add  t0, t0, a0
SHIFT:
    slli  a0, a0, 1
    srli  a1, a1, 1
    addi t1, t1, -1
    bne  t1, x0, LOOP
    add  a0, t0, x0
    jalr x0, 0(ra)