void server_loop(int listenfd) {
  fd_set readfd, masterfds;
  
  FD_ZERO(&masterfds);
  FD_SET(listenfd, &masterfds);
 
  int max_fd = listenfd;
  
  while (1) {
    readfds = masterfds;

    select(max_fd + 1, &readfds, NULL, NULL, NULL);
   
    for (int i = 0; i <= max_fd; i++) {
      if (FD_ISSET(i, &readfds)) {
        if (i == listenfd) {
          int clientfd = accept(listenfd, NULL, NULL);
          FD_SET(clientfd, &masterfds);
          if (clientfd > max_fd)
            max_fd = clientfd;
        }
        else {
          handle_client(1);
          close(i);
          FD_CLR(i, &masterfds);
        }
      }
    }
  }
}
