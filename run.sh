#!/usr/bin/env sh

OUTPUT_FILE=./output
VEC_FILE=./train_img_set/train_set.vec
BG_FILE=./train_img_set/bg.txt
NUM_POS=9000
NUM_NEG=25000
NUM_STAGE=20   
VAL_BUFSIZE=8192
IDX_BUFSIZE=8192
NUM_THREADS=12

STAGE_TYPE=BOOST
FEATURE_TYPE=LBP
WEIGHT=24
HEIGHT=24

BT=GAB
MIN_HITRATE=0.99
MAX_FALSE_ALARM_RATE=0.5
WEIGHT_TRIM_RATE=0.95
MAX_DEPTH=1
MAX_WEAK_COUNT=100

MODE=BASIC


opencv_traincascade \
    -data $OUTPUT_FILE \
    -vec $VEC_FILE \
    -bg $BG_FILE \
    -numPos $NUM_POS \
    -numNeg $NUM_NEG \
    -numStages $NUM_STAGE \
    -precalcValBufSize $VAL_BUFSIZE \
    -precalcIdxBufSize $IDX_BUFSIZE \
    -numThreads $NUM_THREADS \
    -stageType $STAGE_TYPE \
    -featureType $FEATURE_TYPE \
    -w $WEIGHT \
    -h $HEIGHT \
    -bt $BT \
