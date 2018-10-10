import argparse
import sys
import matplotlib.pyplot as plt

# refer to the blog: https://www.jianshu.com/p/7ae10c8f7d77

#################################
# after run: darknet detector train ./cfg/voc.data cfg/tiny_yolo_voc.cfg tiny_yolo_voc.weights >>log training.log 
# Usage: python  drawcurve.py training.log 0
#################################

##############################
# examples of the log:
# 1001: 32.500572, 31.886116 avg, 0.020000 rate, 17.405710 seconds, 512512 images
# iteration: train_loss, avg train_loss, learning rate, one batch process time, the total image haved processed
#
# Loaded: 0.000550 seconds
# Region Avg IOU: 0.828491, Class: 0.967888, Obj: 0.000023, No Obj: 0.000122, Avg Recall: 1.000000,  count: 29
#| Region Avg IOU: (the intersection of predict bbox and Ground-truth
#        bbox)/(the union of predict bbox and Ground-truth bbox)
# Avg Recall: (the predicted object num)/(the labeled object num)
# count: the labed num of all the images(never mind the catogary)
###############################


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("log_file",  help = "path to log file"  )
    parser.add_argument( "option", help = "0 -> loss vs iter"  )
    args = parser.parse_args()
    f = open(args.log_file)
    lines  = [line.rstrip("\n") for line in f.readlines()]
    # skip the first 3 lines
    lines = lines[3:]
    numbers = {'1','2','3','4','5','6','7','8','9','0'}
    iters = []
    loss = []
    for line in lines:
        if line[0] in numbers:
            args = line.split(" ")
            if len(args) >3:
                iters.append(int(args[0][:-1]))
                loss.append(float(args[2]))
    plt.plot(iters,loss)
    plt.xlabel('iters')
    plt.ylabel('loss')
    plt.grid()
    plt.show()
if __name__ == "__main__":
    main(sys.argv)
