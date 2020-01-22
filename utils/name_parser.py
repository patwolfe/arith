#!/usr/bin/env python
import sys
import csv

def main(argv):
  filename = argv[1]

  with open(filename, newline = '') as infile, open('parsed_' + filename, 'w', newline = '') as outfile:
    reader = csv.reader(infile, dialect = 'excel')
    next(reader)

    writer = csv.writer(outfile, dialect = 'excel')
    writer.writerow(['email','major','first','last'])

    for line in reader:
      outline = []
      outline.extend(line[:-1])

      name = line[2]
      name = name.split()

      first = ''
      last = ''

      if len(name) == 2:
        first = name[0]
        last = name[1]
      elif len(name) >= 3 and len(name[1]) == 2 and name[1][1] == '.':
        first = name[0]
        last = ' '.join(name[2:])
      else:
        done = False
        while not done:
          print('Name is not standard: ' + ' '.join(name) + '. Their email is: ' + line[0] + '. Type "undo" to restart name entry.')
          first = input('First name: ')
          if first == 'undo':
            continue
          last = input('Last name: ')
          if last == 'undo':
            continue
          done = True

      print(first + ' ' + last)
      outline.append(first)
      outline.append(last)

      writer.writerow(outline)

if __name__ == '__main__':
  main(sys.argv)
