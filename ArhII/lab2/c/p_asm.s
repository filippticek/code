.intel_syntax noprefix

.global p_asm


p_asm:
                                     /* cdecl prolog: */
                push  ebp            /* spremi ebp */
                mov   ebp, esp       /* ubaci esp u ebp */
                
                mov eax, 0           /* registar za zbroj */
                mov ecx, 0           /* registar za brojač */
                mov edx, [esp+8]     /* registar za granicu */

                or edx, edx
                jz  kraj
          
        petlja: add eax, ecx
                add ecx, 1
                cmp edx, ecx 
                jnz petlja

        kraj:   pop ebp
                ret
