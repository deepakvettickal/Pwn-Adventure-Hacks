// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"
#include <Windows.h>
#include <iostream> 


// This method defines a threat that will run concurrently with the game
DWORD WINAPI MyThread(HMODULE hModule)
{
	// The following 3 lines enable a writable console
	// We don't actually need a console here, but it is very useful to print debugging information to. 
	AllocConsole();
	FILE* f = new FILE;
	freopen_s(&f, "CONOUT$", "w", stdout);

	std::cout << "Injection worked\n";
	std::cout << "Process ID is: " << GetCurrentProcessId() << std::endl;
	// We can see by looking at the process ID in process explorer that this code is being run by the process it was injected into. 


	// From cheat engine analysis we know that
	// player positionx_coord is at memory address: [[[["PwnAdventure3-Win32-Shipping.exe"+018FCD60] + 20 ] + 238 ] + 280 ] + 90 
	// player positiony_coord is at memory address: [[[["PwnAdventure3-Win32-Shipping.exe"+018FCD60] + 20 ] + 238 ] + 280 ] + 94
	// player positionz_coord is at memory address: [[[["PwnAdventure3-Win32-Shipping.exe"+018FCD60] + 20 ] + 238 ] + 280 ] + 98

	// player's camera angle1 is at memory address: [[[[[["PwnAdventure3-Win32-Shipping.exe"+018FCD60] + 20 ] + 238 ] + 280 ] + E0 ] + 04 ] + 80
	// player's camera angle2 is at memory address: [[[[[["PwnAdventure3-Win32-Shipping.exe"+018FCD60] + 20 ] + 238 ] + 280 ] + E0 ] + 04 ] + 84
	// player's camera angle3 is at memory address: [[[[[["PwnAdventure3-Win32-Shipping.exe"+018FCD60] + 20 ] + 238 ] + 280 ] + E0 ] + 04 ] + 88
	// player's camera angle4 is at memory address: [[[[[["PwnAdventure3-Win32-Shipping.exe"+018FCD60] + 20 ] + 238 ] + 280 ] + E0 ] + 04 ] + 8C

	// player's camera position1 is at memory address: [[[[[["PwnAdventure3-Win32-Shipping.exe"+018FCD60] + 20 ] + 238 ] + 280 ] + E0 ] + 04 ] + 90
	// player's camera position1 is at memory address: [[[[[["PwnAdventure3-Win32-Shipping.exe"+018FCD60] + 20 ] + 238 ] + 280 ] + E0 ] + 04 ] + 94
	// player's camera position1 is at memory address: [[[[[["PwnAdventure3-Win32-Shipping.exe"+018FCD60] + 20 ] + 238 ] + 280 ] + E0 ] + 04 ] + 98
	// This code follows that pointer path

	uintptr_t PwnAventAddr = (uintptr_t)GetModuleHandle(L"PwnAdventure3-Win32-Shipping.exe");
	printf("PwnAventAddr: %p\n", PwnAventAddr);
	uintptr_t firstStep = *(uintptr_t*)(PwnAventAddr + 0x18FCD60);
	printf("PwnAventAddr + 0x18FCD60 = %p has value %p\n", PwnAventAddr + 0x18FCD60, firstStep);
	uintptr_t secondStep = *(uintptr_t*)(firstStep + 0x20);
	printf("firstStep + 0x20 = %p has value %p\n", firstStep + 0x20, secondStep);
	uintptr_t thirdStep = *(uintptr_t*)(secondStep + 0x238);
	printf("secondStep + 0x238 = %p has value %p\n", secondStep + 0x238, thirdStep);
	uintptr_t forthStep = *(uintptr_t*)(thirdStep + 0x280);
	printf("thirdStep + 0x280 = %p has value %p\n", thirdStep + 0x280, forthStep);

	uintptr_t fiveStep = *(uintptr_t*)(forthStep + 0xE0);
	printf("forthStep + 0xE0 = %p has value %p\n", forthStep + 0xE0, fiveStep);

	uintptr_t sixStep = *(uintptr_t*)(fiveStep + 0x04);
	printf("fiveStep + 0x04 = %p has value %p\n", fiveStep + 0x04, sixStep);



	float* camera1_Adress = (float*)(sixStep + 0x80); //camera angle1
	float camera1 = *camera1_Adress;

	float* camera2_Adress = (float*)(sixStep + 0x84);//camera angle2
	float camera2 = *camera2_Adress;

	float* camera3_Adress = (float*)(sixStep + 0x88);//camera angle3
	float camera3 = *camera3_Adress;

	float* camera4_Adress = (float*)(sixStep + 0x8C);//camera angle4
	float camera4 = *camera4_Adress;


	float* camerapositionx = (float*)(sixStep + 0x90);//camera position1
	float x_camera = *camerapositionx;

	float* camerapositiony = (float*)(sixStep + 0x94);//camera position2
	float y_camera = *camerapositiony;

	float* camerapositionz = (float*)(sixStep + 0x98);//camera position3
	float z_camera = *camerapositionz;


	float* x_coord_Address = (float*)(forthStep + 0x90);//player positionx
	float x_coord = *x_coord_Address;

	float* y_coord_Address = (float*)(forthStep + 0x94);//player positiony
	float y_coord = *y_coord_Address;

	float* z_coord_Address = (float*)(forthStep + 0x98);//player positionz
	float z_coord = *z_coord_Address;



	// This is the main loop that will run in the background while I play the game
	while (true) {
		

		// If the player presses 'P' then the player teleport to the specified location

		if (GetAsyncKeyState('P') & 1) {
			std::cout << "   P key pressed\n";
			*x_coord_Address = 24512;
			*y_coord_Address = 69682;
			*z_coord_Address = 4820;
		}
		
		//dash forward
		if (GetAsyncKeyState('F') & 1) {
			std::cout << "   F key pressed: dash forword\n";


			float x = 1 - 2 * (camera2 * camera2 + camera3 * camera3) * 800;
			float y = 2 * (camera1 * camera2 + camera3 * camera4) * 800;
			float z = 2 * (camera1 * camera3 - camera4 * camera2) * 800;

			//			*camerapositionx += x ;
			//			*camerapositiony += y ;
			//			*camerapositionz += z ;
			*x_coord_Address += x;
			*y_coord_Address += y;
			//			*z_coord_Address += z;


		}
		// dodge backwards
		if (GetAsyncKeyState('C') & 1) {
			std::cout << "   C key pressed: dodge backwards\n";
			float x = 1 - 2 * (camera2 * camera2 + camera3 * camera3) * 800;
			float y = 2 * (camera1 * camera2 + camera3 * camera4) * 800;
			float z = 2 * (camera1 * camera3 - camera4 * camera2) * 800;

			//			*camerapositionx += -(x );
			//			*camerapositiony += -(y );
			//			*camerapositionz += -(z );
			*x_coord_Address += -x;
			*y_coord_Address += -y;
			//			*z_coord_Address += -z;
		}

		// dash left
		if (GetAsyncKeyState('X') & 1) {
			std::cout << "   X key pressed: dash left\n";
			float x = 1 - 2 * (camera2 * camera2 + camera3 * camera3) * 800;
			float y = 2 * (camera1 * camera2 + camera3 * camera4) * 800;
			float z = 2 * (camera1 * camera3 - camera4 * camera2) * 800;

			//			*camerapositionx += -(x );
			//			*camerapositiony += -(y );
			//			*camerapositionz += -(z );
			*x_coord_Address += x;
			*y_coord_Address += -y;
			//			*z_coord_Address += -z;
		}
		//dash right
		if (GetAsyncKeyState('B') & 1) {
			std::cout << "   B key pressed: dash right";
			float x = 1 - 2 * (camera2 * camera2 + camera3 * camera3) * 800;
			float y = 2 * (camera1 * camera2 + camera3 * camera4) * 800;
			float z = 2 * (camera1 * camera3 - camera4 * camera2) * 800;

			//			*camerapositionx += -(x );
			//			*camerapositiony += -(y );
			//			*camerapositionz += -(z );
			*x_coord_Address += -x;
			*y_coord_Address += y;
			//			*z_coord_Address += -z;
		}
	}
	return 0;
}


// This is the main method that runs when the DLL is injected.
BOOL APIENTRY DllMain(HMODULE hModule,
	DWORD  ul_reason_for_call,
	LPVOID lpReserved
)
{
	switch (ul_reason_for_call)
	{
	case DLL_PROCESS_ATTACH:
	{
		// We run the cheat code in a seperate thread to stop it interupting the game execution. 
		// Again we dont catch a possible NULL, if we are going down then we can go down in flames. 
		CloseHandle(CreateThread(nullptr, 0, (LPTHREAD_START_ROUTINE)MyThread, hModule, 0, nullptr));
	}
	case DLL_THREAD_ATTACH:
	case DLL_THREAD_DETACH:
	case DLL_PROCESS_DETACH:
		break;
	}
	return TRUE;
}