.intel_syntax noprefix

.global potprogram_asm


potprogram_asm:        
                push ebp
                mov ebp, esp

                mov eax, 42
                mov ebx, 0x42
                mov edx, 0x0fff
                shl edx, 0x10
                add edx, 0xdd 

                pop ebp
                ret

