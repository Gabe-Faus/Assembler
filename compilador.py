from pathlib import *
from unittest import case

# Gabriel Pessoa Faustino - 231006121
arquivo = Path.cwd() / "teste.asm"

# Gabriel Pessoa Faustino - 231006121
instrucoes = {
    "add":  {"tipo": "R", "opcode": "0110011", "funct3": "000", "funct7": "0000000"},
    "sub":  {"tipo": "R", "opcode": "0110011", "funct3": "000", "funct7": "0100000"},
    "and":  {"tipo": "R", "opcode": "0110011", "funct3": "111", "funct7": "0000000"},
    "or":   {"tipo": "R", "opcode": "0110011", "funct3": "110", "funct7": "0000000"},
    "xor":  {"tipo": "R", "opcode": "0110011", "funct3": "100", "funct7": "0000000"},
    "slt":  {"tipo": "R", "opcode": "0110011", "funct3": "010", "funct7": "0000000"},
    "sll":  {"tipo": "R", "opcode": "0110011", "funct3": "001", "funct7": "0000000"},
    "srl":  {"tipo": "R", "opcode": "0110011", "funct3": "101", "funct7": "0000000"},
    "addi": {"tipo": "I", "opcode": "0010011", "funct3": "000"},
    "andi": {"tipo": "I", "opcode": "0010011", "funct3": "111"},
    "ori":  {"tipo": "I", "opcode": "0010011", "funct3": "110"},
    "xori": {"tipo": "I", "opcode": "0010011", "funct3": "100"},
    "slti": {"tipo": "I", "opcode": "0010011", "funct3": "010"},
    "lw":   {"tipo": "I", "opcode": "0000011", "funct3": "010"},
    "lhu":  {"tipo": "I", "opcode": "0000011", "funct3": "101"},
    "jalr": {"tipo": "I", "opcode": "1100111", "funct3": "000"},
    "sw":   {"tipo": "S", "opcode": "0100011", "funct3": "010"},
    "beq":  {"tipo": "B", "opcode": "1100011", "funct3": "000"},
    "bne":  {"tipo": "B", "opcode": "1100011", "funct3": "001"},
    "lui":  {"tipo": "U", "opcode": "0110111"},
    "auipc":{"tipo": "U", "opcode": "0010111"},
    "jal":  {"tipo": "J", "opcode": "1101111"}
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
def converter_instrucao(instrucao, linha):
    partes_limpas = linha.replace(",", " ").split()
    informacoes = instrucoes[instrucao]
    tipo = informacoes["tipo"]

    match instrucao:
        case "addi" | "andi" | "ori" | "xori":
            rs1 = registradores[partes_limpas[2]]
            rd = registradores[partes_limpas[1]]
            opcode = informacoes["opcode"]
            funct3 = informacoes["funct3"]
            imm = int_bin(int(partes_limpas[3]))
            return f"{imm} {rs1} {funct3} {rd} {opcode}"

        case "add" | "sub" | "and" | "or" | "xor" | "slt" | "sll" | "srl":
            rs1 = registradores[partes_limpas[2]]
            rs2 = registradores[partes_limpas[3]]
            rd = registradores[partes_limpas[1]]
            opcode = informacoes["opcode"]
            funct3 = informacoes["funct3"]
            funct7 = informacoes["funct7"]
            return f"{funct7} {rs2} {rs1} {funct3} {rd} {opcode}"
        
        case "beq" | "bne":
            rs1 = registradores[partes_limpas[1]]
            rs2 = registradores[partes_limpas[2]]
            opcode = informacoes["opcode"]  
            funct3 = informacoes["funct3"]

            imm = int_bin(int(partes_limpas[3])) 

            imm_12 = imm[0]          # bit 12
            imm_10_5 = imm[1:7]      # bits de 10 a 5
            imm_4_1 = imm[7:11]      # bits de 4 a 1
            imm_11 = imm[11]         # bit 11

            return f"{imm_12}{imm_10_5} {rs2} {rs1} {funct3} {imm_4_1}{imm_11} {opcode}"

        case __:
            return f"Instrução {instrucao} não implementada."




def main():

# Gabriel Pessoa Faustino - 231006121
    with open(arquivo, 'r') as file:
        linhas = file.readlines()
    
        for idx, linha in enumerate(linhas):
            nova_linha = linha.strip()
            
            if not nova_linha:
                continue
            
            instrucao_linha = nova_linha.replace(",", " ").split()[0]
            
            if instrucao_linha in instrucoes:
                if instrucao_linha not in ordem:
                    ordem[instrucao_linha] = []
                
                ordem[instrucao_linha].append((nova_linha, instrucoes[instrucao_linha]["tipo"]))
                print(f"|{'imm':^12}|{'rs1':^5}|{'f3':^3}|{'rd':^5}|{'op':^7}|")
                print(converter_instrucao(instrucao_linha, nova_linha))

                with open(f"{arquivo.stem}.mif", 'a') as output_file:
                    output_file.write(converter_instrucao(instrucao_linha, nova_linha) + "\n")



if __name__ == "__main__":
    main()