from pathlib import *

INSTRUCOES = {
    "add":   {"tipo": "R", "opcode": "0110011", "funct3": "000", "funct7": "0000000"},
    "sub":   {"tipo": "R", "opcode": "0110011", "funct3": "000", "funct7": "0100000"},
    "and":   {"tipo": "R", "opcode": "0110011", "funct3": "111", "funct7": "0000000"},
    "or":    {"tipo": "R", "opcode": "0110011", "funct3": "110", "funct7": "0000000"},
    "xor":   {"tipo": "R", "opcode": "0110011", "funct3": "100", "funct7": "0000000"},
    "slt":   {"tipo": "R", "opcode": "0110011", "funct3": "010", "funct7": "0000000"},
    "sll":   {"tipo": "R", "opcode": "0110011", "funct3": "001", "funct7": "0000000"},
    "srl":   {"tipo": "R", "opcode": "0110011", "funct3": "101", "funct7": "0000000"},
    "slli":  {"tipo": "IS", "opcode": "0010011", "funct3": "001", "funct7": "0000000"},
    "srli":  {"tipo": "IS", "opcode": "0010011", "funct3": "101", "funct7": "0000000"},
    "srai":  {"tipo": "IS", "opcode": "0010011", "funct3": "101", "funct7": "0100000"},
    "addi":  {"tipo": "I", "opcode": "0010011", "funct3": "000"},
    "andi":  {"tipo": "I", "opcode": "0010011", "funct3": "111"},
    "ori":   {"tipo": "I", "opcode": "0010011", "funct3": "110"},
    "xori":  {"tipo": "I", "opcode": "0010011", "funct3": "100"},
    "slti":  {"tipo": "I", "opcode": "0010011", "funct3": "010"},
    "lw":    {"tipo": "I", "opcode": "0000011", "funct3": "010"},
    "lhu":   {"tipo": "I", "opcode": "0000011", "funct3": "101"},
    "jalr":  {"tipo": "I", "opcode": "1100111", "funct3": "000"},
    "sw":    {"tipo": "S", "opcode": "0100011", "funct3": "010"},
    "beq":   {"tipo": "B", "opcode": "1100011", "funct3": "000"},
    "bne":   {"tipo": "B", "opcode": "1100011", "funct3": "001"},
    "lui":   {"tipo": "U", "opcode": "0110111"},
    "auipc": {"tipo": "U", "opcode": "0010111"},
    "jal":   {"tipo": "J", "opcode": "1101111"},
}

REGISTRADORES = {
    **{f"x{i}": format(i, "05b") for i in range(32)},
    "zero": "00000",
    "ra":   "00001",
    "sp":   "00010",
    "gp":   "00011",
    "tp":   "00100",
    "t0": "00101", "t1": "00110", "t2": "00111",
    "s0": "01000", "fp": "01000", "s1": "01001",
    "a0": "01010", "a1": "01011", "a2": "01100", "a3": "01101",
    "a4": "01110", "a5": "01111", "a6": "10000", "a7": "10001",
    "s2": "10010", "s3": "10011", "s4": "10100", "s5": "10101",
    "s6": "10110", "s7": "10111", "s8": "11000", "s9": "11001",
    "s10": "11010", "s11": "11011",
    "t3": "11100", "t4": "11101", "t5": "11110", "t6": "11111",
}


TEXT_BASE = 0x00400000  
DATA_BASE = 0x10010000   

def int_bin(numero, tamanho=12):
    m = (1 << tamanho) - 1
    nm = numero & m
    return bin(nm)[2:].zfill(tamanho)

def bin_hex(bin_str):
    bin_str = bin_str.replace(" ", "")
    hex_2 = hex(int(bin_str, 2))[2:].upper()
    return hex_2.zfill(8)


def gerar_arquivo_mif(nome_arquivo, conjunto_text, conjunto_data, instrucoes):

    depth_padrao = 1024 # para terminar em 3ff se usar o 32768 ai vai terminar em 7fff

    # ---------------- DATA ----------------
    with open(f"{nome_arquivo}_data.mif", 'w') as f:

        f.write(f"DEPTH = {depth_padrao};\n")
        f.write("WIDTH = 32;\n")
        f.write("ADDRESS_RADIX = HEX;\n")
        f.write("DATA_RADIX = HEX;\n")
        f.write("CONTENT\n")
        f.write("BEGIN\n")

        for i, valor_hex in enumerate(conjunto_data):
            f.write(f"{i:08x} : {valor_hex.lower()};\n")

        for addr in range(len(conjunto_data), depth_padrao):
            f.write(f"{addr:08x} : 00000000;\n")

        f.write("END;\n")

    # ---------------- TEXT ----------------
    with open(f"{nome_arquivo}_text.mif", 'w') as f:

        f.write(f"DEPTH = {depth_padrao};\n")
        f.write("WIDTH = 32;\n")
        f.write("ADDRESS_RADIX = HEX;\n")
        f.write("DATA_RADIX = HEX;\n")
        f.write("CONTENT\n")
        f.write("BEGIN\n")

        for i, valor_hex in enumerate(conjunto_text):

            f.write(f"{i:08x} : {valor_hex.lower()};")

            if i < len(instrucoes):
                f.write(f"    % {instrucoes[i]} %")

            f.write("\n")

        """
        for addr in range(len(conjunto_text), depth_padrao):
            f.write(f"{addr:08x} : 00000000;\n")
        """
        
        f.write("END;\n")
        


def converter_instrucao(instrucao, linha, pc, labels):
    
    linha_limpa = linha.replace(",", " ").replace("(", " ").replace(")", " ")

    tem_hi = "%hi" in linha_limpa
    tem_lo = "%lo" in linha_limpa
    linha_limpa = linha_limpa.replace("%hi", "").replace("%lo", "")

    partes_limpas = linha_limpa.split()

    if instrucao not in INSTRUCOES:
        return "Opcode desconhecido ou instrucao inexistente"

    informacoes = INSTRUCOES[instrucao]

    def pega_numero(val):
        if val in labels:
            return labels[val]
        try:
            return int(val, 0)
        except:
            return 0

    def pega_hi(val):

        addr = pega_numero(val)
        lo = addr & 0xFFF
        hi = addr >> 12
  
        if lo >= 0x800:
            hi += 1
        return hi

    def pega_lo(val):
       
        addr = pega_numero(val)
        lo = addr & 0xFFF
        if lo >= 0x800:
            lo -= 0x1000
        return lo

    match instrucao:

        case "addi" | "andi" | "ori" | "xori" | "slti":
            rs1 = REGISTRADORES[partes_limpas[2]]
            rd  = REGISTRADORES[partes_limpas[1]]
            opcode = informacoes["opcode"]
            funct3 = informacoes["funct3"]
            # CORREÇÃO: respeitar %lo se presente
            if tem_lo:
                imm_val = pega_lo(partes_limpas[3])
            else:
                imm_val = pega_numero(partes_limpas[3])
            imm = int_bin(imm_val, 12)
            retorno = f"{imm} {rs1} {funct3} {rd} {opcode}"

        case "add" | "sub" | "and" | "or" | "xor" | "slt" | "sll" | "srl":
            rs1 = REGISTRADORES[partes_limpas[2]]
            rs2 = REGISTRADORES[partes_limpas[3]]
            rd  = REGISTRADORES[partes_limpas[1]]
            opcode = informacoes["opcode"]
            funct3 = informacoes["funct3"]
            funct7 = informacoes["funct7"]
            retorno = f"{funct7} {rs2} {rs1} {funct3} {rd} {opcode}"

      
        case "slli" | "srli" | "srai":
            rd     = REGISTRADORES[partes_limpas[1]]
            rs1    = REGISTRADORES[partes_limpas[2]]
            shamt  = int(partes_limpas[3], 0) & 0x1F  # 5 bits
            opcode = informacoes["opcode"]
            funct3 = informacoes["funct3"]
            funct7 = informacoes["funct7"]
            shamt_bin = format(shamt, "05b")
            retorno = f"{funct7} {shamt_bin} {rs1} {funct3} {rd} {opcode}"

        case "beq" | "bne":
            rs1 = REGISTRADORES[partes_limpas[1]]
            rs2 = REGISTRADORES[partes_limpas[2]]
            opcode = informacoes["opcode"]
            funct3 = informacoes["funct3"]
            salto  = partes_limpas[3]

            if salto in labels:
                alvo = labels[salto] - pc
            else:
                alvo = pega_numero(salto)

            imm = int_bin(alvo, 13) 
            imm_12   = imm[0]
            imm_10_5 = imm[1:7]
            imm_4_1  = imm[7:11]
            imm_11   = imm[11]
            retorno  = f"{imm_12}{imm_10_5} {rs2} {rs1} {funct3} {imm_4_1}{imm_11} {opcode}"

        case "sw":
            rs2 = REGISTRADORES[partes_limpas[1]]
            imm_val = pega_numero(partes_limpas[2])
            rs1 = REGISTRADORES[partes_limpas[3]]
            opcode = informacoes["opcode"]
            funct3 = informacoes["funct3"]
            imm = int_bin(imm_val, 12)
            imm_11_5 = imm[0:7]
            imm_4_0  = imm[7:12]
            retorno = f"{imm_11_5} {rs2} {rs1} {funct3} {imm_4_0} {opcode}"

        case "lw" | "lhu" | "jalr":
            if instrucao == "jalr" and len(partes_limpas) == 3:
                # jalr rd, rs  (sem offset)
                rd  = REGISTRADORES[partes_limpas[1]]
                imm = "000000000000"
                rs1 = REGISTRADORES[partes_limpas[2]]
            else:
                rd  = REGISTRADORES[partes_limpas[1]]
                imm = int_bin(pega_numero(partes_limpas[2]), 12)
                rs1 = REGISTRADORES[partes_limpas[3]]
            opcode = informacoes["opcode"]
            funct3 = informacoes["funct3"]
            retorno = f"{imm} {rs1} {funct3} {rd} {opcode}"

        case "lui" | "auipc":
            rd     = REGISTRADORES[partes_limpas[1]]
            opcode = informacoes["opcode"]
            if tem_hi:
                imm_val = pega_hi(partes_limpas[2])
            else:
                imm_val = pega_numero(partes_limpas[2])
            imm = int_bin(imm_val, 20)
            retorno = f"{imm} {rd} {opcode}"

        case "jal":
            if len(partes_limpas) == 2:
                rd    = REGISTRADORES["ra"]
                salto = partes_limpas[1]
            else:
                rd    = REGISTRADORES[partes_limpas[1]]
                salto = partes_limpas[2]

            opcode = informacoes["opcode"]

            if salto in labels:
                alvo = labels[salto] - pc
            else:
                alvo = pega_numero(salto)

            imm = int_bin(alvo, 21)  
            imm_20   = imm[0]
            imm_1912 = imm[1:9]
            imm_11   = imm[9]
            imm_101  = imm[10:20]
            retorno  = f"{imm_20}{imm_1912}{imm_11}{imm_101} {rd} {opcode}"

        case _:
            return f"Instrucao {instrucao} nao implementada."

    return bin_hex(retorno)


def main():
    nome_arquivo = input("Arquivo .asm: ").strip()
    arquivo = Path.cwd() / nome_arquivo

    with open(arquivo, 'r') as file:
        linhas = file.readlines()

   
    labels = {}
    contador_pc   = TEXT_BASE   
    contador_data = DATA_BASE   
    campo = ".text"

    for linha in linhas:
        linha_sem_comentario = linha.split('#')[0]
        linha_limpa = linha_sem_comentario.strip()

        if not linha_limpa:
            continue

        if linha_limpa == ".data":
            campo = ".data"
            continue
        elif linha_limpa == ".text":
            campo = ".text"
            continue

        if ":" in linha_limpa:
            partes = linha_limpa.split(':', 1)
            nome_label = partes[0].strip()

            if campo == ".text":
                labels[nome_label] = contador_pc
                instrucao_com_label = partes[1].strip()
                if instrucao_com_label:
                    contador_pc += 4
            elif campo == ".data":
                labels[nome_label] = contador_data
                instrucao_com_label = partes[1].strip()
                if instrucao_com_label:
                    linha_limpa = instrucao_com_label
                else:
                    continue
        else:
            if campo == ".text":
                contador_pc += 4

        if campo == ".data":
            if linha_limpa.startswith(".word"):
                valores = linha_limpa.replace(".word", "").replace(",", " ").split()
                contador_data += 4 * len(valores)
            elif linha_limpa.startswith(".asciz") or linha_limpa.startswith(".string"):
                inicio = linha_sem_comentario.find('"')
                fim    = linha_sem_comentario.rfind('"')
                if inicio != -1 and fim != -1:
                    string_val = linha_sem_comentario[inicio+1:fim]
                    chars = len(string_val) + 1
                    resto = chars % 4
                    chars += (4 - resto) if resto != 0 else 0
                    contador_data += chars


    contador_pc = TEXT_BASE  
    lista_data  = []
    lista_text  = []
    conjunto_instrucoes = []
    campo = ".text"

    for linha in linhas:
        linha_sem_comentario = linha.split('#')[0]
        nova_linha = linha_sem_comentario.strip()

        if not nova_linha:
            continue

        if nova_linha == ".data":
            campo = ".data"
            continue
        elif nova_linha == ".text":
            campo = ".text"
            continue

        if ":" in nova_linha:
            partes = nova_linha.split(":", 1)
            nova_linha = partes[1].strip()
            if not nova_linha:
                continue

        if campo == ".data":
            if nova_linha.startswith(".word"):
                valores = nova_linha.replace(".word", "").replace(",", " ").split()
                for val in valores:
                    lista_data.append(bin_hex(int_bin(int(val, 0), 32)))

            elif nova_linha.startswith(".asciz") or nova_linha.startswith(".string"):
                inicio = linha_sem_comentario.find('"')
                fim    = linha_sem_comentario.rfind('"')
                if inicio != -1 and fim != -1:
                    string_val = linha_sem_comentario[inicio+1:fim]
                    chars = [ord(c) for c in string_val] + [0]
                    while len(chars) % 4 != 0:
                        chars.append(0)
                    for i in range(0, len(chars), 4):
                        word_val = (chars[i+3] << 24) | (chars[i+2] << 16) | (chars[i+1] << 8) | chars[i]
                        lista_data.append(bin_hex(int_bin(word_val, 32)))

        elif campo == ".text":
            instrucao_linha = nova_linha.replace(",", " ").split()[0]
            resultado_hex   = converter_instrucao(instrucao_linha, nova_linha, contador_pc, labels)
            lista_text.append(resultado_hex)
            conjunto_instrucoes.append(nova_linha)
            contador_pc += 4

    arquivo_nome = input("Nome do arquivo final (sem o .mif): ").strip()
    gerar_arquivo_mif(arquivo_nome, lista_text, lista_data, conjunto_instrucoes)
    print(f"Arquivos {arquivo_nome}_data.mif e {arquivo_nome}_text.mif criados com sucesso!")


if __name__ == "__main__":
    main()