#include <fcntl.h>
#include <stdlib.h>

int main(void) {
  // invalid_free
  int *a = malloc(1);

  free(a);
  free(a);

  // invalid_read
  int *b = malloc(1);

  b[0] = b[1];
  free(b);

  // invalid write
  int *c = malloc(1);

  c[1] = '0';
  free(c);

  // no free
  char *d = malloc(1);

  // realloc zero
  int *e = NULL;

  e = realloc(e, 0);

  // unclosed fd
  int f = open("unclosed.txt", O_CREAT | O_WRONLY);

  return 0;
}
