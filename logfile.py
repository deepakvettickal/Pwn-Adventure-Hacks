# Log chat

from __future__ import print_function
import frida
import sys

session = frida.attach("PwnAdventure3-Win32-Shipping.exe")
script = session.create_script("""
         //Find "Player::Chat"
         //send(Process.enumerateModules()[0])
        //var chat = Module.findExportByName("PwnAdventure3-Win32-Shipping", "?Chat@Player@@UAEXPBD@Z");
         var chat = DebugSymbol.load('GameLogic.dll')
         var chat = DebugSymbol.getFunctionByName('Player::Chat');
         //console.log(chat)
         //##var chat = Module.findBaseAddress("GameLogic.dll").add('0x00401000');
         //send(chat);
         //console.log("Player::Chat() at  address: " + chat);
         //send(chat);
         //var processArr = Process.enumerateModules();
         //for (var i = 0; i < processArr.length; i++) {
         // send(processArr[i].name);
         //}
         //send(DebugSymbol.fromAddress("0x0401000"))
         Interceptor.attach(chat, {
             onEnter: function (args) { // 0 => this; 1 => cont char* (our text)
                var chatMsg = Memory.readCString(args[1]);
                console.log("[Chat]: " + chatMsg);
                 //this.buf = args[1];
                 //this.len = parseInt(args[2]);
                 //log("ssl3_write(" + this.buf.toString() + ", " + this.len.toString() + ")");
                 //var bbuf = Memory.readByteArray(this.buf, this.len);
                 send(bbuf)
                
             }
         });    
 """)


def on_message(message, data):
  print('ye')
  print(message)


script.on('message', on_message)
script.load()
sys.stdin.read()