/*
 * This is a multi-line comment
 * to test the lexical analyzer.
*/
int main() {
    int count = 100;
    string message = "Hello World!";
    char grade = 'A';

    if (count = 10) { // Single equals is a valid token
        /* A simple comment */
        count = count + 1;
    }

    // The following lines contain errors
    string bad_str = "this string never ends
    char bad_char = 'too_long';
    int invalid_#symbol = 5;
}

/* This comment is never closed.