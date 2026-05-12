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

    "t0": "00101",
    "t1": "00110",
    "t2": "00111",

    "s0": "01000",
    "fp": "01000",
    "s1": "01001",

    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",

    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",

    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6": "11111",
}

BASE_TEXTO = 0x00400000
BASE_DADOS = 0x10010000


def inteiro_para_binario(numero, tamanho):
    mascara = (1 << tamanho) - 1
    return format(numero & mascara, f"0{tamanho}b")


def binario_para_hex(bin_str):
    bin_str = bin_str.replace(" ", "")
    return hex(int(bin_str, 2))[2:].upper().zfill(8)


def gerar_arquivo_mif(nome_arquivo, conjunto_texto, conjunto_dados, instrucoes):

    with open(f"{nome_arquivo}_data.mif", "w") as f:

        f.write("DEPTH = 32768;\n")
        f.write("WIDTH = 32;\n")
        f.write("ADDRESS_RADIX = HEX;\n")
        f.write("DATA_RADIX = HEX;\n")
        f.write("CONTENT\n")
        f.write("BEGIN\n")

        for i, valor in enumerate(conjunto_dados):
            f.write(f"{i:08x} : {valor.lower()};\n")

        for i in range(len(conjunto_dados), 1024):
            f.write(f"{i:08x} : 00000000;\n")

        f.write("END;\n")

    with open(f"{nome_arquivo}_text.mif", "w") as f:

        f.write("DEPTH = 16384;\n")
        f.write("WIDTH = 32;\n")
        f.write("ADDRESS_RADIX = HEX;\n")
        f.write("DATA_RADIX = HEX;\n")
        f.write("CONTENT\n")
        f.write("BEGIN\n")

        for i, valor in enumerate(conjunto_texto):

            f.write(f"{i:08x} : {valor.lower()};")

            if i < len(instrucoes):
                f.write(f"    % {instrucoes[i]} %")

            f.write("\n")

        f.write("END;\n")


def converter_instrucao(instrucao, linha, pc, rotulos):

    linha = linha.replace(",", " ")
    linha = linha.replace("(", " ")
    linha = linha.replace(")", " ")

    tem_hi = "%hi" in linha
    tem_lo = "%lo" in linha

    linha = linha.replace("%hi", "")
    linha = linha.replace("%lo", "")

    partes = linha.split()

    if instrucao not in INSTRUCOES:
        return "INSTRUCAO_INVALIDA"

    info = INSTRUCOES[instrucao]

    def pega_numero(valor):

        if valor in rotulos:
            return rotulos[valor]

        try:
            return int(valor, 0)
        except:
            return 0

    def pega_hi(valor):

        endereco = pega_numero(valor)

        lo = endereco & 0xFFF
        hi = endereco >> 12

        if lo >= 0x800:
            hi += 1

        return hi

    def pega_lo(valor):

        endereco = pega_numero(valor)

        lo = endereco & 0xFFF

        if lo >= 0x800:
            lo -= 0x1000

        return lo

    match instrucao:

        case "add" | "sub" | "and" | "or" | "xor" | "slt" | "sll" | "srl":

            rd = REGISTRADORES[partes[1]]
            rs1 = REGISTRADORES[partes[2]]
            rs2 = REGISTRADORES[partes[3]]

            funct7 = info["funct7"]
            funct3 = info["funct3"]
            opcode = info["opcode"]

            retorno = f"{funct7} {rs2} {rs1} {funct3} {rd} {opcode}"

        case "addi" | "andi" | "ori" | "xori" | "slti":

            rd = REGISTRADORES[partes[1]]
            rs1 = REGISTRADORES[partes[2]]

            if tem_lo:
                imediato = pega_lo(partes[3])
            else:
                imediato = pega_numero(partes[3])

            imm = inteiro_para_binario(imediato, 12)

            funct3 = info["funct3"]
            opcode = info["opcode"]

            retorno = f"{imm} {rs1} {funct3} {rd} {opcode}"

        case "slli" | "srli" | "srai":

            rd = REGISTRADORES[partes[1]]
            rs1 = REGISTRADORES[partes[2]]

            shamt = int(partes[3], 0) & 0x1F

            funct7 = info["funct7"]
            funct3 = info["funct3"]
            opcode = info["opcode"]

            shamt_bin = format(shamt, "05b")

            retorno = f"{funct7} {shamt_bin} {rs1} {funct3} {rd} {opcode}"

        case "lw" | "lhu" | "jalr":

            opcode = info["opcode"]
            funct3 = info["funct3"]

            if instrucao == "jalr" and len(partes) == 3:

                rd = REGISTRADORES[partes[1]]
                rs1 = REGISTRADORES[partes[2]]
                imm = "000000000000"

            else:

                rd = REGISTRADORES[partes[1]]
                rs1 = REGISTRADORES[partes[3]]

                imediato = pega_numero(partes[2])

                imm = inteiro_para_binario(imediato, 12)

            retorno = f"{imm} {rs1} {funct3} {rd} {opcode}"

        case "sw":

            rs2 = REGISTRADORES[partes[1]]
            rs1 = REGISTRADORES[partes[3]]

            imediato = pega_numero(partes[2])

            imm = inteiro_para_binario(imediato, 12)

            imm_11_5 = imm[0:7]
            imm_4_0 = imm[7:12]

            funct3 = info["funct3"]
            opcode = info["opcode"]

            retorno = f"{imm_11_5} {rs2} {rs1} {funct3} {imm_4_0} {opcode}"

        case "beq" | "bne":

            rs1 = REGISTRADORES[partes[1]]
            rs2 = REGISTRADORES[partes[2]]

            destino = partes[3]

            if destino in rotulos:
                offset = rotulos[destino] - pc
            else:
                offset = pega_numero(destino)

            imm = inteiro_para_binario(offset, 13)

            imm_12 = imm[0]
            imm_10_5 = imm[2:8]
            imm_4_1 = imm[8:12]
            imm_11 = imm[1]

            funct3 = info["funct3"]
            opcode = info["opcode"]

            retorno = f"{imm_12}{imm_10_5} {rs2} {rs1} {funct3} {imm_4_1}{imm_11} {opcode}"

        case "lui" | "auipc":

            rd = REGISTRADORES[partes[1]]

            if tem_hi:
                imediato = pega_hi(partes[2])
            else:
                imediato = pega_numero(partes[2])

            imm = inteiro_para_binario(imediato, 20)

            opcode = info["opcode"]

            retorno = f"{imm} {rd} {opcode}"

        case "jal":

            opcode = info["opcode"]

            if len(partes) == 2:
                rd = REGISTRADORES["ra"]
                destino = partes[1]
            else:
                rd = REGISTRADORES[partes[1]]
                destino = partes[2]

            if destino in rotulos:
                offset = rotulos[destino] - pc
            else:
                offset = pega_numero(destino)

            imm = inteiro_para_binario(offset, 21)

            imm_20 = imm[0]
            imm_10_1 = imm[10:20]
            imm_11 = imm[9]
            imm_19_12 = imm[1:9]

            retorno = f"{imm_20}{imm_10_1}{imm_11}{imm_19_12} {rd} {opcode}"

        case _:
            return "INSTRUCAO_NAO_IMPLEMENTADA"

    return binario_para_hex(retorno)


def main():

    nome_arquivo = input("Arquivo .asm: ").strip()

    caminho = Path.cwd() / nome_arquivo

    with open(caminho, "r") as f:
        linhas = f.readlines()

    rotulos = {}

    pc = BASE_TEXTO
    dados = BASE_DADOS

    secao = ".text"

    for linha in linhas:

        linha_sem_comentario = linha.split("#")[0]
        linha_limpa = linha_sem_comentario.strip()

        if not linha_limpa:
            continue

        if linha_limpa == ".data":
            secao = ".data"
            continue

        if linha_limpa == ".text":
            secao = ".text"
            continue

        if ":" in linha_limpa:

            partes = linha_limpa.split(":", 1)

            nome_rotulo = partes[0].strip()

            if secao == ".text":

                rotulos[nome_rotulo] = pc

                resto = partes[1].strip()

                if resto:
                    pc += 4

            else:

                rotulos[nome_rotulo] = dados

                resto = partes[1].strip()

                if resto:
                    linha_limpa = resto
                else:
                    continue

        else:

            if secao == ".text":
                pc += 4

        if secao == ".data":

            if linha_limpa.startswith(".word"):

                valores = linha_limpa.replace(".word", "")
                valores = valores.replace(",", " ").split()

                dados += 4 * len(valores)

            elif linha_limpa.startswith(".asciz") or linha_limpa.startswith(".string"):

                inicio = linha_sem_comentario.find('"')
                fim = linha_sem_comentario.rfind('"')

                if inicio != -1 and fim != -1:

                    string = linha_sem_comentario[inicio + 1:fim]

                    tamanho = len(string) + 1

                    while tamanho % 4 != 0:
                        tamanho += 1

                    dados += tamanho

    pc = BASE_TEXTO

    lista_texto = []
    lista_dados = []
    instrucoes = []

    secao = ".text"

    for linha in linhas:

        linha_sem_comentario = linha.split("#")[0]
        linha_limpa = linha_sem_comentario.strip()

        if not linha_limpa:
            continue

        if linha_limpa == ".data":
            secao = ".data"
            continue

        if linha_limpa == ".text":
            secao = ".text"
            continue

        if ":" in linha_limpa:

            partes = linha_limpa.split(":", 1)

            linha_limpa = partes[1].strip()

            if not linha_limpa:
                continue

        if secao == ".data":

            if linha_limpa.startswith(".word"):

                valores = linha_limpa.replace(".word", "")
                valores = valores.replace(",", " ").split()

                for valor in valores:

                    inteiro = int(valor, 0)

                    lista_dados.append(
                        binario_para_hex(
                            inteiro_para_binario(inteiro, 32)
                        )
                    )

            elif linha_limpa.startswith(".asciz") or linha_limpa.startswith(".string"):

                inicio = linha_sem_comentario.find('"')
                fim = linha_sem_comentario.rfind('"')

                if inicio != -1 and fim != -1:

                    string = linha_sem_comentario[inicio + 1:fim]

                    chars = [ord(c) for c in string] + [0]

                    while len(chars) % 4 != 0:
                        chars.append(0)

                    for i in range(0, len(chars), 4):

                        word = (
                            (chars[i + 3] << 24)
                            | (chars[i + 2] << 16)
                            | (chars[i + 1] << 8)
                            | chars[i]
                        )

                        lista_dados.append(
                            binario_para_hex(
                                inteiro_para_binario(word, 32)
                            )
                        )

        elif secao == ".text":

            instrucao = linha_limpa.replace(",", " ").split()[0]

            hex_instrucao = converter_instrucao(
                instrucao,
                linha_limpa,
                pc,
                rotulos
            )

            lista_texto.append(hex_instrucao)
            instrucoes.append(linha_limpa)

            pc += 4

    nome_saida = input("Nome do arquivo final: ").strip()

    gerar_arquivo_mif(
        nome_saida,
        lista_texto,
        lista_dados,
        instrucoes
    )

    print(
        f"Arquivos {nome_saida}_data.mif e "
        f"{nome_saida}_text.mif criados com sucesso!"
    )


if __name__ == "__main__":
    main()