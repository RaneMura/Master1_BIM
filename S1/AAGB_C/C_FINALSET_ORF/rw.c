#include<stdio.h>

int main () {
   FILE *fp;
   char str[] = "This is tutorialspoint.com";

   fp = fopen( "file.txt" , "w" );
   fwrite(str , 1 , sizeof(str) , fp );

   fclose(fp);
  
   return(0);
}

int main () {
   FILE *fp;
   char c[] = "this is tutorialspoint";
   char buffer[100];

   /* Open file for both reading and writing */
   fp = fopen("file.txt", "w+");

   /* Write data to the file */
   fwrite(c, strlen(c) + 1, 1, fp);

   /* Seek to the beginning of the file */
   fseek(fp, 0, SEEK_SET);

   /* Read and display data */
   fread(buffer, strlen(c)+1, 1, fp);
   printf("%s\n", buffer);
   fclose(fp);
   
   return(0);
}


int main () {
   FILE *fp;
   int ch;

   fp = fopen("file.txt", "w+");
   for( ch = 33 ; ch <= 100; ch++ ) {
      fputc(ch, fp);
   }
   fclose(fp);

   return(0);
}


int main () {
   FILE *fp;

   fp = fopen("file.txt", "w+");

   fputs("This is c programming.", fp);
   fputs("This is a system programming language.", fp);

   fclose(fp);
   
   return(0);
}

int main () {
   FILE * fp;

   fp = fopen ("file.txt", "w+");
   fprintf(fp, "%s %s %s %d", "We", "are", "in", 2012);
   
   fclose(fp);
   
   return(0);
}

int main () {
   char str1[10], str2[10], str3[10];
   int year;
   FILE * fp;

   fp = fopen ("file.txt", "w+");
   fputs("We are in 2012", fp);
   
   rewind(fp);
   fscanf(fp, "%s %s %s %d", str1, str2, str3, &year);
   
   printf("Read String1 |%s|\n", str1 );
   printf("Read String2 |%s|\n", str2 );
   printf("Read String3 |%s|\n", str3 );
   printf("Read Integer |%d|\n", year );

   fclose(fp);
   
   return(0);
}