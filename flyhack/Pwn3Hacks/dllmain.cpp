// referred from videos by liveoverflow and articles by guided hacking
#include "pch.h"
#include "stdafx.h"
#include <iostream>
#include "mem.h"
#include "proc.cpp"
#include <concepts>
#include "dllmain.h"
#include "geom.h"

DWORD WINAPI HackThread(HMODULE hModule) {
    //Create Console
    AllocConsole();
    FILE* f = new FILE;
    freopen_s(&f, "CONOUT$", "w", stdout);

    std::cout << "Starting PwnAdventure3 Hack\n";
    std::cout << "Injection worked\n";
    std::cout << "Process ID is: " << GetCurrentProcessId() << std::endl;

    bool fly_hack = false;

    //GET EXE and DLL BASE ADDRESSES
    uintptr_t exe_base_address = (uintptr_t)GetModuleHandle(L"PwnAdventure3-Win32-Shipping.exe");
    uintptr_t dll_base_address = (uintptr_t)GetModuleHandle(L"GameLogic.dll");

    //store camera update value
    BYTE restore[7] = { 0 };
    mem::Patch(restore, (BYTE*)(exe_base_address + 0x8DB2D8), 7);

    //for declaring variables that can store camera and player positions
    struct vector_3 { float x, y, z; };
    //for decalring variables that can store camera angles
    struct vector_4 { float w, x, y, z; };

    //get the camera position values x,y,z
    vector_3* camera_position = (vector_3*)mem::FindAddress(exe_base_address + 0x18fcd60, { 0x20, 0x238, 0x400, 0x90 });
    //get the position of the player in x,y,z
    vector_3* old_position = (vector_3*)mem::FindAddress(dll_base_address + 0x97E48, { 0x148, 0x4, 0x114, 0x90 });
    //get the camera angles w,x,y,z
    vector_4* quaternions = (vector_4*)mem::FindAddress(exe_base_address + 0x18fcd60, { 0x20, 0x238, 0x400, 0x80 });
    vector_3 tmp;
   
    float speed = 0.1f;
    float step = 0.1f;

    while (true) {

        if (GetAsyncKeyState(VK_LCONTROL) & 1)
        {
            fly_hack = !fly_hack;
            std::cout << "FlyHack enabled?" << fly_hack << std::endl;
            if (fly_hack) {
                mem::Nop((BYTE*)(exe_base_address + 0x8DB2D8), 7);
            }
            else {
                mem::Patch((BYTE*)(exe_base_address + 0x8DB2D8), restore, 7);
            }
        }

        if (fly_hack)
        {
            if (speed < step) {
                speed = step;
            }
            speed -= step;

            //move camera in mouse pointer direction
            if (GetAsyncKeyState(VK_RBUTTON)) {
                tmp.x = 1 - 2 * (quaternions->y * quaternions->y + quaternions->z * quaternions->z); 
                tmp.y = 2 * (quaternions->x * quaternions->y + quaternions->w * quaternions->z);
                tmp.z = 2 * (quaternions->x * quaternions->z - quaternions->w * quaternions->y);

                camera_position->x -= tmp.x * speed;
                camera_position->y -= tmp.y * speed;
                camera_position->z -= tmp.z * speed;
                speed += step * 2;
            }

            //move camera forward
            if (GetAsyncKeyState('W') & 1) {
                tmp.x = 1 - 2 * (quaternions->y * quaternions->y + quaternions->z * quaternions->z);
                tmp.y = 2 * (quaternions->x * quaternions->y + quaternions->w * quaternions->z);
                tmp.z = 2 * (quaternions->x * quaternions->z - quaternions->w * quaternions->y);
                float mul = 0.8 / sqrt(tmp.x * tmp.x + tmp.y * tmp.y);

                camera_position->x += tmp.x * speed * mul;
                camera_position->y += tmp.y * speed * mul;
                camera_position->z += 0;
                speed += step * 2;
            }

            //move camera to the left
            if (GetAsyncKeyState('A') & 1) {
                tmp.x = 1 - 2 * (quaternions->y * quaternions->y + quaternions->z * quaternions->z);
                tmp.y = 2 * (quaternions->x * quaternions->y + quaternions->w * quaternions->z);
                tmp.z = 2 * (quaternions->x * quaternions->z - quaternions->w * quaternions->y);
                float mul = 0.8 / sqrt(tmp.x * tmp.x + tmp.y * tmp.y);

                camera_position->x += tmp.y * speed * mul;
                camera_position->y += -tmp.x * speed * mul;
                camera_position->z += 0;
                speed += step * 2;
            }

            //move camera backwards
            if (GetAsyncKeyState('S') & 1) {
                tmp.x = 1 - 2 * (quaternions->y * quaternions->y + quaternions->z * quaternions->z);
                tmp.y = 2 * (quaternions->x * quaternions->y + quaternions->w * quaternions->z);
                tmp.z = 2 * (quaternions->x * quaternions->z - quaternions->w * quaternions->y);
                float mul = 0.8 / sqrt(tmp.x * tmp.x + tmp.y * tmp.y);

                camera_position->x += -tmp.x * speed * mul;
                camera_position->y += -tmp.y * speed * mul;
                camera_position->z += 0;
                speed += step * 2;
            }

            //move camera to the right
            if (GetAsyncKeyState('D') & 1 ) {
                tmp.x = 1 - 2 * (quaternions->y * quaternions->y + quaternions->z * quaternions->z);
                tmp.y = 2 * (quaternions->x * quaternions->y + quaternions->w * quaternions->z);
                tmp.z = 2 * (quaternions->x * quaternions->z - quaternions->w * quaternions->y);
                float mul = 0.8 / sqrt(tmp.x * tmp.x + tmp.y * tmp.y);

                camera_position->x += -tmp.y * speed * mul;
                camera_position->y += tmp.x * speed * mul;
                camera_position->z += 0;
                speed += step * 2;
            }
            
            //move camera to upward
            if (GetAsyncKeyState(VK_SPACE)) {
                camera_position->z += speed;
                speed += step * 2;
            }

            //move camera to downward
            if (GetAsyncKeyState(VK_SHIFT)) {
                camera_position->z -= speed;
                speed += step * 2;
            }

            //maximum speed limit
            if (speed > 15.0f) {
                speed = 15.0f;
            }

            //teleport player to where the camera is at
            if (GetAsyncKeyState('L') & 1) {
                old_position->x = camera_position->x;
                old_position->y = camera_position->y;
                old_position->z = camera_position->z;
            }
        }
    }

    fclose(f);
    FreeConsole();
    FreeLibraryAndExitThread(hModule, 0);
    return 0;
}

BOOL APIENTRY DllMain(HMODULE hModule,
    DWORD  ul_reason_for_call,
    LPVOID lpReserved
)
{
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH:
    {
        HANDLE thread = CreateThread(nullptr, 0, (LPTHREAD_START_ROUTINE)HackThread, hModule, 0, nullptr);
        if (thread)
            CloseHandle(thread);
    }
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}