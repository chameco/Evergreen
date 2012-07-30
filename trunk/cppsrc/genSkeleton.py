import sys
name = sys.argv[1]
package = sys.argv[2]

print "#ifndef " + name.upper() + "_H"
print "#define " + name.upper() + "_H"
print "//LIBRARY INCLUDES:"
print "#include <string>"
print "//USER INCLUDES:"
print '#include "chameleon.h"'
print "namespace " + package + " {"
print "\tusing namespace std;"
print "\tclass " + name + " {"
print "\t\tpublic:"
print "\t\t\t" + name + "();"
print "\t\tprivate:"
print "\t\t\t"
print "\t};"
print "}"
print "#endif"
