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

#define MAXLEN 512
#define DEFAULT_PORT "1234"

int main(int argc, char *argv[]) {
	int sockDesc, conSock;
	char buf[MAXLEN];
	char msg[MAXLEN];
	int msg_len_t, msg_len;
	char *tcp_port = NULL;
	struct sockaddr_in tcp;
	struct addrinfo hints, *res;
	struct sockaddr from;
	socklen_t fromaddrlen;
	char ip_con_tcp[INET_ADDRSTRLEN];
	int ip_con_port;
	struct sockaddr_in addr_target[60];
	struct sockaddr_in target;

	if (argc > 3) {
		fprintf(stderr, "Usage: tcp2udp [-p tcp_port]/n");
		return -1;
	} else if (argc == 3) {
		tcp_port = argv[2];
	} else {
		tcp_port = malloc(sizeof(char) * MAXLEN);
		tcp_port = DEFAULT_PORT;	
	}
	
	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_flags = AI_PASSIVE;
	getaddrinfo(NULL, tcp_port, &hints, &res);

	if ((sockDesc = socket(res->ai_family, res->ai_socktype, res->ai_protocol)) == -1) {
		fprintf(stderr, "Couldn't create a socket\n");
		return -2;
	}

	if (bind(sockDesc, res->ai_addr, res->ai_addrlen)) {
		fprintf(stderr, "Couldn't bind address to socket\n");
		return -3;
	}

	if (listen(sockDesc, 128)) {
		fprintf(stderr, "Couldn't listen on socket\n");
		return -4;
	}

	while (1) {
		if ((conSock = accept(sockDesc, &from, &fromaddrlen)) == -1) {
			fprintf(stderr, "Error on accepting connection\n");
			return -5;
		} else {
			inet_ntop(AF_INET, &((struct sockaddr_in *) &from)->sin_addr, 
					ip_con_tcp,INET_ADDRSTRLEN);
			ip_con_port = ntohs(&((struct sockaddr_in *) &from)->sin_port);
			printf("ON:%s:%d\n",ip_con_tcp, ip_con_port);
		}
		while(1) {
			memset(buf, '\0', sizeof(buf));
			memset(msg, '\0', sizeof(msg));
		    	msg_len_t = 0;
			msg_len = 0;
			do { 
				msg_len = read(conSock, buf, MAXLEN); 
				msg_len_t += msg_len; 
		    		if (msg_len_t > MAXLEN) {
					    break;
			    	} else {
		     			strncpy(&msg[msg_len_t], buf, msg_len);
		    		}
		    		if (buf[msg_len] == '\n') {
		    			break;
		    		}
			} while (msg_len > 0);
			
			if (msg[0] == "Q") {
				close(conSock);
				printf("OFF:%s:%d\n",ip_con_tcp, ip_con_port);
				break;
			} else {
				if (msg[1] == "T") {
					if (write(conSock, "OK\n", sizeof("OK\n")) > 0) {
						fprintf(stderr, "Couldn't send data");
						return -6;
					}
				} else if (msg[1] == "E") {
					int target_count = 0;
					int msg_count = 5;
					char target_ip[INET_ADDRSTRLEN];
					char target_port[22];
					while (msg[msg_count] != '\n') {
						int i = msg_count;
						int j;
						while (msg[i] != ':') i++;
						j = i+1;
						while (msg[j] != ';' || msg[j] != '#') j++;
						strncpy(target_ip, &msg[msg_count], i - msg_count);
						msg_count += (i + 1);
						strncpy(target_port, &msg[i], j - msg_count);
						inet_pton(AF_INET, target_ip, (struct sockaddr *)&(target.sin_addr));
						target.sin_family = AF_INET;
						target.sin_port = htons(atoi(target_port));
						memset(target.sin_zero, '\0', sizeof(target.sin_zero));
						addr_target[target_count] = target;
					}


				}
			}
		}
			
			
	}



}
