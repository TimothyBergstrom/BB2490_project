#include <stdio.h>
#include <stdlib.h>
#define BUFMAX 1000

int main(){
	char buffer[BUFMAX + 1];
	FILE *ptr;  // Pointer to file
	char c;
	char line[10000];
	fgets(buffer, sizeof(buffer), stdin);  // stdin to string
	ptr = fopen(buffer, "r");
	int line_count = 0;  // Count lines, clear the first 4
	if(ptr != NULL){  // Check if we can open file
		while(fgets(line, sizeof(line), ptr)){
			line_count++;
		}
	}
	fclose(ptr);
	printf("%d", line_count);
}