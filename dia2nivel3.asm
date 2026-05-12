.data
A:
    .word 1, 2
    .word 3, 4
B:
    .word 5, 6
    .word 7, 8
C:
    .word 0, 0
    .word 0, 0

.text
    lui  s0, 65552
    addi s0, s0, 0
    lui  s1, 65552
    addi s1, s1, 16
    lui  s2, 65552
    addi s2, s2, 32
    addi s3, x0, 0

LOOP_I:

    slti t0, s3, 2
    beq  t0, x0, END
    addi s4, x0, 0

LOOP_J:

    slti t0, s4, 2
    beq  t0, x0, NEXT_I
    addi s5, x0, 0
    addi s6, x0, 0

LOOP_K:
    slti t0, s6, 2
    beq  t0, x0, STORE
    sll  t1, s3, t1
    add  t1, t1, s6
    sll  t1, t1, t0
    add  t2, s0, t1
    lw   a0, 0(t2)
    sll  t3, s6, t5
    add  t3, t3, s4
    sll  t3, t3, s2
    add  t4, s1, t3
    lw   a1, 0(t4)
    jal  ra, MULT
    add  s5, s5, a0
    addi s6, s6, 1
    bne  x0, x0, LOOP_K

STORE:
    sll  t5, s3, t2
    add  t5, t5, s4
    sll  t5, t5, t2
    add  t6, s2, t5
    sw   s5, 0(t6)
    addi s4, s4, 1
    bne  x0, x0, LOOP_J

NEXT_I:
    addi s3, s3, 1
    bne  x0, x0, LOOP_I
MULT:

    addi t0, x0, 0
    addi t1, x0, 32

M_LOOP:
    andi t2, a1, 1
    beq  t2, x0, SHIFT
    add  t0, t0, a0

SHIFT:

    sll  a0, a0, t0
    srl  a1, a1, t1
    addi t1, t1, -1
    bne  t1, x0, M_LOOP
    add  a0, t0, x0
    jalr x0, 0(ra)

END:
    jal  x0, END