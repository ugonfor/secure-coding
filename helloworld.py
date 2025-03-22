import sys

def helloworld(command):
    print("Hello World!")
    print("You entered: " + command)

if __name__ == "__main__":
    assert len(sys.argv) == 2, "Usage: python helloworld.py <comment>"
    helloworld(sys.argv[1])