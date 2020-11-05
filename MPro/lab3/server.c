#include <netdb.h>
#include <sys/socket.h>
#include <netdb.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/select.h>
#define STDIN 0
#define MAXLEN 1024 
#define S_PORT_DEF "1234"
#define PAYLOAD "PAYLOAD:"

int main (int argc, char *argv[]) {
	int sockDesc, c, conSock;
	struct sockaddr from;
	struct addrinfo hints, *res;

	int is_tcp = 0;	
	char buf[MAXLEN];
	char *S_PORT = NULL;
	char payload[MAXLEN];
	socklen_t fromaddrlen;
	int msglen;
	char cli_cmd[MAXLEN + 10];
	
	fd_set readfds;
	fd_set writefds;

	while ((c = getopt(argc, argv, "t:u:p:")) != -1) {
		switch (c) {
		case 'u':
			S_PORT = optarg;
			break;
		case 't':
			S_PORT = optarg;
			is_tcp = 1;
			break;
		case 'p':
			strcpy(payload, optarg);
			if (strlen(payload) > MAXLEN) {
				fprintf(stderr, "Size of payload too large");
				return 2;
			}
			break;
		default:
			fprintf(stderr, "Usage: ./server [-t tcp_port] [-u udp_port] [-p popis]\n");
			return 1;
		}
	}
	if (S_PORT == NULL) {
		S_PORT = malloc(sizeof(char) * MAXLEN);
		S_PORT = S_PORT_DEF;
	}
	memset(&hints, 0, sizeof hints);

	hints.ai_family = AF_INET;
	hints.ai_socktype = (is_tcp ? SOCK_STREAM : SOCK_DGRAM);
	hints.ai_flags = AI_PASSIVE;	
	getaddrinfo(NULL, S_PORT, &hints, &res);

	sockDesc = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
	
	if (sockDesc == -1){
		fprintf(stderr, "Couldn't create a socket\n");
		return 3;
	}

	if (bind(sockDesc, res->ai_addr, res->ai_addrlen)){
		fprintf(stderr, "Couldn't bind address to socket\n");
		return 4;
	
	}
	if (is_tcp) {
		if (listen(sockDesc, 128)) {
			fprintf(stderr, "Couldn't listen on socket\n");
			return -4;
		}
	}
	
	
	while (1) {
		FD_ZERO(&readfds);
		FD_ZERO(&writefds);
		FD_SET(STDIN, &readfds);
		FD_SET(sockDesc, &readfds);

		if (select(sockDesc+1, &readfds, &writefds, 0,0) < 0) {
			fprintf(stderr, "Select error\n");
			return -6;
		}
		
		if (FD_ISSET(STDIN,&readfds)){
			memset(cli_cmd, '\0', sizeof(cli_cmd));
			read(STDIN, cli_cmd, MAXLEN);
			switch (cli_cmd[0]) {
			case 'P':
				printf("%s\n", payload);
				break;
			case 'S':
				memset(payload, '\0', sizeof(payload));
				strcpy(payload, &cli_cmd[4]);
				break;
			case 'Q':
				printf("Terminating\n");
				return 0;
				break;
			default:
				fprintf(stderr, "Command unknown\n");
			}
		}
		fromaddrlen = sizeof(from);
		if (FD_ISSET(sockDesc, &readfds)) {
			memset(buf, '\0', MAXLEN);
			if (is_tcp) {
				if ((conSock = accept(sockDesc, &from, &fromaddrlen)) == -1) {
					fprintf(stderr, "Error on accepting connection\n");
					return -5;
				} 
				if (read(conSock, buf, MAXLEN) < 0) {
					continue;
				} else {
					if (write(conSock, payload, MAXLEN) < 0) {
						fprintf(stderr, "Couldn't write to socket\n");
						return -7;
					}
				}
				close(conSock);
					
			} else {
				if ((msglen = recvfrom(sockDesc, buf, MAXLEN, 0, &from, &fromaddrlen)) > 0) {
					printf("%s\n", buf);	
					if (strcmp(buf, "HELLO\n")) {
						fprintf(stderr, "Garbage message");
					} else {	
						sendto(sockDesc, payload, strlen(payload), 0, &from, fromaddrlen);
					}
				}
			}
		}
	}
}
