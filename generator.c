#include <stdio.h>
#include <stdlib.h>

#define N 100001
#define INT_MIN 0
#define INT_MAX 4


int main()
{
    FILE *file = fopen("input.txt", "w");
    char letters[] = {'a', 'b', 'c', 'd', 'e'};
    char letter;

    for (int i = 0; i < N; i++) {
        letter = letters[rand() % (INT_MAX - INT_MIN + 1) + INT_MIN];
        fprintf(file, "%c", letter);
    }

    fclose(file);
}