echo "Creating train lmdb..."

GLOG_logtostderr=1 /home/vlad/face-detection/caffe/build/tools/convert_imageset \
    --resize_height=210 \
    --resize_width=210 \
    --shuffle \
    /home/vlad/face-detection/images/train/ \
    /home/vlad/face-detection/images/train.txt \
    /home/vlad/face-detection/images/train_lmdb

echo "Creating val lmdb..."

GLOG_logtostderr=1 /home/vlad/face-detection/caffe/build/tools/convert_imageset \
    --resize_height=210 \
    --resize_width=210 \
    --shuffle \
    /home/vlad/face-detection/images/val/ \
    /home/vlad/face-detection/images/val.txt \
    /home/vlad/face-detection/images/val_lmdb

echo "Done."
