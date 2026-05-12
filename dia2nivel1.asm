.data
VET:    .word 9, 4, 7, 1, 3, 8, 2, 6
N:	.word 8

.text
    lui  t0, 65552
    addi t0, t0, 0
    lui  t1, 65552
    addi t1, t1, 32
    lw   t1, 0(t1)
    addi s0, x0, 0

OUTER_LOOP:
    slt  t2, s0, t1
    beq  t2, x0, END
    addi s1, x0, 0
    sub  s2, t1, s0
    addi s2, s2, -1

INNER_LOOP:
    slt  t3, s1, s2
    beq  t3, x0, NEXT_I
    sll  t4, s1, x3
    add  t5, t0, t4
    lw   t6, 0(t5)
    lw   t6, 4(t5)
    slt  t3, t6, t6
    beq  t3, x0, NO_SWAP
    sw   t6, 0(t5)
    sw   t6, 4(t5)

NO_SWAP:
    addi s1, s1, 1
    bne  x0, x0, INNER_LOOP

NEXT_I:

    addi s0, s0, 1
    bne  x0, x0, OUTER_LOOP

END:
    jal  x0, END