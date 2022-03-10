# Extract exports & demangle it
from __future__ import print_function
import frida
from cppmangle import demangle, cdecl_sym
##from itanium_demangler import parse as demangle

session = frida.attach("PwnAdventure3-Win32-Shipping.exe")
script = session.create_script("""
	 //send(Module.findBaseAddress('GameLogic.dll'));
	 //var exports = Module.enumerateExports('GameLogic.dll');
      var exports = Module.enumerateExports('GameLogic.pdb');
      for (var i = 0; i < exports.length; i++) {
        send(exports[i].name);
    }
    
    var processArr = Process.enumerateModules();
    for (var i = 0; i < processArr.length; i++) {
          var exports = Module.enumerateExports(processArr[i].name);
          for (var j = 0; j < exports.length; j++) {
            send(exports[j].name);
          }
          
    }
""")

def on_message(message, data):
    try:
        print(message["payload"] + " - " + cdecl_sym(demangle(message["payload"])))
    except:
        print(message["payload"])
script.on('message', on_message)
script.load()