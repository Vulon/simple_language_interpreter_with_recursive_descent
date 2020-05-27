import sys

def readFile(filename : str):
    arr = []
    with open(filename, mode="rb") as file:
        byte = file.read(1)
        while byte != b"":
            arr.append(byte)
            byte = file.read(1)
    return arr

order = sys.byteorder
data = readFile("my_program.obj")
# data = readFile("example.obj")
print("bytes count: ", len(data))
symbols_count = int.from_bytes(b''.join(data[12 : 16]), byteorder=order)
print("Header: symbols count: ", symbols_count)
table_bias = int.from_bytes(b''.join(data[8 : 12]), byteorder=order)
print("Header: Symbol table bias: ", table_bias)
name_table_pos = table_bias + 18 * symbols_count
print("Name table position", name_table_pos)
name_table_size = int.from_bytes(b''.join(data[name_table_pos: name_table_pos + 4]), byteorder=order)
print("Name table size: ", name_table_size)
name_table = b''.join(data[name_table_pos + 4: name_table_pos + name_table_size])

symbol_table_names = []
string_table_biases = []
start_pos = table_bias
for i in range(symbols_count):
    symbol_name = b''.join(data[start_pos: start_pos + 8])
    print("parse entry: ", symbol_name)
    if symbol_name[: 4] == b'\x00\x00\x00\x00':
        bias = int.from_bytes(symbol_name[4:], byteorder=order)
        print("Bias: ", bias)
        string_table_biases.append(bias)
    else:
        symbol_table_names.append(symbol_name.replace(b'\x00', b'').decode())
    start_pos += 18
string_table_names = []
for bias in string_table_biases:
    temp = []
    index = name_table_pos + bias
    while(index < len(data)) and (data[index] != b'\x00'):
        temp.append(data[index])
        index += 1
    string_table_names.append(b''.join(temp).decode())

print("Symbol Table Names: ", symbol_table_names)
print("String Table names: ", string_table_names)



