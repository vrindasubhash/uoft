/*****************************************************************************/
/*                       CSC209-24s A4 Audio Stream                          */
/*       Copyright 2024 -- Demetres Kostas PhD (aka Darlene Heliokinde)      */
/*****************************************************************************/
#include "as_server.h"


int init_server_addr(int port, struct sockaddr_in *addr){
    // Allow sockets across machines.
    addr->sin_family = AF_INET;
    // The port the process will listen on.
    addr->sin_port = htons(port);
    // Clear this field; sin_zero is used for padding for the struct.
    memset(&(addr->sin_zero), 0, 8);

    // Listen on all network interfaces.
    addr->sin_addr.s_addr = INADDR_ANY;

    return 0;
}

int set_up_server_socket(const struct sockaddr_in *server_options, int num_queue) {
    int soc = socket(AF_INET, SOCK_STREAM, 0);
    if (soc < 0) {
        perror("socket");
        exit(1);
    }

    printf("Listen socket created\n");

    // Make sure we can reuse the port immediately after the
    // server terminates. Avoids the "address in use" error
    int on = 1;
    int status = setsockopt(soc, SOL_SOCKET, SO_REUSEADDR,
                            (const char *) &on, sizeof(on));
    if (status < 0) {
        perror("setsockopt");
        exit(1);
    }

    // Associate the process with the address and a port
    if (bind(soc, (struct sockaddr *)server_options, sizeof(*server_options)) < 0) {
        // bind failed; could be because port is in use.
        perror("bind");
        exit(1);
    }

    printf("Socket bound to port %d\n", ntohs(server_options->sin_port));

    // Set up a queue in the kernel to hold pending connections.
    if (listen(soc, num_queue) < 0) {
        // listen failed
        perror("listen");
        exit(1);
    }

    printf("Socket listening for connections\n");

    return soc;
}


ClientSocket accept_connection(int listenfd) {
    ClientSocket client;
    socklen_t addr_size = sizeof(client.addr);
    client.socket = accept(listenfd, (struct sockaddr *)&client.addr,
                               &addr_size);
    if (client.socket < 0) {
        perror("accept_connection: accept");
        exit(-1);
    }

    // print out a message that we got the connection
    printf("Server got a connection from %s, port %d\n",
           inet_ntoa(client.addr.sin_addr), ntohs(client.addr.sin_port));

    return client;
}


int list_request_response(const ClientSocket * client, const Library *library) {
    // TODO Complete this function
    printf("started list_request_response"); //@vrinda
    size_t buffer_size = 0;
    for (uint32_t i = 0; i < library->num_files; i++) {
        buffer_size += strlen(library->files[i]) + 10; // Extra space for the index, colon, "\r\n
    }
    buffer_size += 2; // last "\r\n"

    char *response = (char *)malloc(buffer_size);
    if (!response) {
        perror("Memory allocation failed");
        return -1;
    }
    response[0] = '\0'; // start with empty string
    size_t offset = 0;
    for (int i = library->num_files - 1; i >= 0; i--) {
        // Append each file info to the response string starting from the back to reverse
        int added = snprintf(response + offset, buffer_size - offset, "%d:%s\r\n", i, library->files[i]);
        printf("%d, %s", i, library->files[i]);
        if (added < 0) {
            perror("Failed to append to response string");
            free(response);
            return -1;
        }
        offset += added;
    }
    // Write the response to the client.
    int fd = client->socket;
    if (write(fd, response, strlen(response)) < 0) {
        perror("Failed to send response to client");
        free(response);
        return -1;
    }

    // Free the response buffer.
    free(response);

    return 0;
}


static int _load_file_size_into_buffer(FILE *file, uint8_t *buffer) {
    if (fseek(file, 0, SEEK_END) < 0) {
        ERR_PRINT("Error seeking to end of file\n");
        return -1;
    }
    uint32_t file_size = ftell(file);
    if (fseek(file, 0, SEEK_SET) < 0) {
        ERR_PRINT("Error seeking to start of file\n");
        return -1;
    }
    buffer[0] = (file_size >> 24) & 0xFF;
    buffer[1] = (file_size >> 16) & 0xFF;
    buffer[2] = (file_size >> 8) & 0xFF;
    buffer[3] = file_size & 0xFF;
    return 0;
}


int stream_request_response(const ClientSocket * client, const Library *library,
                            uint8_t *post_req, int num_pr_bytes) {
    // TODO Complete this function
    /*
    (void)_load_file_size_into_buffer;
    return -1;
    */
    if (num_pr_bytes > 4) {
        ERR_PRINT("Received more bytes than expected for file index\n");
        return -1;
    }

    // Complete the reception of the file index if necessary
    uint32_t file_index_network_order;
    memcpy(&file_index_network_order, post_req, num_pr_bytes);
    if (num_pr_bytes < 4) {
        ssize_t extra_bytes_needed = 4 - num_pr_bytes;
        if (read_precisely(client->socket, ((uint8_t*)&file_index_network_order) + num_pr_bytes, extra_bytes_needed) != extra_bytes_needed) {
            ERR_PRINT("Failed to read the complete file index\n");
            return -1;
        }
    }

    // Convert network byte order to host byte order
    uint32_t file_index = ntohl(file_index_network_order);

    // Validate file index
    if (file_index >= library->num_files) {
        ERR_PRINT("File index %u out of range\n", file_index);
        return -1; // Client will hang, as specified
    }

    // Create file path
    char *file_path = _join_path(library->path, library->files[file_index]);
    if (!file_path) {
        ERR_PRINT("Memory allocation failed for file path\n");
        return -1;
    }

    FILE *file = fopen(file_path, "rb");
    free(file_path); // No longer needed
    if (!file) {
        ERR_PRINT("File %u not found\n", file_index);
        return -1; // File not found
    }

    // Get file size
    fseek(file, 0L, SEEK_END);
    uint32_t file_size = htonl(ftell(file)); // Convert to network byte order
    fseek(file, 0L, SEEK_SET);

    // Send file size to client
    if (write_precisely(client->socket, &file_size, sizeof(file_size)) != sizeof(file_size)) {
        ERR_PRINT("Failed to send file size\n");
        fclose(file);
        return -1;
    }

    // Stream the file
    char buffer[STREAM_CHUNK_SIZE];
    size_t bytes_read;
    while ((bytes_read = fread(buffer, 1, sizeof(buffer), file)) > 0) {
        if (write_precisely(client->socket, buffer, bytes_read) != bytes_read) {
            ERR_PRINT("Failed to send file data\n");
            fclose(file);
            return -1;
        }
    }

    fclose(file);
    return 0;
}


static Library make_library(const char *path){
    Library library;
    library.path = path;
    library.num_files = 0;
    library.files = NULL;
    library.name = "server";

    printf("Initializing library\n");
    printf("Library path: %s\n", library.path);

    return library;
}


static void _wait_for_children(pid_t **client_conn_pids, int *num_connected_clients, uint8_t immediate) {
    int status;
    for (int i = 0; i < *num_connected_clients; i++) {
        int options = immediate ? WNOHANG : 0;
        if (waitpid((*client_conn_pids)[i], &status, options) > 0) {
            if (WIFEXITED(status)) {
                printf("Client process %d terminated\n", (*client_conn_pids)[i]);
                if (WEXITSTATUS(status) != 0) {
                    fprintf(stderr, "Client process %d exited with status %d\n",
                            (*client_conn_pids)[i], WEXITSTATUS(status));
                }
            } else {
                fprintf(stderr, "Client process %d terminated abnormally\n",
                        (*client_conn_pids)[i]);
            }

            for (int j = i; j < *num_connected_clients - 1; j++) {
                (*client_conn_pids)[j] = (*client_conn_pids)[j + 1];
            }

            (*num_connected_clients)--;
            *client_conn_pids = (pid_t *)realloc(*client_conn_pids,
                                                 (*num_connected_clients)
                                                 * sizeof(pid_t));
        }
    }
}

/*
** Create a server socket and listen for connections
**
** port: the port number to listen on.
** 
** On success, returns the file descriptor of the socket.
** On failure, return -1.
*/
static int initialize_server_socket(int port) {
    struct sockaddr_in addr;
    init_server_addr(port, &addr);
    return set_up_server_socket(&addr, MAX_PENDING); 
}

int run_server(int port, const char *library_directory){
    Library library = make_library(library_directory);
    if (scan_library(&library) < 0) {
        ERR_PRINT("Error scanning library\n");
        return -1;
    }

    int num_connected_clients = 0;
    pid_t *client_conn_pids = NULL;

	int incoming_connections = initialize_server_socket(port);
	if (incoming_connections == -1) {
		return -1;	
	}
	
    int maxfd = incoming_connections;
    fd_set incoming;
    SET_SERVER_FD_SET(incoming, incoming_connections);
    int num_intervals_without_scan = 0;

    while(1) {
        if (num_intervals_without_scan >= LIBRARY_SCAN_INTERVAL) {
            if (scan_library(&library) < 0) {
                fprintf(stderr, "Error scanning library\n");
                return 1;
            }
            num_intervals_without_scan = 0;
        }

        struct timeval select_timeout = SELECT_TIMEOUT;
        if(select(maxfd + 1, &incoming, NULL, NULL, &select_timeout) < 0){
            perror("run_server");
            exit(1);
        }

        if (FD_ISSET(incoming_connections, &incoming)) {
            ClientSocket client_socket = accept_connection(incoming_connections);

            pid_t pid = fork();
            if(pid == -1){
                perror("run_server");
                exit(-1);
            }
            // child process
            if(pid == 0){
                close(incoming_connections);
                free(client_conn_pids);
                printf("debug 1: run_server\n");
                int result = handle_client(&client_socket, &library);
                _free_library(&library);
                close(client_socket.socket);
                return result;
            }
            close(client_socket.socket);
            num_connected_clients++;
            client_conn_pids = (pid_t *)realloc(client_conn_pids,
                                               (num_connected_clients)
                                               * sizeof(pid_t));
            client_conn_pids[num_connected_clients - 1] = pid;
        }
        if (FD_ISSET(STDIN_FILENO, &incoming)) {
            if (getchar() == 'q') break;
        }

        num_intervals_without_scan++;
        SET_SERVER_FD_SET(incoming, incoming_connections);

        // Immediate return wait for client processes
        _wait_for_children(&client_conn_pids, &num_connected_clients, 1);
    }

    printf("Quitting server\n");
    close(incoming_connections);
    _wait_for_children(&client_conn_pids, &num_connected_clients, 0);
    _free_library(&library);
    return 0;
}


static uint8_t _is_file_extension_supported(const char *filename){
    static const char *supported_file_exts[] = SUPPORTED_FILE_EXTS;

    for (int i = 0; i < sizeof(supported_file_exts)/sizeof(char *); i++) {
        char *files_ext = strrchr(filename, '.');
        if (files_ext != NULL && strcmp(files_ext, supported_file_exts[i]) == 0) {
            return 1;
        }
    }

    return 0;
}


static int _depth_scan_library(Library *library, char *current_path){

    char *path_in_lib = _join_path(library->path, current_path);
    if (path_in_lib == NULL) {
        return -1;
    }

    DIR *dir = opendir(path_in_lib);
    if (dir == NULL) {
        perror("scan_library");
        return -1;
    }
    free(path_in_lib);

    struct dirent *entry;
    while((entry = readdir(dir)) != NULL) {
        if ((entry->d_type == DT_REG) &&
            _is_file_extension_supported(entry->d_name)) {
            library->files = (char **)realloc(library->files,
                                              (library->num_files + 1)
                                              * sizeof(char *));
            if (library->files == NULL) {
                perror("_depth_scan_library");
                return -1;
            }

            library->files[library->num_files] = _join_path(current_path, entry->d_name);
            if (library->files[library->num_files] == NULL) {
                perror("scan_library");
                return -1;
            }
            #ifdef DEBUG
            printf("Found file: %s\n", library->files[library->num_files]);
            #endif
            library->num_files++;

        } else if (entry->d_type == DT_DIR) {
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
                continue;
            }

            char *new_path = _join_path(current_path, entry->d_name);
            if (new_path == NULL) {
                return -1;
            }

            #ifdef DEBUG
            printf("Library scan descending into directory: %s\n", new_path);
            #endif

            int ret_code = _depth_scan_library(library, new_path);
            free(new_path);
            if (ret_code < 0) {
                return -1;
            }
        }
    }

    closedir(dir);
    return 0;
}


// This function is implemented recursively and uses realloc to grow the files array
// as it finds more files in the library. It ignores MAX_FILES.
int scan_library(Library *library) {
    // Maximal flexibility, free the old strings and start again
    // A hash table leveraging inode number would be a better way to do this
    #ifdef DEBUG
    printf("^^^^ ----------------------------------- ^^^^\n");
    printf("Freeing library\n");
    #endif
    _free_library(library);

    #ifdef DEBUG
    printf("Scanning library\n");
    #endif
    int result = _depth_scan_library(library, "");
    #ifdef DEBUG
    printf("vvvv ----------------------------------- vvvv\n");
    #endif
    return result;
}


int handle_client(const ClientSocket * client, Library *library) {
    printf("trying to debug2: handle_client\n"); //@vrinda
    char *request = NULL;
    uint8_t *request_buffer = (uint8_t *)malloc(REQUEST_BUFFER_SIZE);
    printf("trying to debug3: handle_client\n"); //@vrinda
    if (request_buffer == NULL) {
        perror("handle_client");
        return 1;
    }
    uint8_t *buff_end = request_buffer;

    int bytes_read = 0;
    int bytes_in_buf = 0;
    while((bytes_read = read(client->socket, buff_end, REQUEST_BUFFER_SIZE - bytes_in_buf)) > 0){
        #ifdef DEBUG
        printf("Read %d bytes from client\n", bytes_read);
        #endif

        bytes_in_buf += bytes_read;

        request = find_network_newline((char *)request_buffer, &bytes_in_buf);

        if (request && strcmp(request, REQUEST_LIST) == 0) {
        printf("trying to debug4: in handle_client before list_request_response\n"); //@vrinda
            if (list_request_response(client, library) < 0) {
                ERR_PRINT("Error handling LIST request\n");
                goto client_error;
            }
        printf("trying to debug5: in handle_client after list_request_response\n"); //@vrinda

        } else if (request && strcmp(request, REQUEST_STREAM) == 0) {
            int num_pr_bytes = MIN(sizeof(uint32_t), (unsigned long)bytes_in_buf);
            if (stream_request_response(client, library, request_buffer, num_pr_bytes) < 0) {
                ERR_PRINT("Error handling STREAM request\n");
                goto client_error;
            }
            bytes_in_buf -= num_pr_bytes;
            memmove(request_buffer, request_buffer + num_pr_bytes, bytes_in_buf);

        } else if (request) {
            ERR_PRINT("Unknown request: %s\n", request);
        }

        free(request); request = NULL;
        buff_end = request_buffer + bytes_in_buf;

    }
    if (bytes_read < 0) {
        perror("handle_client");
        goto client_error;
    }

    printf("Client on %s:%d disconnected\n",
           inet_ntoa(client->addr.sin_addr),
           ntohs(client->addr.sin_port));

    free(request_buffer);
    if (request != NULL) {
        free(request);
    }
    return 0;
client_error:
    free(request_buffer);
    if (request != NULL) {
        free(request);
    }
    return -1;
}


static void print_usage(){
    printf("Usage: as_server [-h] [-p port] [-l library_directory]\n");
    printf("  -h  Print this message\n");
    printf("  -p  Port to listen on (default: " XSTR(DEFAULT_PORT) ")\n");
    printf("  -l  Directory containing the library (default: ./library/)\n");
}


int main(int argc, char * const *argv){
    int opt;
    int port = DEFAULT_PORT;
    const char *library_directory = "library";

    // Check out man 3 getopt for how to use this function
    // The short version: it parses command line options
    // Note that optarg is a global variable declared in getopt.h
    while ((opt = getopt(argc, argv, "hp:l:")) != -1) {
        switch (opt) {
            case 'h':
                print_usage();
                return 0;
            case 'p':
                port = atoi(optarg);
                break;
            case 'l':
                library_directory = optarg;
                break;
            default:
                print_usage();
                return 1;
        }
    }

    printf("Starting server on port %d, serving library in %s\n",
           port, library_directory);

    return run_server(port, library_directory);
}
