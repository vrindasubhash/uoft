void handle_client(int clientfd) {
  filename_size = ntohl(filename_size);
  message_size = ntohl(message_size);

  filename = malloc(sizeof(char) * (filename_size + 1));
  message = malloc(sizeof(char) * (message_size + 1));

  read(clientfd, filename, filename_size);
  read(clientfd, message, message_size);

  filename[filename_size] = '\0';
  message[message_size] = '\0';


  FILE * f = fopen(filename, "a");
  fprintf(f, "%s\n", message);
  fclose(f);
  
  free(filename);
  free(message);

}
