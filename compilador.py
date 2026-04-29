from pathlib import *
from unittest import case

# Gabriel Pessoa Faustino - 231006121
instrucoes = [
    "lw","add", "sub", "and", "or", "xor",
    "addi","sw","jal","jalr","beq", "bne",
    "slt","slti","lui","auipc","sll", "srl",
    "andi", "ori", "xori","lhu"
]

# Gabriel Pessoa Faustino - 231006121
tipos = {
    "add": "R", "sub": "R", "and": "R", "or": "R", "xor": "R", "slt": "R", "sll": "R", "srl": "R",
    "lw": "I", "addi": "I", "jalr": "I", "slti": "I", "andi": "I", "ori": "I", "xori": "I", "lhu": "I",
    "sw": "S",
    "beq": "B", "bne": "B",
    "lui": "U", "auipc": "U",
    "jal": "J"
}

# Gabriel Pessoa Faustino - 231006121
registradores = {
    "zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011",
    "tp": "00100", "t0": "00101", "t1": "00110", "t2": "00111",
    "s0": "01000", "fp": "01000", "s1": "01001", "a0": "01010",
    "a1": "01011", "a2": "01100", "a3": "01101", "a4": "01110",
    "a5": "01111", "a6": "10000", "a7": "10001", "s2": "10010",
    "s3": "10011", "s4": "10100", "s5": "10101", "s6": "10110",
    "s7": "10111", "s8": "11000", "s9": "11001", "s10": "11010",
    "s11": "11011", "t3": "11100", "t4": "11101", "t5": "11110",
    "t6": "11111"
}

# Gabriel Pessoa Faustino - 231006121
ordem = dict()

# Gabriel Pessoa Faustino - 231006121
def int_bin(numero):
    if numero < 0:
        numero = (1 << 32) + numero
    return bin(numero)[2:].zfill(12)

# Gabriel Pessoa Faustino - 231006121
def conv_opcode(tipo):
    match tipo:
        case "R":
            return "0110011"
        case "I":
            return "0010011"
        case "S":
            return "0100011"
        case "B":
            return "1100011"
        case "U":
            return "1110111"
        case "J":
            return "1101111"
        case __:
            raise ValueError(f"Tipo {tipo} não reconhecido.")

# Gabriel Pessoa Faustino - 231006121        
def converter_instrucao(instrucao, linha, tipo):
    partes_limpas = linha.replace(",", " ").split()
    match instrucao:
        case "addi":
            rsi = registradores[partes_limpas[1]] # codigo do registrador fonte
            rd = registradores[partes_limpas[2]] # codigo do registrador de destino
            opcode = conv_opcode(tipo) # opcode para tipo I
            funct3 = "000" # função específica para addi
            imm = int_bin(int(partes_limpas[3])) # inteiro imediato com 12 bits
            return f"{imm} {rsi} {funct3} {rd} {opcode}"
        
        case "andi":
            rsi = registradores[partes_limpas[1]] # codigo do registrador fonte
            rd = registradores[partes_limpas[2]] # codigo do registrador de destino
            opcode = conv_opcode(tipo) # opcode para tipo I
            funct3 = "111" # função específica para andi
            imm = int_bin(int(partes_limpas[3])) # inteiro imediato com 12 bits
            return f"{imm} {rsi} {funct3} {rd} {opcode}"
        
        case "ori":
            rsi = registradores[partes_limpas[1]] # codigo do registrador fonte
            rd = registradores[partes_limpas[2]] # codigo do registrador de destino
            opcode = conv_opcode(tipo) # opcode para tipo I
            funct3 = "110" # função específica para ori
            imm = int_bin(int(partes_limpas[3])) # inteiro imediato com 12 bits
            return f"{imm} {rsi} {funct3} {rd} {opcode}"
        
        case "xori":
            rsi = registradores[partes_limpas[1]] # codigo do registrador fonte
            rd = registradores[partes_limpas[2]] # codigo do registrador de destino
            opcode = conv_opcode(tipo) # opcode para tipo I
            funct3 = "101" # função específica para xori
            imm = int_bin(int(partes_limpas[3])) # inteiro imediato com 12 bits
            return f"{imm} {rsi} {funct3} {rd} {opcode}"

        case __:
            return f"Instrução {instrucao} não implementada."

# Gabriel Pessoa Faustino - 231006121
arquivo = Path.cwd() / "teste.asm"

# Gabriel Pessoa Faustino - 231006121
with open(arquivo, 'r') as file:
    linhas = file.readlines()
    
    for idx, linha in enumerate(linhas):
        nova_linha = linha.strip()
        
        if not nova_linha:
            continue
        
        instrucao_linha = nova_linha.replace(",", " ").split()[0]
        
        if instrucao_linha in tipos:
            tipo = tipos[instrucao_linha]
            
            if instrucao_linha not in ordem:
                ordem[instrucao_linha] = []
            
            ordem[instrucao_linha].append((nova_linha, tipo))
            print(f"|{'imm':^12}|{'rs1':^5}|{'f3':^3}|{'rd':^5}|{'op':^7}|")
            print(converter_instrucao(instrucao_linha, nova_linha, tipo))




