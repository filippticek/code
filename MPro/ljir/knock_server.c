#include <stdio.h>
#include <netdb.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <sys/time.h>
#include <sys/select.h>
#define MAXLEN 512

int main(int argc, char *argv[]) {
	int u1_sockDesc, u2_sockDesc, uk_sockDesc, tk_sockDesc, ta_sockDesc;
	struct sockaddr_in ;
	struct addrinfo hints, *res;
	struct sockaddr from;
	socklen_t fromaddrlen;
    int on = 1;
	int state = 1;
	char *lozinka;
	char *tajni_kljuc;	
	char *u1;
	char *u2;
	char *uk;
	char *ta;
	char *tk;
	char buf[MAXLEN];
	char challenge[5];
	char poruka[5];
	
	struct timeval tv = {10, 0};
	fd_set readfds, writefds;

	if (argc == 8) {
		lozinka = argv[1];
		tajni_kljuc = argv[2];
		u1 = argv[3];
		u2 = argv[4];
		uk = argv[5];
		ta = argv[6];
		tk = argv[7];
	} else if (argc == 10 && !strcmp(argv[1], "-t")) {
		tv.tv_sec = atoi(argv[2]);
		lozinka = argv[3];
		tajni_kljuc = argv[4];
		u1 = argv[5];
		u2 = argv[6];
		uk = argv[7];
		ta = argv[8];
		tk = argv[9];
	} else {
		fprintf(stderr, "Usage: knock_server [-t timeout] lozinka tajni_kljuc u1 u2 uk ta tk\n");
		return -1;
	}

	//kreiranje u1
	memset(&hints, 0, sizeof(hints));

	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_DGRAM;
	hints.ai_flags = AI_PASSIVE;
	getaddrinfo(NULL, u1, &hints, &res);

	u1_sockDesc = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
	if (u1_sockDesc == -1) {
		fprintf(stderr, ".knock_server: Couldn't create socket on u1\n");
		return -2;
	}

	if (bind (u1_sockDesc, res->ai_addr, res->ai_addrlen)) {
		fprintf(stderr, ".knock_server: Couldn't bind socket on u1\n");
		return -3;
	}
	//kreiranje u2
	getaddrinfo(NULL, u2, &hints, &res);

	u2_sockDesc = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
	if (u2_sockDesc == -1) {
		fprintf(stderr, ".knock_server: Couldn't create socket on u2\n");
		return -2;
	}

	if (setsockopt(u2_sockDesc, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(struct timeval))) {
		fprintf(stderr, ".knock_server: Couldn't set socket option on u2\n");
		return -4;
	}
	
	if (bind (u2_sockDesc, res->ai_addr, res->ai_addrlen)) {
		fprintf(stderr, ".knock_server: Couldn't bind socket on u2\n");
		return -3;
	}
	//kreiranje uk
	getaddrinfo(NULL, uk, &hints, &res);

	uk_sockDesc = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
	if (uk_sockDesc == -1) {
		fprintf(stderr, ".knock_server: Couldn't create socket on uk\n");
		return -2;
	}

	if (bind (uk_sockDesc, res->ai_addr, res->ai_addrlen)) {
		fprintf(stderr, ".knock_server: Couldn't bind socket on uk\n");
		return -3;
	}
	//kreiranje tk
	hints.ai_socktype = SOCK_STREAM;
	getaddrinfo(NULL, tk, &hints, &res);

	tk_sockDesc = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
	if (tk_sockDesc == -1) {
		fprintf(stderr, ".knock_server: Couldn't create socket on tk\n");
		return -2;
	}

	if (setsockopt(tk_sockDesc, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(int))) {
		fprintf(stderr, ".knock_server: Couldn't set socket option on tk\n");
		return -4;
	}
	
	if (bind (tk_sockDesc, res->ai_addr, res->ai_addrlen)) {
		fprintf(stderr, ".knock_server: Couldn't bind socket on tk\n");
		return -3;
	}
	
	if (listen(tk_sockDesc, 128)) {
		fprintf(stderr, ".knock_server: Couldn't listen on tk\n");
		return -5;
	}

	while(1) {
		FD_ZERO(&readfds);
		FD_ZERO(&writefds);
		FD_SET(u1_sockDesc, &readfds);
		FD_SET(u2_sockDesc, &readfds);
		FD_SET(uk_sockDesc, &readfds);
		FD_SET(tk_sockDesc, &readfds);
		int maxDesc = (u1_sockDesc > u2_sockDesc) ? u1_sockDesc : u2_sockDesc;
		maxDesc = (uk_sockDesc > maxDesc) ? uk_sockDesc : maxDesc;
		maxDesc = (tk_sockDesc > maxDesc) ? tk_sockDesc : maxDesc;

		if (select(maxDesc + 1, &readfds, &writefds, 0, 0) < 0) {
			fprintf(stderr, ".knock_server: select() error\n");
			return -6;
		}
		if (FD_ISSET(u1_sockDesc, &readfds) && state == 1) {
			int msglen;
            int rnd = 0;
			memset(buf, '\0', MAXLEN);
			if ((msglen = recvfrom(u1_sockDesc, buf, MAXLEN, 0, &from, &fromaddrlen)) > 0) {
				if (!strncmp(buf, lozinka, strlen(lozinka))) {
					state = 2;
                    for (int i=0; i<4;i++) {
                        rnd = random() % 2;
                        if (rnd) challenge[i] = 'A' + (random() % 26);
                        else challenge[i] = 'a' + (random() % 26);
                    }
                    challenge[4] = '\0';
                    memset(poruka, '\0', sizeof(poruka));
					for (int i=0; i<4;i++) poruka[i] = tajni_kljuc[i] ^ challenge[i];
					poruka[4] = '\0';
                    sendto(u1_sockDesc, challenge, strlen(challenge), 0, &from, fromaddrlen); 		
				}
			}
		} else if (FD_ISSET(u2_sockDesc, &readfds) && state == 2) {
			int msglen;
			memset(buf, '\0', MAXLEN);
			if ((msglen = recvfrom(u2_sockDesc, buf, MAXLEN, 0, &from, &fromaddrlen)) > 0) {
				if (!strncmp(buf, poruka, 4)) {
					int socknew;
					hints.ai_socktype = SOCK_STREAM;
					getaddrinfo(NULL, ta, &hints, &res);
					state = 3;
					ta_sockDesc = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
					if (ta_sockDesc == -1) {
						fprintf(stderr, ".knock_server: Couldn't create socket on ta\n");
						return -2;
					}
					if (setsockopt(ta_sockDesc, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(struct timeval))) {
		                fprintf(stderr, ".knock_server: Couldn't set socket option on u2\n");
		                return -4;
	                }
	


					if (setsockopt(ta_sockDesc, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(int))) {
						fprintf(stderr, ".knock_server: Couldn't set socket option on ta\n");
						return -4;
					}
					
					if (bind(ta_sockDesc, res->ai_addr, res->ai_addrlen)) {
						fprintf(stderr, ".knock_server: Couldn't bind socket on ta\n");
						return -3;
					}
					
					if (listen(ta_sockDesc, 128)) {
						fprintf(stderr, ".knock_server: Couldn't listen on ta\n");
						return -5;
					}
					if (setsockopt(u2_sockDesc, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(struct timeval))) {
		                fprintf(stderr, ".knock_server: Couldn't set socket option on u2\n");
		                return -4;
	                }
	

					socknew = accept(ta_sockDesc, &from, &fromaddrlen);
					if (socknew) {
					    write(socknew, "Hello world!\n", strlen("Hello world!\n"));
					}
                    close(socknew);
                    close(ta_sockDesc);
				}
			} 
            state = 1;
		} else if (FD_ISSET(uk_sockDesc, &readfds)) {
			memset(buf, '\0', MAXLEN);
			if (recvfrom(uk_sockDesc, buf, MAXLEN,0, &from, &fromaddrlen) >= 0) state = 1;
		} else if (FD_ISSET(tk_sockDesc, &readfds)) {
			int socknew;
			memset(buf, '\0', MAXLEN);
			socknew = accept (tk_sockDesc, &from, &fromaddrlen);
			if (socknew < 0) {
				fprintf(stderr, ".knock_server: acceot() error\n");
				return -7;
			} 
			if (read(socknew, buf, MAXLEN) >= 0) state = 1;
		}

		 
	}
}


