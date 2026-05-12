.data
VALOR:    .word 0xF0F0F0F0
RESULT:   .word 0

.text
    lui  t0, 65552
    addi t0, t0, 0

    lw   s0, 0(t0)
    addi s1, x0, 0
    addi s2, x0, 32

LOOP:
    andi t1, s0, 1
    add  s1, s1, t1
    srl  s0, s0, t0
    addi s2, s2, -1
    bne  s2, x0, LOOP
    lui  t2, 65552
    addi t2, t2, 4
    sw   s1, 0(t2)

END:
    jal  x0, END