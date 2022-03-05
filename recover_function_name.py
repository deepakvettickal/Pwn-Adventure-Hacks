import idaapi

handler_function_addr = 0xb5c130

first_xref_addr = idaapi.get_first_fcref_to(handler_function_addr)
next_xref_addr = first_xref_addr

def get_string(addr):
    #print(addr)
    string =""
    data_byte = idaapi.get_byte(addr)
    while data_byte:
        string = string +chr(data_byte)
        addr = addr + 1
        data_byte = idaapi.get_byte(addr)
    return string


while next_xref_addr!=0xffffffff:
    #print("a")
    function_addr = idaapi.get_dword(next_xref_addr-0xb+1)
    function_name_offset = idaapi.get_dword(next_xref_addr-0xb+6)
    function_name = get_string(function_name_offset)+str(function_addr)

    #rename
    assert idaapi.set_name(function_addr,function_name)
    print(f"addr :{function_name_offset} {function_name} ")
    next_xref_addr = idaapi.get_next_fcref_to(handler_function_addr, next_xref_addr)
