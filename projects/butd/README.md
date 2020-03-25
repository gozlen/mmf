# BUTD

This repository contains the code for pytorch implementation of BUTD model, released originally under this ([repo](https://github.com/peteanderson80/bottom-up-attention)). Please cite the following paper if you are using BUTD model from pythia:

* Anderson, P., He, X., Buehler, C., Teney, D., Johnson, M., Gould, S., & Zhang, L. (2018). *Bottom-up and top-down attention for image captioning and visual question answering*. In Proceedings of the IEEE conference on computer vision and pattern recognition (pp. 6077-6086). ([arXiV](https://arxiv.org/abs/1707.07998))
```
@inproceedings{Anderson2017up-down,
  author = {Peter Anderson and Xiaodong He and Chris Buehler and Damien Teney and Mark Johnson and Stephen Gould and Lei Zhang},
  title = {Bottom-Up and Top-Down Attention for Image Captioning and Visual Question Answering},
  booktitle={CVPR},
  year = {2018}
}
```

## Installation

Clone this repository, and build it with the following command.
```
cd ~/pythia
python setup.py build develop
```

## Training
To train BUTD model on the COCO Captions dataset, run the following command
```
python tools/run.py --config configs/captioning/coco/butd.yml --run_type train_val --dataset coco --model butd
```

For training BUTD model use the config `butd.yml` only. Training uses greedy decoding for validation. Currently we do not have support to train the model using beam search or nucleus sampling decoding. For inference, any of the following methods can be used:

- Greedy Decoding (`butd.yml`)
- Beam Search Decoding (`butd_beam_search.yml`)
- Nucleus Sampling Decoding (`butd_nucleus_sampling.yml`)