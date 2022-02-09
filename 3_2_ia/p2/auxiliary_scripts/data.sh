# Small script to store data from a game (both players) in two different files for each player
NAME="depth4_times_pruning"
cat "${NAME}.txt" | awk '{if (NR % 2 == 1) print int((NR+1)/2) " " $s}' > "${NAME}_p1.dat"
cat "${NAME}.txt" | awk '{if (NR % 2 == 0) print NR/2 " " $s}' > "${NAME}_p2.dat"