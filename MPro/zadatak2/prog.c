#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string.h>
  
int main(int argc, char* argv[]){
     char *host = argv[argc - 2];
     char *service = argv[argc - 1];
     int flags[5] = {0,0,0,0,0};
     int c, brArg = 0, error;
     struct addrinfo hints, *res;
     char addrstr[100];

     if (argc < 3){
         fprintf(stderr, "Krivi broj argumenata\n");
         return 1;
     }
     
     while ((c = getopt (argc, argv, "rtuxhn46")) != -1){
         switch (c){
             case 'r':
                 flags[0] = 1;
                 break;
             case 't':
                 flags[1] = 0;
                 break;
             case 'u':
                 flags[1] = 1;
                 break;
             case 'x':
                 flags[2] = 1;
                 break;
             case 'h':
                 flags[3] = 0;
                 break;
             case 'n':
                 flags[3] = 1;
                 break;
             case '4':
                 flags[4] = 0;
                 break;
             case '6':
                 flags[4] = 1;
                 break;
             default:
                 fprintf(stderr, "prog [-r] [-t|-u] [-x] [-h|-n] [-46] {hostname | IP_address} {servic    ename | port}\n");
                 return 1;
         }
         brArg++;
     }
 
     if ((argc - brArg) > 3){
                 fprintf(stderr, "prog [-r] [-t|-u] [-x] [-h|-n] [-46] {hostname | IP_address{servicename | port}\n");
         return 1;
     }
 
     if (!flags[0]){
         int port;
         memset(&hints, 0, sizeof(hints));
         hints.ai_flags |= AI_CANONNAME;
 
         if (!flags[4]){                     //ipv4 ili ipv6
             hints.ai_family = AF_INET;
         } else {
             hints.ai_family = AF_INET6;
         }
 
         if(!flags[1]){                      //tcp ili udp
             hints.ai_socktype = SOCK_STREAM;
         } else {
             hints.ai_socktype = SOCK_DGRAM;
         }
 
         error = getaddrinfo(host, service, &hints, &res);
 
         if (error){
             fprintf(stderr, "Pogreška. Provijeri argumente i pokušaj ponovno\n");
             return 1;
         }
 
 
         if(!flags[4]){
 
             inet_ntop(res->ai_family, &((struct sockaddr_in *) res->ai_addr)->sin_addr, addrstr, 100)    ;
             if (flags[3]){
                 port = ((struct sockaddr_in *)res->ai_addr)->sin_port;
             } else {
                 port =  ntohs(((struct sockaddr_in *)res->ai_addr)->sin_port);
             }
         } else {
             inet_ntop(res->ai_family, &((struct sockaddr_in6 *) res->ai_addr)->sin6_addr, addrstr,100);
             if (flags[3]) {
                 port = ((struct sockaddr_in6 *)res->ai_addr)->sin6_port;
             } else {
                 port = ntohs(((struct sockaddr_in6 *)res->ai_addr)->sin6_port);
             }
         }
         if (flags[2]){
             printf("%s (%s) %04x\n", addrstr, res->ai_canonname, port);
         } else {
             printf("%s (%s) %d\n", addrstr, res->ai_canonname, port);
         }
         freeaddrinfo(res);
                                                                                       
        return 0;
 
     } else {
		if(flags[4]){
			char hos[NI_MAXHOST];
			char port[30];
   	 		struct sockaddr_in6 sa;
			
			sa.sin6_family = AF_INET6;
			sa.sin6_port = htons(atoi(service)); 
			int flag = 0;
			if (flags[1]) flag = NI_DGRAM;
			
			if (inet_pton(AF_INET6, host, &(sa.sin6_addr)) != 1) {
				fprintf(stderr,"%s nije valjana IPv6 adresa\n", host);
				return 1;
			}
			
			if (getnameinfo((struct sockaddr *)&sa,sizeof(struct sockaddr_in6), hos, sizeof(hos), port, sizeof(port), flag)) {
				fprintf(stderr, "Pogreska. Provijeri argumente i pokusaj ponovno\n");
				return 1;
			}
			printf("%s (%s) %s\n", host, hos, port);
			return 0;

		} else {
				char hos[NI_MAXHOST];
				char port[30];
   	 			struct sockaddr_in sa;
				
				sa.sin_family = AF_INET;
				sa.sin_port = htons(atoi(service)); 
				int flag = 0;
				if (flags[1]) flag = NI_DGRAM;
			
				if (inet_pton(AF_INET, host, &(sa.sin_addr)) != 1) {
					fprintf(stderr,"%s nije valjana IPv6 adresa\n", host);
					return 1;
				}
			
				if (getnameinfo((struct sockaddr *)&sa,sizeof(struct sockaddr_in), hos, sizeof(hos), port, sizeof(port), flag)) {
					fprintf(stderr, "Pogreska. Provijeri argumente i pokusaj ponovno\n");
					return 1;
				}
				printf("%s (%s) %s\n", host, hos, port);
				return 0;
		}
	}
}

