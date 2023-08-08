# btc_puzzle
This program is only being used to solve bitcoin puzzles.

Use btc_puzzle.py to try your luck!
-

The number of 0 and 1 in a 66-bit binary number can be specified to reduce the key space. It is calculated that if combinations of 0 or 1 with a probability of occurrence greater than 41% are used, the key space will be reduced to about 44.56% of the puzzle 66.

It was originally used to solve Puzzle 66, if you want to solve other puzzles with it, follow the steps below to modify the code:

Step 1: Modify the 'target_hash' value, it's public key hashed value(hash 160)

Step 2: Modify the 'private_key_bin' value, initial is {'0' * (256 - 66) + private_key_bin}, just change '66' to the number of the puzzle

Step 3: Modify the 't' value, initial is {threading.Thread(target=worker, args=(31, 35))}, change '31' to the number of 0 and '35' to number of 1

In addition
-
Change the value of 'num_threads' to use more threads for the calculation

Good Luck!
-
