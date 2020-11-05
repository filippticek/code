.386
.model flat, stdcall
option casemap :none

.data
	prvi dd 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29

.code

binary_search:							; indexPocetak, indexKraj, brojKojiTrazimo
			push ebp
			mov ebp, esp
		
			mov ebx, dword ptr [ebp + 10h]
			mov ecx, dword ptr [ebp + 0ch]
			mov edx, dword ptr [ebp + 8h]

			cmp ecx, ebx
			jb nema

			xor eax, eax
			add eax, ebx
			add eax, ecx
			shr eax, 1

			cmp dword ptr[prvi + eax*4h], edx
			jz kraj
			jl test_desno
			jg test_lijevo

		test_desno:
			inc eax
			push eax
			push ecx
			push edx
			call binary_search
			jmp kraj

		test_lijevo:
			dec eax
			push ebx
			push eax
			push edx 
			call binary_search
			jmp kraj

	nema:	mov eax, -1

	kraj:	pop ebp
			retn 0Ch

_start:
		push 0
		push 29
		push 5

		call binary_search
		
		ret
end _start