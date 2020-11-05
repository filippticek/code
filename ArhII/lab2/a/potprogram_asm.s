.intel_syntax noprefix

.global potprogram_asm


potprogram_asm:
		                     /* cdecl prolog: */
		push  ebp            /* spremi ebp */
		mov   ebp, esp       /* ubaci esp u ebp */

                		     /* zauzmi 4 bajta za lokalne varijable: */
		sub   esp,4         /* lokalne varijable su "ispod" ebp */
  		mov   eax,[ebp+12]  /* b */
		add   eax,[ebp+8]   /* a */
  		imul  eax,[ebp+16]  /* c */  

		add   esp,4

                		     /* cdecl epilog: */
		pop ebp            /* umjesto 'add esp,4, pop ebp' može biti 'leave'*/
		ret                /* povratak iz potprograma */  
