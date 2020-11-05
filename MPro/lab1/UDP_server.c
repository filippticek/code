#include <netdb.h>
#include <sys/socket.h>
#include <netdb.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#define MAXLEN 512
#define S_PORT_DEF "1234"
#define PAYLOAD "PAYLOAD:"

int main (int argc, char *argv[]) {
	int sockDesc, c;
	struct sockaddr from;
	struct addrinfo hints, *res;
	
	char buf[MAXLEN];
	char *S_PORT = NULL;
	char payload[MAXLEN] = PAYLOAD;
	socklen_t fromaddrlen;
	int msglen;
	
	while ((c = getopt(argc, argv, "l:p:")) != -1) {
		switch (c) {
		case 'l':
			S_PORT = optarg;
			break;
		case 'p':
			strcat(payload, optarg);
			if (strlen(payload) > MAXLEN) {
				fprintf(stderr, "Size of payload too large");
				return 2;
			}
			break;
		default:
			fprintf(stderr, "Usage: ./UDP_server [-l port] [-p payload]\n");
			return 1;
		}
	}

	if (S_PORT == NULL) {
		S_PORT = malloc(sizeof(char) * MAXLEN);
		S_PORT = S_PORT_DEF;
	}
	//if (payload == NULL) {
	//	payload = malloc(sizeof(char) * MAXLEN);
	//	memset(payload, '\0', sizeof(char) * MAXLEN);
	//}
	memset(&hints, 0, sizeof hints);
	
	hints.ai_family = AF_INET; 
	hints.ai_socktype = SOCK_DGRAM;
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
		
	while (1){
		fromaddrlen = sizeof(from);
		msglen = recvfrom(sockDesc, buf, MAXLEN, 0, &from, &fromaddrlen);
		printf("%s\n", buf);	
		if (strcmp(buf, "HELLO\n")) {
			fprintf(stderr, "Garbage message");
		} else {	
			sendto(sockDesc, payload, strlen(payload), 0, &from, fromaddrlen);
		}
	}
}
