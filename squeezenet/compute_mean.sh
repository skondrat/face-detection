echo "Computing image mean... "

/home/vlad/face-detection/caffe/build/tools/compute_image_mean /home/vlad/face-detection/images/train_lmdb/ /home/vlad/face-detection/images/train_mean.binaryproto
/home/vlad/face-detection/caffe/build/tools/compute_image_mean /home/vlad/face-detection/images/val_lmdb/ /home/vlad/face-detection/images/val_mean.binaryproto

echo "Done."
