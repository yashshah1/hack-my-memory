#!/usr/bin/env python3
"""
No error handling done.
Run it as:
python3 name.py <pid of your c code> <string to replace> <replacement string>

NOTE: YOU MIGHT HAVE TO RUN THIS WITH SUDO
"""
from sys import argv

_, pid, initial_string, new_string = argv[:4]

maps_filename = "/proc/{}/maps".format(pid)
mem_filename = "/proc/{}/mem".format(pid)

maps_file = open(maps_filename, 'r')

maps_file_line = maps_file.readline()

while maps_file_line:
  temp = maps_file_line.split()
  if temp[-1] != "[heap]":
    # If the line isn't describing the heap, move on.
    maps_file_line = maps_file.readline()
  else:
    print("* Found the heap")
    addr_range, perm, offset, dev, inode, path = temp
    print("* Address range: ", addr_range)
    print("* Permissions: ", perm)

    try:
      assert('r' in perm and 'w' in perm) # Making sure we have all the permissions.
    except:
      print("Couldn't find permissions, try running with sudo?")
      maps_file.close()
      exit(1)
    
    low, high = addr_range.split("-") # Getting the addresses
    low = int(low, 16) # Getting it from Base 16
    high = int(high, 16) # Getting it from Base 16

    print("The heap starts at: {}".format(low))
    print("The heap ends at: {}".format(high))


    mem_file = open(mem_filename, 'rb+')

    # Now we want to seek to the start of our heap, which is given to us by low
    mem_file.seek(low)

    # Now, we read the size of our heap
    heap = mem_file.read(high - low)

    # Now let's find our string
    # Because our heap is stored in binary, we'll convert our string to binary
    try:
      start_index = heap.index(bytes(initial_string, "ASCII"))
    except ValueError:
      print("Did not find {} in heap, are you sure that's what you want?".format(initial_string))
      maps_file.close()
      mem_file.close()
      exit(1)
    
    print("* Found {}".format(initial_string))

    print("* Writing {} in the heap".format(new_string))

    mem_file.seek(low + start_index) # Get back to where we want to write it
    mem_file.write(bytes(new_string, "ASCII"))

    maps_file.close()
    mem_file.close()
  
    break



