# Preprocess the dataset:
# Note that the dataset release is the full data, but the paper models the first 1000 words of each story
# Here is some example code that can trim the dataset to the first 1000 words of each story
$ python trim.py 'example/stories/writingPrompts'

# Binarize the dataset:
$ export TEXT=examples/stories/writingPrompts
$ python preprocess.py --source-lang wp_source --target-lang wp_target --trainpref $TEXT/train --validpref $TEXT/valid --testpref $TEXT/test --destdir data-bin/writingPrompts --padding-factor 1 --thresholdtgt 10 --thresholdsrc 10

# Train the model:
$ python train.py data-bin/writingPrompts -a fconv_self_att_wp --lr 0.25 --clip-norm 0.1 --max-tokens 1500 --lr-scheduler reduce_lr_on_plateau --decoder-attention True --encoder-attention False --criterion label_smoothed_cross_entropy --weight-decay .0000001 --label-smoothing 0 --source-lang wp_source --target-lang wp_target --gated-attention True --self-attention True --project-input True --pretrained True --pretrained-checkpoint pretrained_model/models/pretrained_checkpoint.pt

$ python train.py data-bin/writingPrompts -a cs_jk_jz_model_wp --lr 0.25 --clip-norm 0.1 --max-tokens 1500 --lr-scheduler reduce_lr_on_plateau --decoder-attention True --encoder-attention False --criterion label_smoothed_cross_entropy --weight-decay .0000001 --label-smoothing 0 --source-lang wp_source --target-lang wp_target --gated-attention True --self-attention True --project-input True --pretrained False
# Train a fusion model:
# add the arguments: --pretrained True --pretrained-checkpoint path/to/checkpoint

# Download pretrained model
# $ curl https://s3.amazonaws.com/fairseq-py/models/stories_checkpoint.tar.bz2 | tar xvjf -

# Generate:
# Note: to load the pretrained model at generation time, you need to pass in a model-override argument to communicate to the fusion model at generation time where you have placed the pretrained checkpoint. By default, it will load the exact path of the fusion model's pretrained model from training time. You should use model-override if you have moved the pretrained model (or are using our provided models). If you are generating from a non-fusion model, the model-override argument is not necessary.

$ python generate.py data-bin/writingPrompts --path pretrained_model/models/pretrained_checkpoint.pt --batch-size 32 --beam 1 --sampling --sampling-topk 10 --sampling-temperature 0.8 --nbest 1 --model-overrides "{'pretrained_checkpoint':'pretrained_model/models/fusion_checkpoint.pt'}"

$ python eval_lm.py data-bin/writingPrompts --path 'pretrained_model/models/pretrained_checkpoint.pt' --task translation --max-tokens 32

$ python interactive.py --path pretrained_model/models/pretrained_checkpoint.pt --beam 5 --task translation data-bin/writingPrompts