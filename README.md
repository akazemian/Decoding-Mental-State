## Predicting mental state using deep learning
 
## Intoduction

This project aims to predict a subject's mental state (focused, relaxed, neutral) by training a model on data collected using a [commercial EEG headband](https://choosemuse.com/shop/) during an experiment. The [dataset](https://www.kaggle.com/birdy654/eeg-brainwave-dataset-mental-state) was introduced in a [study](https://ieeexplore.ieee.org/abstract/document/8710576) that aims to classify mental states using feature selection techniques and classical classifiers such as Bayesian Networks, Support Vector Machines and Random Forests, obtaning an overall accuracy of over 87%. 

This project aims to explore the performance of deep learning models for this task. An average accuracy of 83% is achieved using a simple CNN model.

## Data

The data was collected from 2 males and 2 females for 60 seconds. Each experiment was repeated twice for each of the 4 subjects. The Muse headband records the TP9, AF7, AF8 and TP10 EEG placements via dry electrodes. The figure below shows the locations of these electrodes.The study categorizes brain waves into 3 possible states defined by cognitive behavioral studies. These include relaxed, concentrating, neutral. For the relaxed state, subjects listened to meditation low-tempo music and were asked to relax their muscles. For the neutral state, a similar test was carried out, but with no music. This test was done before the rest to prevent lasting effects of relaxation and concentration. Finally, for the concentration state, the subjects played a game in which they had to find a ball that was hidden under one of three rotating cups. 

<p align="center">
  <img src="https://github.com/Atlaskz/Mental-State-Predictor/blob/main/muse%20electrodes.png" width="350" height="300">
</p>

## Data Processing:

To prepare the data for traning, a band-pass filter of 4-30 Hz was used to filter out the delta (1–4 Hz) and gamma (31–40 Hz) bands while keeping theta (5–8 Hz), alpha (9–13 Hz), lower beta (14–16 Hz), and higher beta (17–30 Hz). Delta and gamma bands were excluded since their activity types are not relevant in this experiment. Delta frequencies are responsible for deep sleep brain activity and gamma frequencies are responsible for high level information processing tasks. A window size of 64 was chosen to make use of previous timestamps as features for each row.   

Although data augmentation was not used in this project, it is proven to increase accuracy and stability of results for small datasets.

## Deep Learning Model

This project also aims to study the effect of network depth (convolutions and fully connected layers) on model performance. This [paper](https://iopscience.iop.org/article/10.1088/1741-2552/ab260c) summarizes 154 studies focused on using deep learning for EEG decoding. The majority of studies found that a shallower network of convolutions and fully connected layers performed better than deeper networks. Therefore a shallow network architecture was used in this project. 

## Training

To test the performance of the model for each subject, each subject's trials were used as the test set individually. With 4 subjects and 2 trials per subject, the procedure could be considered as an 8-fold cross-validation. However, subject b's second trial was missing data for one of the 3 states, and was skipped. This resulted in 7 trained models instead of 8. 

## Results

The graph below shows the mean AUC score from each subjects' trials (for subject b, the score corresponds to the first trial only). The total average AUC score was found to be 83%. The mean AUC score for each subject is as follows:

Subject A : 91%

Subject B : 80%

Subject C : 84%

Subject D: 78%

<p align="center">
  <img src="https://github.com/Atlaskz/Mental-State-Predictor/blob/main/chart.png">
</p>

## Discussion

The original study used feature engineering and classical machine learning models for this task. They found that with 44 features and classical classifiers such as Bayesian Networks, Support Vector Machines and Random Forests, an overall accuracy of around  87% was attained. 

In this project, a score of 83% was achieved with no feature extraction and minimal processing. This score would likely increase with further hyperparameter tuning (including the optimizer, learning rate, batchsize, number of epochs). The aim of this project was to simply demonstrate the performance of deep learning models for decoding brain activity. One of the known limitations of deep learning is the amount of data required for training. With more trials per subject, the performance of the model is likely to imporve. Moreover, commercial grade EEG headbands are not as reliable as 64-128 channel headsets used in research labs. However, as more neurotech companies emerge, commercial EEG devices are gaining popularity amongst researchers due to their ease of use and affordability. Hence, there is growing interest in creating models that work well with these devices.

