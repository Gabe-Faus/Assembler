.data
enunc1: .asciz "Qual número você quer dividir? \n"
enunc2: .asciz "\nVocê gostaria de dividir "
enunc3: .asciz " por qual numero?\n"
resp1: .asciz "\nO quociente eh: "
resp2: .asciz "\nO resto eh: "

.text

main:
	# Print do primeiro enunciado
	li a7, 4
	la a0, enunc1
	ecall
	
	# Input do numero n
	li a7, 5
	ecall
	
	# move o valor de n que esta em a0 para a1 e guarda
	add a1, a0, zero
	
	# Print do segundo  enunciado
	li a7, 4
	la a0, enunc2
	ecall
	

	# Print do numero n escolhido	
	li a7, 1
	add a0, a1, zero
	ecall
	
	# Print do terceiro enunciado
	li a7, 4
	la a0, enunc3
	ecall
	
	# Input de i
	li a7, 5
	ecall
	
	# mone o valor i para a2
	add a2, a0, zero
	
	# inicio do contador
	add t0, zero, zero
	
	# chama a função multiplicar
	jal div
	
	add t1, a1, zero
	add t0, a0, zero
	
	# Print da string do quociente
	li a7, 4
	la a0, resp1
	ecall
	
	# mostra o quociente
	li a7, 1
	add a0, t0, zero
	ecall
	
	# Print da string do resto
	li a7, 4
	la a0, resp2
	ecall
	
	# Print do resto
	li a7, 1
	add a0, t1, zero
	ecall
	
	
	# Saída
	li a7, 10
	ecall
	
	
div:
	addi sp, sp, -4
	sw ra, 0(sp)
	
	blt a1, a2, base
	
 	sub a1, a1, a2

	jal div
	
	addi a0, a0, 1
	
	lw ra, 0(sp)
	addi sp, sp, 4
	ret
	
base:
	addi a0, zero, 0 
	
	lw ra, 0(sp)
	addi sp, sp, 4
	ret