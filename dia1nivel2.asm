.data
VET:    .word 15, 3, 88, 21, 7, 54, 90, 12
MAIOR:    .word 0

.text
main:
    lui  t0, 65552
    addi t0, t0, 0
    addi t1, x0, 7
    lw   t2, 0(t0)
    addi t0, t0, 4
LOOP:
    lw   t3, 0(t0)
    slt  t4, t2, t3
    beq  t4, x0, CONT
    add  t2, t3, x0
CONT:
    addi t0, t0, 4
    addi t1, t1, -1
    bne  t1, x0, LOOP
    lui  t5, 65552
    addi t5, t5, 16
    sw   t2, 0(t5)
FIM:
    jal  x0, FIM