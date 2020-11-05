.intel_syntax noprefix

.global pot_x87

pot_x87:
            push  ebp 
            mov   ebp, esp 
            push ebx
            push edi
            
            mov eax, [ebp+8]    /* A */
            mov ebx, [ebp+12]   /* B */
            mov ecx, [ebp+16]   /* count */
            mov edi, [ebp+20]   /* R */
            mov edx, 0          /* index */    

            or ecx, ecx
            jz kraj

petlja:     fld DWORD PTR [eax+edx*4]
            fld DWORD PTR [ebx+edx*4]
            
            fadd
            fstp DWORD PTR [edi+edx*4]

            inc edx
            cmp ecx, edx
            jne petlja

kraj:       pop edi
            pop ebx
            pop ebp
            ret

