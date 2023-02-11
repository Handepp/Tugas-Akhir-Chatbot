import time

print (time.strftime("%A, %d %b %Y %H:%M:%S"))

import locale
locale.setlocale(locale.LC_TIME, "id_ID") # swedish

waktu = time.strftime("%H %M")
b = "Pukul"
print (b + ' ' + waktu)

