# Mental-State-Predictor
## Predicting mental state using deep learning
 
## Intoduction

In my previous project [Bionic AI](https://github.com/Atlaskz/Bionic-AI-Predicting-Grasp-and-Lift-Motions), I mentioned my interest in designing a real time mental state prediction experiment. I have been inspired by the increasing collaboration between computer science experts and neuroscientists for transforming neurotechnology in ways that will revolutionize many industries. This collaboration can result in a new level of human-machine symbiosis with the goal of improving the lives of people suffering from various mental and muscle disorders as well as healthy individuals.

To do this, the first thing I needed was an EEG headset. I decided on a [muse 2 headband](https://choosemuse.com/muse-2/) because of the growing research community around using Muse devices for EEG data collection and analysis. My goal was to use the Muse headband to collect my own data by designing an experiment for mental state recognition. This would then allow me to predict mental state in real time.

I ordered the headset around a month ago and expected it to be delivered within a week. However, what I did not account for at the time was Christmas holidays mail delays. When I realized I am not getting my headband anytime soon, I decided to start the project by using similar data collected from a muse headband by other researchers. I came across a [dataset](https://www.kaggle.com/birdy654/eeg-brainwave-dataset-mental-state) for mental state classification uploaded on Kaggle by Jordan Bird. In this article, I will go over my methods and results using this dataset.

## The Data

The data was collected from 2 males and 2 females for 60 seconds. Each experiment was repeated twice for each of the 4 subjects. The Muse headband records the TP9, AF7, AF8 and TP10 EEG placements via dry electrodes. The figure below shows the locations of these electrodes. The mental states considered for the experiment included relaxed, concentrating, neutral. For the relaxed state, subjects listened to meditation low-tempo music and were asked to relax their muscles. For the neutral state, a similar test was carried out, but with no music. This test was done before the rest to prevent lasting effects of relaxation and concentration. Finally, for the concentration state, the subjects played a game in which they had to find a ball that was hidden under one of three rotating cups. To learn more about the experiment, you can check out the [original study](https://www.researchgate.net/publication/328615252_A_Study_on_Mental_State_Classification_using_EEG-based_Brain-Machine_Interface).

<p align="center">
  <img src="https://github.com/Atlaskz/Mental-State-Predictor/blob/main/muse%20electrodes.png" width="350" height="300">
</p>



Even though the dataset was small, I did not use any data augmentation techniques. I planned on doing so if the results achieved without augmentation were not promising. As you will see soon, the results were pretty good even without data augmentation. However, in many studies, augmentation is proven to increase accuracy and stability when done properly.

## Data Processing:

Preprocessing EEG data usually includes a few general steps. These are downsampling, band-pass filtering, and windowing. For this project, I first used a band-pass filter of 4-30 Hz to filter out  delta (1–4 Hz) and gamma (31–40 Hz) bands while keeping theta (5–8 Hz), alpha (9–13 Hz), lower beta (14–16 Hz), higher beta (17–30 Hz). The reason for excluding delta and gamma bands was that these activity types are not relevant in this experiment (as you will see soon). Delta frequencies are responsible for deep sleep brain activity and gamma frequencies are responsible for high level information processing tasks.  I then used a windowing technique with a window size of 64 to make use of the previous timestamps as features for each data point. Initially, I also used independent component analysis (ICA) to separate ocular components from the data, however, this seemed to decrease the performance of the model, so I ended up skipping this step. 

## Deep Learning Model

Since I used PyTorch for my previous project, I went with TensorFlow this time. As for the deep learning model, I went with a deep CNN Model with 1d convolutions since this model gave me good results in my previous project. 


For this project, I wanted to explore the effect of network depth on the performance of the model. I was interested in altering the depth of both the fully connected layers and the CNN. Since pure trial and error for this type of hyper parameter tuning can get very complicated and take a long time, I looked on the web for some guidance. I came across an [amazing paper](https://iopscience.iop.org/article/10.1088/1741-2552/ab260c) that summarizes 154 studies on Deep Learning for EEG Decoding, from 2010 to 2018. Based on this paper, the majority of studies found that a shallower network of fully connected layers performed better. I tested out various numbers of layers and settled on 3. As for the CNN, in one of the studies, models with 2 and 3 convolutional layers were compared. The results showed that the shallower model outperformed the deeper one in all scenarios. So I decided to start with 2 layers of convolutions as well.

## Training

BTo test the performance of the model for each subject, I used each trial from every subject as the test set separately. The procedure would have been similar to an 8-fold cross-validation  (4 subjects and 2 trials each) , except that subject b trial 2 was missing data for one of the mental states and I decided to skip it. This resulted in 7 trained models instead of 8. 

In the previous project, I achieved the highest AUC score when I first trained the model on all the data, and a second time on each subject individually. This time, I achieved a pretty good score from just the first step (training the model on all data) and for the sake of time, I did not go any further.

## Results

The graph below shows the average AUC score for each subject individually (for subject b, the score corresponds to the first trial only). The total average AUC score is 83%. The average score for each subject is as follows:

Subject A : 91%

Subject B : 80%

Subject C : 84%

Subject D: 78%

<p align="center">
  <img src="https://github.com/Atlaskz/Mental-State-Predictor/blob/main/chart.png">
</p>

## Wrapping up

The original study used feature engineering and traditional machine learning models for this classification task. They found that with 44 features and classical classifiers such as Bayesian Networks, Support Vector Machines and Random Forests, they could obtain an overall accuracy of around  87%. 

A score of 83%, with no extracted features and minimal processing from only a few lines of code seems like a great start to me. This also shows the potential of deep learning for decoding brain activity. As you might know, one of the limitations of deep learning models are the amount of data they need for training. And this dataset is very small compared to what’s used for computer vision projects where deep learning is having stellar performance. This is probably the main reason for not achieving an accuracy score of over 90% from deep learning. Another reason could be the use of a commercial grade EEG headband as opposed to performing the experiments in a lab. However, as these headbands are becoming more popular for research purposes, it is important to optimize models to work well with them. For these reasons, I’m interested in using data augmentation and further hyper parameter tuning to observe the change in the overall accuracy of the model.

Furthermore, as I mentioned at the beginning of the post, my original intention was to design my own experiment so I can use the Muse headband for predicting mental state in real time.  So staye tuned for part 2 of this project when I receive my muse headband in the mail. 

