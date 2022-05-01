from multiprocessing import Pool
import os
import logging
import logging.handlers
import utilitaires

count = 0
def f(x):
   global count
   count += 1
   #print("Input {} in process {}".format(x, os.getpid()))
   logger = logging.getLogger("app")
   #logger.info("f({}) count {} in PID {}".format(x, count, os.getpid()))
   logger.info(f"f({x}) count {count} in PID {os.getpid()}")
   return x*x


def prt(z):
   print(z)
   

def main():

   logger = utilitaires.logging.getLogger('app')
   logger.info("main")

   with Pool(5) as p:
       results = p.imap(f, range(110)) # <multiprocessing.pool.IMapIterator object
       print(results)
       print('--')
       for r in results:
           print(r)


if __name__ == '__main__':
   main()