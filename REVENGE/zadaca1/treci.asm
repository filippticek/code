.386
.model flat, stdcall
option casemap :none

.data
	tekst db "Sifrirani tekst\n"

.code
_start:
			lea edx, byte ptr [tekst]
			xor ecx, ecx

	petlja:	
			xor ebx, ebx
			xor eax, eax
			mov bl, [edx + ecx]
			cmp bx, 65
			jl next
			cmp bx, 91
			jge mali

			mov al, bl
			add al, 13
			cmp ax, 91
			jge preljev
			jmp u_granici

	mali:	
			cmp bx, 97
			jl next
			cmp bx, 123
			jge next

			mov al, bl
			add al, 13
			cmp ax, 123
			jge preljev
			jmp u_granici

	preljev: 
			mov al, bl
			sub al, 13

	u_granici:
			mov [edx + ecx], al

	next:	inc ecx
			mov bx, [edx + ecx]
			cmp ebx, 6E5Ch 
			jne petlja

			ret
end _start