# deep_learning_project_text_generation_cs_jk_jz
Deep Learning Course Projection: Text Generation - CS, JK, JZ

# Prerequisite

* pytorch is installed
* Cloned fairseq from the github repo (github.com/pytorch/fairseq)
* All the python files are stored in the fairseq directory

# Preliminary Step

Before using the whole writingPrompt dataset, we sampled 10% of the train, test, valid and saved in the sample folder. We used the following script to sample 10% (assume all the data is stored in examples/stories/writingPrompts

```
$ python sample.py examples/stories/writingPrompts train.wp_target train.wp_source examples/stories/writingPrompts/sample
$ python sample.py examples/stories/writingPrompts test.wp_target test.wp_source examples/stories/writingPrompts/sample
$ python sample.py examples/stories/writingPrompts valid.wp_target valid.wp_source examples/stories/writingPrompts/sample
```

Next we run the preprocess
```
$ export TEXT=examples/stories/sample
```

```$ python preprocess.py --source-lang wp_source --target-lang wp_target --trainpref $TEXT/train --validpref $TEXT/valid --testpref $TEXT/test --destdir data-bin/sample --padding-factor 1 --thresholdtgt 10 --thresholdsrc 10 --worker 4```


# README.sh

## Preprocess the dataset:
First we downloaded the writingPrompt dataset from fairseq github repo.

Note that the dataset release is the full data, but the paper models the first 1000 words of each story
Here is some example code that can trim the dataset to the first 1000 words of each story

```$ python trim.py example/stories/writingPrompts```

## Binarize the dataset:
```$ export TEXT=examples/stories/writingPrompts```

```$ python preprocess.py --source-lang wp_source --target-lang wp_target --trainpref $TEXT/train --validpref $TEXT/valid --testpref $TEXT/test --destdir data-bin/writingPrompts --padding-factor 1 --thresholdtgt 10 --thresholdsrc 10 --worker```

## Train the model:
Trainer.py 

•	Sets up the task (passed as arg) by calling one of the scripts in the folder fairseq/tasks, e.g. fairseq_task.py, translation.py, language_modeling.py  etc. Tasks store dictionaries and provide helpers for loading/iterating over datasets, initializing the Model/Criterion and calculating the loss.

•	Initializes the data loader, pulling the dataset from the folder fairseq/data, and using arguments passed as the training parameters such as learning rate, number of batches etc. 

•	Loads the training, validation split returned by fariseq_task.py

•	Builds model and criterion (by calling task.build_model). Models are located in the folder fairseq/models.

  o	For example, fairseq_model.py contains the base class for the main fusion model in this project. It takes two arguments, the encoder and the decoder, and runs the forward pass for an encoder-decoder model. First feed a batch of source tokens through the encoder. Then, feed the encoder output and previous decoder outputs (i.e., input feeding/teacher forcing) to the decoder to produce the next outputs. 

•	Trains the specified model until learning gets too small (set by threshold min_lr) by building the Trainer (found in trainer.py) 

  o	Trainer.py is the main class for data parallel training. This class supports synchronous distributed data parallel training, where multiple workers each have a full model replica and gradients are accumulated across workers before each update using :class:`~torch.nn.parallel.DistributedDataParallel` to handle communication of the gradients across workers.

  o	Note: only the first validation loss is used to update the learning rate in each epoch.

```$ python train.py data-bin/writingPrompts -a cs_jk_jz_model_wp --lr 0.25 --clip-norm 0.1 --max-tokens 1500 --lr-scheduler reduce_lr_on_plateau --decoder-attention True --encoder-attention False --criterion label_smoothed_cross_entropy --weight-decay .0000001 --label-smoothing 0 --source-lang wp_source --target-lang wp_target --gated-attention True --self-attention True --project-input True --pretrained False```

## Generate:
Note: to load the pretrained model at generation time, you need to pass in a model-override argument to communicate to the fusion model at generation time where you have placed the pretrained checkpoint. By default, it will load the exact path of the fusion model's pretrained model from training time. You should use model-override if you have moved the pretrained model (or are using our provided models). If you are generating from a non-fusion model, the model-override argument is not necessary.

```$ python generate.py data-bin/writingPrompts --path pretrained_model/models/pretrained_checkpoint.pt --batch-size 32 --beam 1 --sampling --sampling-topk 10 --sampling-temperature 0.8 --nbest 1```

```$ python eval_lm.py data-bin/writingPrompts --path 'pretrained_model/models/pretrained_checkpoint.pt' --task translation --max-tokens 32```

```$ python interactive.py --path pretrained_model/models/pretrained_checkpoint.pt --beam 5 --task translation data-bin/writingPrompts```
