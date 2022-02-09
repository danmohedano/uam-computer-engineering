import graphs10
import tgf

print(''.join(['-']*30))
for i in range(50):
    if not graphs10.check_sequencing(30, 8):
        print('False')
