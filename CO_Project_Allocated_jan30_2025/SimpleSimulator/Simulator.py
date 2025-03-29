import sys
input_file = r"C:\Users\ajays\OneDrive\Desktop\output.txt"
output_file = r"C:\Users\ajays\OneDrive\Desktop\meow.txt"

registers = {
    "x0": 0, "x1": 0, "x2": 380, "x3": 0,
    "x4": 0, "x5": 0, "x6": 0, "x7": 0,
    "x8": 0, "x9": 0, "x10": 0, "x11": 0, 
    "x12": 0, "x13": 0, "x14": 0, "x15": 0,
    "x16": 0, "x17": 0, "x18": 0, "x19": 0,
    "x20": 0, "x21": 0, "x22": 0, "x23": 0,
    "x24": 0, "x25": 0, "x26": 0, "x27": 0,
    "x28": 0, "x29": 0, "x30": 0, "x31": 0
    }

data_memory = {
    0x00010000: 0b00000000000000000000000000000000, 0x00010004: 0b00000000000000000000000000000000, 0x00010008: 0b00000000000000000000000000000000, 0x0001000C: 0b00000000000000000000000000000000,
    0x00010010: 0b00000000000000000000000000000000, 0x00010014: 0b00000000000000000000000000000000, 0x00010018: 0b00000000000000000000000000000000, 0x0001001C: 0b00000000000000000000000000000000,
    0x00010020: 0b00000000000000000000000000000000, 0x00010024: 0b00000000000000000000000000000000, 0x00010028: 0b00000000000000000000000000000000, 0x0001002C: 0b00000000000000000000000000000000,
    0x00010030: 0b00000000000000000000000000000000, 0x00010034: 0b00000000000000000000000000000000, 0x00010038: 0b00000000000000000000000000000000, 0x0001003C: 0b00000000000000000000000000000000,
    0x00010040: 0b00000000000000000000000000000000, 0x00010044: 0b00000000000000000000000000000000, 0x00010048: 0b00000000000000000000000000000000, 0x0001004C: 0b00000000000000000000000000000000,
    0x00010050: 0b00000000000000000000000000000000, 0x00010054: 0b00000000000000000000000000000000, 0x00010058: 0b00000000000000000000000000000000, 0x0001005C: 0b00000000000000000000000000000000,
    0x00010060: 0b00000000000000000000000000000000, 0x00010064: 0b00000000000000000000000000000000, 0x00010068: 0b00000000000000000000000000000000, 0x0001006C: 0b00000000000000000000000000000000,
    0x00010070: 0b00000000000000000000000000000000, 0x00010074: 0b00000000000000000000000000000000, 0x00010078: 0b00000000000000000000000000000000, 0x0001007C: 0b00000000000000000000000000000000
    }

memory_addresses = {
    "0x10000" : 0,  
    "0x10004" : 0,  
    "0x10008" : 0, 
    "0x1000C" : 0,  
    "0x10010" : 0, 
    "0x10014" : 0,  
    "0x10018" : 0,
    "0x1001C" : 0, 
    "0x10020" : 0,  
    "0x10024" : 0,  
    "0x10028" : 0,  
    "0x1002C" : 0,  
    "0x10030" : 0,  
    "0x10034" : 0,  
    "0x10038" : 0,  
    "0x1003C" : 0,  
    "0x10040" : 0,  
    "0x10044" : 0,  
    "0x10048" : 0,  
    "0x1004C" : 0,  
    "0x10050" : 0,  
    "0x10054" : 0,  
    "0x10058" : 0,  
    "0x1005C" : 0,  
    "0x10060" : 0,  
    "0x10064" : 0,  
    "0x10068" : 0,  
    "0x1006C" : 0,  
    "0x10070" : 0,  
    "0x10074" : 0,  
    "0x10078" : 0,  
    "0x1007C" : 0  
}

def trace(pc):    
    return (f"0b{format(pc, '032b')} "f"0b{format(registers['x0'], '032b')} "f"0b{format(registers['x1'], '032b')} "f"0b{format(registers['x2'], '032b')} "f"0b{format(registers['x3'], '032b')} "f"0b{format(registers['x4'], '032b')} "f"0b{format(registers['x5'], '032b')} "f"0b{format(registers['x6'], '032b')} "f"0b{format(registers['x7'], '032b')} "f"0b{format(registers['x8'], '032b')} "f"0b{format(registers['x9'], '032b')} "f"0b{format(registers['x10'], '032b')} "f"0b{format(registers['x11'], '032b')} "f"0b{format(registers['x12'], '032b')} "f"0b{ format(registers['x13'], '032b')} "f"0b{format(registers['x14'], '032b')} "f"0b{format(registers['x15'], '032b')} "f"0b{format(registers['x16'], '032b')} "f"0b{format(registers['x17'], '032b')} "f"0b{format(registers['x18'], '032b')} "f"0b{format(registers['x19'], '032b')} "f"0b{ format(registers['x20'], '032b')} "f"0b{format(registers ['x21'], '032b')} "f"0b{format(registers['x22'], '032b')} "f"0b{format(registers['x23'], '032b')} "f"0b{format(registers['x24'], '032b')} " f"0b{format(registers['x25'], '032b')} "f"0b{format(registers ['x26'], '032b')} "f"0b{format (registers['x27'], '032b')} "f"0b{format(registers['x28'], '032b')} "f"0b{format(registers['x29'], '032b')} "f"0b{format(registers['x30'], '032b')} "f"0b{format(registers['x31'], '032b')} ") 

def type_checker(opcode):
    if opcode == "0110011":
        type = "r"
    elif opcode in ["0000011", "0010011", "1100111"]:
        type = "i"
    elif opcode == "0100011":
        type = "s"
    elif opcode == "1100011":
        type = "b"
    elif opcode == "1101111":
        type = "j"
    else:
        type = "Unkown Instruction"
    return type

def binary_12bit_to_decimal(binary_str):
    return int(binary_str, 2) - ((binary_str[0] == '1') << 12)

#R Type Instructions
def add(rd, rs1 ,rs2):
    registers[rd] = registers[rs1] + registers[rs2]

def sub(rd, rs1 ,rs2):
    registers[rd] = registers[rs1] - registers[rs2]

def or1(rd, rs1 ,rs2):
    registers[rd] = registers[rs1] | registers[rs2]

def and1(rd, rs1 ,rs2):
    registers[rd] = registers[rs1] & registers[rs2]

def slt(rd, rs1 ,rs2):
    if registers[rs1] < registers[rs2]:
        registers[rd] = 1
    else:
        registers[rd] = 0

def srl(rd, rs1, rs2):
    registers[rd] = registers[rs1] >> registers[rs2]

#I Type instructions
def addi(rd, rs1, imm):
    registers[rd] = registers[rs1] + int(imm)

#encodings 
def r_type(line):
    funct7 = line[:7]
    rs2 = line[7:12]
    rs1 = line[12:17]
    func3 = line[17:20]
    rd = line[20:25]
    rd = "x" + str(int(rd, 2))
    rs1 = "x" + str(int(rs1, 2))
    rs2 = "x" + str(int(rs2, 2))
    if funct7 == "0100000" and func3 == "000":
        operation = "sub"
    elif funct7 == "0000000" and func3 == "000":
        operation = "add"
    elif funct7 == "0000000" and func3 == "010":
        operation = "slt"
    elif funct7 == "0000000" and func3 == "101":
        operation = "srl"
    elif funct7 == "0000000" and func3 == "110":
        operation = "or"
    elif funct7 == "0000000" and func3 == "111":
        operation = "and"
           
    instruction = operation + " " + rd + "," + rs1 + "," + rs2
    return instruction

def i_type(line):
    imm = line[:12]
    imm = str(binary_12bit_to_decimal(imm))
    rs1 = line[12:17]
    func3 = line[17:20]
    rd = line[20:25]
    opcode = line[-7:]
    rd = "x" + str(int(rd, 2))
    rs1 = "x" + str(int(rs1, 2))
    if func3 == "010" and opcode == "0000011":
        operation = "lw"
        instruction = operation + " " + rd + ", " + imm + "(" + rs1 + ")"
    elif func3 == "000" and opcode == "0010011":
        operation = "addi"
        instruction = operation + " " + rd + "," + rs1 + ",#" + imm
    elif func3 == "000" and opcode == "1100111":
        operation = "jalr"
        instruction = operation + " " + rd + "," + rs1 + "," + imm    
    
    return (instruction)

def s_type(line):
    imm1 = line[:7]
    rs2 = line[7:12]
    rs1 = line[12:17]
    func3 = line[17:20]
    imm2 = line[20:25]
    opcode = line[25:32]
    imm = imm1 + imm2
    rs2 = "x" + str(int(rs2, 2))
    rs1 = "x" + str(int(rs1, 2))
    imm = str(binary_12bit_to_decimal(imm))
    if opcode == "0100011" and func3 == "010":
        operation = "sw"
        instruction = operation + " " + rs2 + ", " + imm + "(" + rs1 + ")"
    
    return instruction

def b_type(line):
    imm1 = line[0:1]
    imm2 = line[1:7]
    rs2 = line[7:12]
    rs1 = line[12:17]
    func3 = line[17:20]
    imm3 = line[20:24]
    imm4 = line[24:25]
    opcode = line[25:32]
    rs2 = "x" + str(int(rs2, 2))
    rs1 = "x" + str(int(rs1, 2))
    imm = imm1 + imm4 + imm2 + imm3
    imm = str(binary_12bit_to_decimal(imm))
    if opcode == "1100011" and func3 == "000":
        operation = "beq"
    elif opcode == "1100011" and func3 == "001":
        operation = "bne"
    elif opcode == "1100011" and func3 == "100":
        operation = "blt"

    instruction = operation + " " + rs1 + "," + rs2 + "," + imm
    return instruction

def j_type(line):
    imm1 = line[0:1]
    imm2 = line[1:9]
    imm3 = line[9:10]
    imm4 = line[10:20]
    rd = line[20:25]
    opcode = line[25:32]
    rd = "x" + str(int(rd, 2))
    imm = imm1 + imm4 + imm3 + imm2
    imm = str(binary_12bit_to_decimal(imm))
    if opcode == "1101111":
        operation = "jal"
    
    instruction = operation + " " + rd + "," + imm
    return instruction

address = {}

with open(input_file, 'r') as f:
    x = 0x0004
    pc = 0
    for line in f:
        address[x] = pc
        x += 4
        pc += 4


with open(input_file, "r") as f:
    pc = 4
    for line in f:
        line = line.strip()
        opcode = line[-7:]
        type = type_checker(opcode)
        if type == "r":
            instruction = r_type(line)
        elif type == "i":
            instruction = i_type(line)
        elif type == "s":
            instruction = s_type(line)
        elif type == "b":
            instruction = b_type(line)
        elif type == "j":
            instruction = j_type(line)
        x = instruction
        address[pc] = x
        x = trace(pc)
        pc+=4
t = pc

with open(output_file, "w") as f:
    pc = 4
    while (pc < t):
        x = address[pc]
        x = x.replace(',', ' ')
        x = x.replace('#', '')
        x = x.split(" ")
        print(x)
        if x[0] == "srl":
            srl(x[1], x[2], x[3])
        elif x[0] == "slt":
            slt(x[1], x[2], x[3])
        elif x[0] == "addi":
            addi(x[1], x[2], x[3])
        f.write(trace(pc)+"\n")
        pc += 4
    for x in data_memory:
        f.write("0x"+format(x, '08X')+":0b"+format(data_memory[x], '032b')+"\n")



for t in address:
    print(t, address[t])
