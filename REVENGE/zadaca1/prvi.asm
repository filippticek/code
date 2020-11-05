.386
.model flat, stdcall
option casemap :none

.data
	prvi dd 10, 2, 8, 4, 6, 5, 7, 3, 9, 1		
 	zamj dw 0h
.code
_start:
			lea ecx, dword ptr [prvi]  			; pocetak polja
	poc:	xor edx, edx
			inc edx
			mov dword ptr [zamj], 0h

	petlja:	mov eax, dword ptr [ecx + edx*4h]
			mov ebx, dword ptr [ecx + edx*4h - 4h]

			cmp eax, ebx
			jg dalje

			push ebx
			mov ebx, eax
			pop eax

			mov dword ptr [ecx + edx*4h], eax
			mov dword ptr [ecx + edx*4h - 4h], ebx

			mov dword ptr [zamj], 1h

	dalje:	inc edx
			cmp edx, 0Ah
			jnz petlja

			cmp dword ptr [zamj], 1h
			jz poc

	kraj:
			ret
end _start