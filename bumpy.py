from time import sleep
import math

def areasf(lsm, areas_n=9, minv=-2, delay=0.001):
    mina = abs(minv)
    step = 2 * mina / areas_n
    areas = [0 for i in range(areas_n)]
    n = 0
    while True:
        try:
            a = lsm.read_accel()
        except OSError:
            areas = [0 for i in range(areas_n)]
            n = 0
            continue
        if n > 1000:
            n = 0
            print(areas)
            areas = [0 for i in range(areas_n)]
            continue
        areas[math.floor((a[2] + mina)/step)] += 1
        sleep(delay)
        n += 1

class BumpCounter():
    def __init__(self, lsm):
        self.lsm = lsm
        self.bumps = 0


    def count_bumps(self, delay=0.001, samples=5000):
        isamples = 1 - 1/samples
        isamples2 = 1 - 1/(samples/100)
        avg = 0
        var = 0
        local_var = 0
        bumpflag = False
        print("Initializing average")
        for i in range(samples):
            a = self.lsm.read_accel()[2]
            avg += a / samples
            # var += (a - avg) ** 2 / samples
            sleep(delay)
        print("Entering main cycle")
        while True:
            try:
                a = self.lsm.read_accel()[2]
            except OSError:
                sleep(delay)
                continue
            avg = avg * isamples
            avg += a / samples
            var = var * isamples
            var += (a - avg) ** 2 / samples
            local_var = local_var * 0.99
            local_var += (a - avg) ** 2 / 100
            if (local_var >= var) and (not bumpflag):
                self.bumps += 1
                bumpflag = True
            elif (local_var < var) and bumpflag:
                bumpflag = False
            # print("% 5.5f\t% 5.5f" % (var, local_var))
            sleep(delay)
