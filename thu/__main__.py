import sys

if len(sys.argv) < 2:
    print("usage: thu module [command]")
    exit(0)

module = sys.argv[1]
command = sys.argv[2] if len(sys.argv) > 2 else "main"

m = __import__(module, globals(), locals())
getattr(m, command)(*sys.argv[3:])
