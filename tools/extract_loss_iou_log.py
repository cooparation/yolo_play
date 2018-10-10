# coding=utf-8

###################################################
# this tool is used to extract the log of loss and IOU
# and then help to visualize it based on this logs
# visual loss to see train_loss_visualization.py
# visual iou to see train_iou_visualization.py 
###################################################

def extract_log(log_file,new_log_file,key_word):

    f = open(log_file)
    train_log = open(new_log_file, 'w')

    for line in f:
        # remove multi gpu synchronous log
        if 'Syncing' in line:
            continue
        # remove nan error log
        if 'nan' in line:
            continue
        if key_word in line:
            train_log.write(line)

    f.close()
    train_log.close()


extract_log('paul_train_log.txt','paul_train_log_loss.txt','images')
extract_log('paul_train_log.txt','paul_train_log_iou.txt','IOU')
