#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef char* string;

string int_to_binary(int number);

int main(void) {
    char message[500];
    printf("Enter the string: ");
    fgets(message, sizeof(message), stdin);
    message[strcspn(message, "\n")] = '\0';

    int len = strlen(message);

    int messarray[len];
    char *array_unicode[len];

    // Convert characters to integers
    for (int i = 0; i < len; i++) {
        messarray[i] = (unsigned char)message[i];
    }

    printf("\nASCII values:\n");
    for (int i = 0; i < len; i++) {
        printf("%d ", messarray[i]);
    }

    printf("\n\nBinary (8-bit):\n");
    for (int i = 0; i < len; i++) {
        array_unicode[i] = int_to_binary(messarray[i]);
        printf("%s ", array_unicode[i]);
    }

    printf("\n");

    // Free allocated memory
    for (int i = 0; i < len; i++) {
        free(array_unicode[i]);
    }

    return 0;
}

string int_to_binary(int number) {
    char *binary = malloc(9); 
    if (!binary) return NULL;

    binary[8] = '\0';

    for (int i = 7; i >= 0; i--) {
        binary[i] = (number & 1) ? '1' : '0';
        number >>= 1;
    }

    return binary;
}
