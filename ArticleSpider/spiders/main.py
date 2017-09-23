# -*- coding: utf-8 -*-
from scrapy.cmdline import  execute
import sys
import os
import numpy.random
import matplotlib.pyplot

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(['scrapy','crawl','jobbole'])

if __name__ == '__main__':
    matplotlib.pyplot.yticks()
    a = numpy.array([1,2,3])
    numpy.random.normal()
    print type(a)
