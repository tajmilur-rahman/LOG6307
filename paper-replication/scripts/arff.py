__author__ = 'lquerel'

from settings.postgres import Postgres
import math

postgres = Postgres()

metrics = postgres.get_all_metrics()
RQ1 = open('rq1.arff', 'w')
RQ3 = open('rq3.arff', 'w')

header = "% Django \n" \
         "@relation DJANGO\n" \
         "@attribute transaction NUMERIC\n" \
         "@attribute commit STRING\n" \
         "@attribute ns NUMERIC\n" \
         "@attribute nd NUMERIC\n" \
         "@attribute nf NUMERIC\n" \
         "@attribute entropy NUMERIC\n" \
         "@attribute la NUMERIC\n" \
         "@attribute ld NUMERIC\n" \
         "@attribute fix {0,1}\n" \
         "@attribute ndev NUMERIC\n" \
         "@attribute age NUMERIC\n" \
         "@attribute nuc NUMERIC\n" \
         "@attribute exp NUMERIC\n" \
         "@attribute rexp NUMERIC\n" \
         "@attribute sexp NUMERIC\n" \
         "@attribute bug {0,1}\n" \
         "@data\n"

RQ1.write(header)
RQ3.write(header)

print header

def process(value):
    if not value:
        return 0
    else:
        return value

def process_log(value):
    value = process(value)
    return math.log10(value)


def process_boolean(value):
    if not value:
        return 0
    else:
        return 1 if value else 0

for metric in metrics:

    row = "%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % \
          (metric[0],
           metric[1],
           metric[2],
           metric[3],
           metric[4],
           process(metric[5]),
           process(metric[6]),
           process(metric[7]),
           process_boolean(metric[8]),
           process(metric[9]),
           process(metric[10]),
           process(metric[11]),
           process(metric[12]),
           process(metric[13]),
           process(metric[14]),
           process_boolean(metric[15]))
    RQ1.write(row)

    row = "%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % \
          (metric[0],
           metric[1],
           process_log(metric[2]),
           process_log(metric[3]),
           process_log(metric[4]),
           process_log(metric[5]),
           process_log(metric[6]),
           process_log(metric[7]),
           process_boolean(metric[8]),
           process_log(metric[9]),
           process_log(metric[10]),
           process_log(metric[11]),
           process_log(metric[12]),
           process_log(metric[13]),
           process_log(metric[14]),
           process_boolean(metric[15]))
    RQ3.write(row)
    
    pass

RQ1.close()
