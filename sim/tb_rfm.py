
import time
import numpy as np

NUM_ENTRY = 512
NUM_ROW = 2000
TRACE_SIZE = 2000

RFM_TH = 649

if __name__ == '__main__':

  #np.random.seed(777)
  np.random.seed(int(time.time()))

#  trace = np.random.randint(1, NUM_ROW+1, size=TRACE_SIZE)
#  np.savetxt('trace.txt', trace, fmt = '%d')
  trace = np.loadtxt('trace.txt', dtype = 'int')

  table = []
  for _ in range(NUM_ENTRY):
    table.append([0,0])
  len_table = 0  

  spcnt = 0

  act_cnt = 0

  for act_row in trace:
    act_cnt += 1
    print("////////  ACT{:>12d} ////////".format(act_cnt))
    print("ACT Address :{:>7d}".format(act_row))
    act_row = act_row
    exist = False
    for i, row in enumerate(table):
      if row[0] == act_row:
        row[1] += 1
        exist = True
    if not exist:
      min_cnt = table[0][1]
      for i, row in enumerate(table):
        if min_cnt > row[1]:
          min_cnt = row[1]
      if min_cnt == spcnt:
        for i, row in enumerate(table):
          if row[1] == spcnt:
            row[0] = act_row
            row[1] = spcnt + 1
            break
      else:
        spcnt += 1

    for i, row in enumerate(table):
      print("{:>11d}: {:>6d}, {:>10d}".format(i, row[0], row[1]))
    print("\n")   

    if act_cnt % RFM_TH == 0:
      max_cnt = table[0][1]
      for i, row in enumerate(table):
        if max_cnt < row[1]:
          max_cnt = row[1]
      for i, row in enumerate(table):
        if row[1] == max_cnt:
          row[1] = spcnt
          break


