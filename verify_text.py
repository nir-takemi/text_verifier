import sys

from textverifier import text_verifier as tv

def main():
    args = sys.argv
    if len(args) < 2 :
        raise ValueError('''
            Specify at least 1 argument.
            usage:
                python3 text_verifier.py "dir or file_path"
        ''')

    # Execute
    text_verifier = tv.TextVerifier(args[1])
    text_verifier.verify()


if __name__ == '__main__':
    main()