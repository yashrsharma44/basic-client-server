import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2

def usage():
    print("usage: wordclient.py server port", file=sys.stderr)

packet_buffer = b''

def get_next_word_packet(s):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """

    def contains_delimeter(buffer : bytes):
        # check and return if the buffer contains
        # the delimeter or not
        # return the position of the index if any
        
        for i, val in enumerate(buffer):
            if val == 0:
                return i
        return -1

    global packet_buffer
    token = None
    # we try to loop through the recv call till we hit a 
    # delimeter. We then try to extract the next token, based
    # on the size of the word expected

    # note that the invariant out here is
    # the buffer contains the starting portion
    # of the word eventually! It may not contain
    # the ending part of the word however.
    while True:
        received_buffer = s.recv(WORD_LEN_SIZE)

        # close the parsing, if the connection is closed
        if not received_buffer:
            return None

        packet_buffer += received_buffer
        # if we find the delimeter, we try to extract the token
        # and check if it's a word_length type or a word
        
        # check if the buffer received contains the delimeter
        index = contains_delimeter(packet_buffer)
        if index != -1:
            # extract the token
            token = packet_buffer[:index]
            packet_buffer = packet_buffer[index+1:]

            if token != b'':
                return token

    return None

def extract_word(word_packet):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """
    # each word packet contains 
    # length of word as the first byte
    # followed by the word itself
    return str(word_packet[1:], encoding='utf-8')

# Do not modify:

def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)

        print(f"    {word}")

    s.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))