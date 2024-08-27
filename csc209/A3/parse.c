/*****************************************************************************/
/*                           CSC209-24s A3 CSCSHELL                          */
/*       Copyright 2024 -- Demetres Kostas PhD (aka Darlene Heliokinde)      */
/*****************************************************************************/

#include <stdbool.h>

#include "cscshell.h"

#define CONTINUE_SEARCH NULL


// COMPLETE
char *resolve_executable(const char *command_name, Variable *path){

    if (command_name == NULL || path == NULL){
        return NULL;
    }

    if (strcmp(command_name, CD) == 0){
        return strdup(CD);
    }

    if (strcmp(path->name, PATH_VAR_NAME) != 0){
        ERR_PRINT(ERR_NOT_PATH);
        return NULL;
    }

    char *exec_path = NULL;

    if (strchr(command_name, '/')){
        exec_path = strdup(command_name);
        if (exec_path == NULL){
            perror("resolve_executable");
            return NULL;
        }
        return exec_path;
    }

    // we create a duplicate so that we can mess it up with strtok
    char *path_to_toke = strdup(path->value);
    if (path_to_toke == NULL){
        perror("resolve_executable");
        return NULL;
    }
    char *current_path = strtok(path_to_toke, ":");

    do {
        DIR *dir = opendir(current_path);
        if (dir == NULL){
            ERR_PRINT(ERR_BAD_PATH, current_path);
            closedir(dir);
            continue;
        }

        struct dirent *possible_file;

        while (exec_path == NULL) {
            // rare case where we should do this -- see: man readdir
            errno = 0;
            possible_file = readdir(dir);
            if (possible_file == NULL) {
                if (errno > 0){
                    perror("resolve_executable");
                    closedir(dir);
                    goto res_ex_cleanup;
                }
                // end of files, break
                break;
            }

            if (strcmp(possible_file->d_name, command_name) == 0){
                // +1 null term, +1 possible missing '/'
                size_t buflen = strlen(current_path) +
                    strlen(command_name) + 1 + 1;
                exec_path = (char *) malloc(buflen);
                // also sets remaining buf to 0
                strncpy(exec_path, current_path, buflen);
                if (current_path[strlen(current_path)-1] != '/'){
                    strncat(exec_path, "/", 2);
                }
                strncat(exec_path, command_name, strlen(command_name)+1);
            }
        }
        closedir(dir);

        // if this isn't null, stop checking paths
        if (possible_file) break;

    } while ((current_path = strtok(CONTINUE_SEARCH, ":")));

res_ex_cleanup:
    free(path_to_toke);
    return exec_path;
}


// Checks if a name is a valid shell variable name
bool is_valid_name(const char * name){
    while (*name != '\0') {
        if (!isalpha(*name) && (*name != '_')) 
            return false;
        name++;
    }
    return true;
}

// Creates a Variable.
Variable *create_var(const char * name, const char * value){
    Variable * var = safe_malloc(sizeof(Variable));
    var->name = strdup(name); 
    var->value = strdup(value);
    var->next = NULL; 
    return var;
}

// Get the variables.
Command *parse_variables(char *name, char *value, Variable **variables){
    if (strlen(name) == 0) {
        ERR_PRINT(ERR_VAR_START);
        return NULL;
    }
    if (!is_valid_name(name)) {
       ERR_PRINT(ERR_VAR_NAME, name); 
       return NULL;
    }

    if (*variables == NULL) { 
        *variables = create_var(name, value);
        return NULL;
    }
    
    // if it is PATH, put at the start
    if (strcmp(name, PATH_VAR_NAME) == 0) {
        Variable *tmp = create_var(name, value);
        tmp->next = *variables;
        *variables = tmp;
    }

    // checking for existing variables 
    Variable * curr = *variables;
    Variable * last = NULL;
    while (curr != NULL) {
        if (strcmp(curr->name, name) == 0) {
            free(curr->value);
            curr->value = strdup(value);
            return NULL;
        }
        last = curr;
        curr = curr->next;
    }
    last->next = create_var(name, value);
        
    return NULL;
}

// Gets the path environment variable. 
Variable *get_path(Variable ** variables){
     if (variables == NULL)
         return NULL;
     Variable * p_var = *variables;
     while (p_var != NULL) {
         if (strcmp(p_var->name, PATH_VAR_NAME) == 0)
             return p_var;
         p_var = p_var->next;
     }
     return NULL;
}

char *replace_variables_mk_line(const char *line, Variable *variables);

// Substitutes line with variable values. 
char *expand(const char *line, Variable **variables){
    if (*variables == NULL)
        return strdup(line);
    
    return replace_variables_mk_line(line, *variables);
}


// Creates the command objects. 
Command *parse_commands(char *line, Variable **variables){
    char * expanded_line = expand(line, variables);
    char * ptr = strchr(expanded_line, ' ');
    Command * cmd = safe_malloc(sizeof(Command));
    memset(cmd, 0, sizeof(Command));
    if (ptr != NULL) {
        *ptr = '\0';
        ptr++;
    }
    // empty line
    if (strlen(expanded_line) == 0) {
        free(cmd);
        free(expanded_line);
        return NULL;
    }
    
    cmd->exec_path = resolve_executable(expanded_line, get_path(variables));
    int count = 1;
    cmd->args = safe_malloc(sizeof(char*) * count);
    cmd->args[0] = strdup(cmd->exec_path);
    while ((ptr != NULL) && (strlen(ptr) > 0)) {
       char * last = ptr;
       ptr = strchr(ptr + 1, ' ');
       if (ptr != NULL) {
           *ptr = '\0';
           ptr++;
       }
       count++;
       cmd->args = safe_realloc(cmd->args, sizeof(char*) * count);
       cmd->args[count - 1] = strdup(last);
    }
    count++;
    cmd->args = safe_realloc(cmd->args, sizeof(char*) * count);
    cmd->args[count - 1] = NULL; 

    free(expanded_line);
    return cmd; 
}

Command *parse_line(char *line, Variable **variables){ 
    // getting rid of comments
    char * ptr = strchr(line, '#');
    if (ptr != NULL)
        *ptr = '\0';
    // find variable assignments
    ptr = strchr(line, '=');
    if (ptr == NULL)
        return parse_commands(line, variables);
    int position = ptr - line;
    // checks for spaces before equal sign
    for (int i = 0; i < position; i++) {
        if (line[i] == ' ')
            return parse_commands(line, variables);
    }
    
    // splits string into 2 by replacing '=' with '\0'
    // variable name goes from line to ptr
    // value goes from ptr+1 to end of string
    *ptr = '\0';
    char * name = line;
    char * value = ptr + 1;
    return parse_variables(name, value, variables);
}


// Checks if the var matches the string.  
// Takes care of short strings for both line and var.
bool compare(const char *line, const char *var) {
    for (int i = 0; i < strlen(var); i++) {
        if (line[i] == '\0')
            return false;
        if (var[i] != line[i])
            return false;
    }
    return true;
}

// Returns the value of the key to replace if found, if not returns NULL.
// No memory allocation. 
Variable *find_replacement(const char *line, Variable *variables) {
    while (variables != NULL) {
        if (compare(line, variables->name))
            return variables;
        variables = variables->next;
    }
    return NULL;
}


/*
** This function is partially implemented for you, but you may
** scrap the implementation as long as it produces the same result.
**
** Creates a new line on the heap with all named variable *usages*
** replaced with their associated values.
**
** Returns NULL if replacement parsing had an error, or (char *) -1 if
** system calls fail and the shell needs to exit.
*/
char *replace_variables_mk_line(const char *line,
                                Variable *variables){
    char * new_line = safe_malloc(strlen(line) * 2 + 1000); 
    new_line[0] = '\0'; 
    
    int new_line_i = 0;
    int line_i = 0;
    while (line[line_i] != '\0') {
       if (line[line_i] != '$') {
          new_line[new_line_i++] = line[line_i++];
          continue;
       }
       // found a '$'
       Variable * var = find_replacement(&line[line_i + 1], variables);
       if (var == NULL) {
          new_line[new_line_i++] = line[line_i++];
          continue;
       }
       // found a matching variable
       strcat(new_line, var->value);
       new_line_i += strlen(var->value); 
       
       line_i += strlen(var->name);
       line_i++;
    }

    new_line[new_line_i] = '\0';
    return new_line;
}

void free_variable(Variable *var, uint8_t recursive){
    while (var != NULL) {
        Variable * tmp = var;
        var = var->next;
        SAFE_FREE(tmp->name);
        SAFE_FREE(tmp->value);
        free(tmp);
        if (!recursive)
            return;
    }

}

void *safe_malloc(size_t s) {
    void *ptr = malloc(s);
    if (ptr == NULL) {
       perror("malloc");
       exit(1);
    }
    return ptr;
}

void *safe_realloc(void * ptr, size_t s) {
    void *_ptr = realloc(ptr, s);
    if (_ptr == NULL) {
       perror("realloc");
       exit(1);
    }
    return _ptr;
}
