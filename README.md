# Mental-State-Decoder
## Predicting mental state using deep learning
 
## Intoduction

This project aims to predict a subject's mental state (focused, relaxed, neutral) by training a model on data collected using a [commercial EEG headband](https://choosemuse.com/shop/) during an experiment. The [dataset](https://www.kaggle.com/birdy654/eeg-brainwave-dataset-mental-state) used was uploaded to kaggle by Jordan Bird. The results of their study is summarized in this [paper](https://ieeexplore.ieee.org/abstract/document/8710576), which aims to classify mental states using feature selection techniques and classical classifiers such as Bayesian Networks, Support Vector Machines and Random Forests, obtaning an overall accuracy over 87%. 

This project aims to compare the performance of deep learning with such classifical models. An average accuracy of 83% is achieved using a simple CNN model.

## The Data

The data was collected from 2 males and 2 females for 60 seconds. Each experiment was repeated twice for each of the 4 subjects. The Muse headband records the TP9, AF7, AF8 and TP10 EEG placements via dry electrodes. The figure below shows the locations of these electrodes.The study categorizes brain waves into 3 possible states defined by cognitive behavioral studies. These include relaxed, concentrating, neutral. For the relaxed state, subjects listened to meditation low-tempo music and were asked to relax their muscles. For the neutral state, a similar test was carried out, but with no music. This test was done before the rest to prevent lasting effects of relaxation and concentration. Finally, for the concentration state, the subjects played a game in which they had to find a ball that was hidden under one of three rotating cups. 

<p align="center">
  <img src="https://github.com/Atlaskz/Mental-State-Predictor/blob/main/muse%20electrodes.png" width="350" height="300">
</p>

Although data augmentation was not used in this project, it is proven to increase accuracy and stability of results for such small datasets.

## Data Processing:

To prepare the data for traning, a band-pass filter of 4-30 Hz was used to filter out the delta (1–4 Hz) and gamma (31–40 Hz) bands while keeping theta (5–8 Hz), alpha (9–13 Hz), lower beta (14–16 Hz), and higher beta (17–30 Hz). Delta and gamma bands were excluded since their activity types are not relevant in this experiment. Delta frequencies are responsible for deep sleep brain activity and gamma frequencies are responsible for high level information processing tasks.  I A window size of 64 was chosen to make use of previous timestamps as features for each row.  

## Deep Learning Model

This project also aimed to study the effect of network depth (convolutions as well as fully connected layers) on the performance of the model. This [paper](https://iopscience.iop.org/article/10.1088/1741-2552/ab260c) summarizes 154 studies on Deep Learning for EEG Decoding, from 2010 to 2018. Based on this paper, the majority of studies found that a shallower network of fully connected layers performed better. After a few rounds of parameter tuning, 3 fully connected layers were chosen. As for the convolutions, it was shown that shallower models outperformed the deeper ones. Hence, 2 convolutions were chosen to start with.

## Training

To test the performance of the model for each subject, each subject's trial was used as the test set separately. Given 2 trials per subject and 4 subjects, the procedure could be considered as an 8-fold cross-validation. However, subject b's trial 2 was missing data for one of the states so the whole trial was skipped. This resulted in 7 trained models instead of 8. 

## Results

The graph below shows the average of the AUC scores of the 2 trials for each subject (for subject b, the score corresponds to the first trial only). The total average AUC score is 83%. The average score for each subject is as follows:

Subject A : 91%

Subject B : 80%

Subject C : 84%

Subject D: 78%

<p align="center">
  <img src="https://github.com/Atlaskz/Mental-State-Predictor/blob/main/chart.png">
</p>

## Wrapping up

The original study used feature engineering and classical machine learning models for this task. They found that with 44 features and classical classifiers such as Bayesian Networks, Support Vector Machines and Random Forests, they could obtain an overall accuracy of around  87%. 

In this project, a score of 83% was achieved with no feature extraction and minimal processing. This score would likely increase with further hyperparameter tuning. The aim of this project was to demonstrate the performance of deep learning for decoding brain activity. One of the known limitations of deep learning is the amount of data required for training. It is only expected to achieve a lower accuracy with limited data. On the other hand, commercial grade EEG headbands are not as reliable as 128 channel headsets used in research labs. However, as more neurtech startups emerge, commercial eeg devices are gaining popularity amongst researchers due to their ease of use and affordability. Hence, there is growing interest in creating models that work well with these devices.

