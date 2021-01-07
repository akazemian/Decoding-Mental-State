# Mental-State-Predictor
## Predicting mental state using deep learning
 
## Intoduction

In my previous project [Bionic AI](), I mentioned my interest in designing a real time mental state prediction experiment. I have been inspired by the increasing collaboration between computer science experts and neuroscientists for transforming neurotechnology in ways that will revolutionize many industries. This collaboration can result in a new level of human-machine symbiosis with the goal of improving the lives of people suffering from various mental and muscle disorders as well as healthy individuals.

To do this, the first thing I needed was an EEG headset. I decided on a [muse 2 headband](https://choosemuse.com/muse-2/) because of the growing research community around using Muse devices for EEG data collection and analysis. My goal was to use the Muse headband to collect my own data by designing an experiment for mental state recognition. This would then allow me to predict mental state in real time.

I ordered the headset around a month ago and expected it to be delivered within a week. However, what I did not account for at the time was Christmas holidays mail delays. When I realized I am not getting my headband anytime soon, I decided to start the project by using similar data collected from a muse headband by other researchers. I came across a [dataset](https://www.kaggle.com/birdy654/eeg-brainwave-dataset-mental-state) for mental state classification uploaded on Kaggle by Jordan Bird. In this article, I will go over my methods and results using this dataset.

## The Data

The data was collected from 2 males and 2 females for 60 seconds. Each experiment was repeated twice for each of the 4 subjects. The Muse headband records the TP9, AF7, AF8 and TP10 EEG placements via dry electrodes. The figure below shows the locations of these electrodes. The mental states considered for the experiment included relaxed, concentrating, neutral. For the relaxed state, subjects listened to meditation low-tempo music and were asked to relax their muscles. For the neutral state, a similar test was carried out, but with no music. This test was done before the rest to prevent lasting effects of relaxation and concentration. Finally, for the concentration state, the subjects played a game in which they had to find a ball that was hidden under one of three rotating cups. To learn more about the experiment, you can check out the [original study](https://www.researchgate.net/publication/328615252_A_Study_on_Mental_State_Classification_using_EEG-based_Brain-Machine_Interface).


![alt text]

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

![alt text] (https://github.com/Atlaskz/Mental-State-Predictor/blob/main/chart.png)


## Wrapping up

I had a blast working on this problem as my first real data science project. If I decided to improve the accuracy, I would spend more time on signal processing to reduce the noise in the data. I would also try other deep learning algorithms and compare more models. I have a slight bias towards using deep learning for this problem due to its end to end optimization and the elimination of the feature engineering step. This is important since having to feature engineer the incoming data could increase prediction delay in real time. 

Speaking of real time, I thought it would be very interesting to test the performance of the model for actual prediction. Hence, for my next project, I am hoping to use a muse EEG headset or a similar product for predicting sentiment from brain activity in real time.

