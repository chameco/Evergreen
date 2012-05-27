import sys
def dotify(string):
    buffer = ""
    for char in string:
        if not char.isalnum() and char != "_":
            buffer += "_"
        else:
            buffer += char
    return buffer
def main():
    nodes = []
    file = open(sys.argv[1], "r")
    for line in file:
        both = line.split("->")
        both[0] = "".join(both[0].strip().split(";"))
        both[1] = "".join(both[1].strip().split(";"))
        d1 = dotify(both[0])
        d2 = dotify(both[1])
        if d1 not in nodes:
            nodes.append(d1 + "[label=\"" + both[0] + "\"];")
        if d2 not in nodes:
            nodes.append(d2 + "[label=\"" + both[1] + "\"];")
    print "\n".join(nodes)
if __name__ == "__main__":
    main()
