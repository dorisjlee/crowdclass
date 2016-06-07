DEBUG = True
from collections import Counter
import numpy as np 
import fnmatch
import pandas as pd
import os
import operator
from helper import *
import environment
from crowdclass.models import UserSession
from crowdclass.models import PrePostTest
'''
This code takes the user data stored in db.sqlite3
and derive useful statistics for analysis.
'''

if DEBUG: print "Loading in data from GZ2"
data = pd.read_csv("scripts/analysis/gz_classification_result.csv")
gz_data = pd.read_csv("../../zoo2MainSpecz.csv")
gz_data_for_our_100_samples = gz_data.loc[gz_data["dr7objid"].isin(data["dr7objid"])] # JOIN two tables based on dr7objid key
gz_subset = gz_data_for_our_100_samples.merge(data,on="dr7objid") 
gz_subset["img_name"] = gz_subset["img_name"].apply(lambda x: x[:-4]) #strip all the .png to just ID numbers 
gz_options_list = ['t03_bar_a06_bar_weighted_fraction',
    ['t05_bulge_prominence_a11_just_noticeable_weighted_fraction', 
     't05_bulge_prominence_a12_obvious_weighted_fraction', 
     't05_bulge_prominence_a13_dominant_weighted_fraction'],
   't08_odd_feature_a38_dust_lane_weighted_fraction',
   't02_edgeon_a04_yes_weighted_fraction', 
   't01_smooth_or_features_a01_smooth_weighted_fraction', 
   't08_odd_feature_a20_lens_or_arc_weighted_fraction', 
   't08_odd_feature_a24_merger_weighted_fraction', 
   't04_spiral_a08_spiral_weighted_fraction', 
   't08_odd_feature_a21_disturbed_weighted_fraction' ]

if DEBUG: print "Loading in data by expert"
expert_data = pd.read_csv("scripts/analysis/crowdclass_expert_classification_result.csv")
expert_data_for_our_100_samples = gz_data.loc[gz_data["dr7objid"].isin(expert_data["dr7objid"])] # JOIN two tables based on dr7objid key
expert_subset =expert_data_for_our_100_samples.merge(expert_data,on="dr7objid") 
expert_subset["img_name"] = expert_subset["img_name"].apply(lambda x: x[:-4]) #strip all the .png to just ID numbers 
expert_options_list = ['bar','bulge','dust','edge','elliptical','lens','merging','spiral','tidal']

dictUser_data = create_dictUser()
dictPrePost_data = create_PrePost()

# Interested in only columns containing weighted_fractions info 
gz_headers = list(gz_data.columns)
filtered_headers = fnmatch.filter(gz_headers, '*_weighted_fraction') 

#mapping from session.*_choice outputs to gz_class names 
parent_options = ['smooth','features or disk',"star or artifact"]
edge_options = ['yes','no']
bar_options = ['bar','no bar']
pattern_options = ['spiral','no spiral']
prominence_options = ['no bulge','obvious','dominant']
bulge_options = ['rounded','boxy','no bulge']
round_options = ['completely round','in between','cigar shaped','other','overlapping']
# odd_options = ['ring','lens','disturbed','irregular','other','merger']
odd_options = ['none' , 'ring','lens or arc','irregular','other','dust lane']
sa_options = ['tight' , 'medium loose','loose']
sa_num_options = ['1','2','3','4','more than 4']
#GZ choices for that question
gz_parent_options = fnmatch.filter(filtered_headers,'t01_smooth_or_features*') 
gz_edge_options = fnmatch.filter(filtered_headers,'t02_edgeon*') 
gz_bar_options = fnmatch.filter(filtered_headers,'t03_bar*') 
gz_pattern_options = fnmatch.filter(filtered_headers,'t04_spiral*') 
# Ignoring 't05_bulge_prominence_a11_just_noticeable_weighted_fraction' choice
gz_prominence_options = ['t05_bulge_prominence_a10_no_bulge_weighted_fraction',
                         't05_bulge_prominence_a12_obvious_weighted_fraction', 
                         't05_bulge_prominence_a13_dominant_weighted_fraction']
gz_round_options = fnmatch.filter(filtered_headers,'t07_rounded*') 
# Ignoring 't08_odd_feature_a21_disturbed_weighted_fraction','t08_odd_feature_a24_merger_weighted_fraction'
gz_odd_options = ['t06_odd_a15_no_weighted_fraction',
                 't08_odd_feature_a19_ring_weighted_fraction',
                 't08_odd_feature_a20_lens_or_arc_weighted_fraction',
                 't08_odd_feature_a22_irregular_weighted_fraction',
                 't08_odd_feature_a23_other_weighted_fraction',
                 't08_odd_feature_a38_dust_lane_weighted_fraction',
                ]
gz_bulge_options = fnmatch.filter(filtered_headers,'t09_bulge_shape*') 
gz_sa_options= fnmatch.filter(filtered_headers,'t10_arms_winding*') 
#Ignoring 't11_arms_number_a37_cant_tell_weighted_fraction'
gz_sa_num_options = ['t11_arms_number_a31_1_weighted_fraction',
                     't11_arms_number_a32_2_weighted_fraction',
                     't11_arms_number_a33_3_weighted_fraction',
                     't11_arms_number_a34_4_weighted_fraction' ]

#total number of unqiue users
N_users = len(UserSession.objects.values_list('user', flat=True).distinct())
# create dataframe
df = pd.DataFrame(index=np.arange(0, N_users),
                  columns=('ID','img_classified', 'restart_count','examples_count',

                            'hints_count', 'easy_count','med_count','hard_count',

                           'bar_right_gz', 'bar_wrong_gz', 'accuracy_bar_gz',
                           'bulge_right_gz', 'bulge_wrong_gz', 'accuracy_bulge_gz',
                           'dust_right_gz', 'dust_wrong_gz', 'accuracy_dust_gz',
                           'edge_right_gz', 'edge_wrong_gz', 'accuracy_edge_gz',
                           'elliptical_right_gz', 'elliptical_wrong_gz', 'accuracy_elliptical_gz',
                           'lens_right_gz', 'lens_wrong_gz', 'accuracy_lens_gz',
                           'merging_right_gz', 'merging_wrong_gz', 'accuracy_merging_gz',
                           'spiral_right_gz', 'spiral_wrong_gz', 'accuracy_spiral_gz',
                           'tidal_right_gz', 'tidal_wrong_gz', 'accuracy_tidal_gz',

                           'bar_right_expert', 'bar_wrong_expert', 'accuracy_bar_expert',
                           'bulge_right_expert', 'bulge_wrong_expert', 'accuracy_bulge_expert',
                           'dust_right_expert', 'dust_wrong_expert', 'accuracy_dust_expert',
                           'edge_right_expert', 'edge_wrong_expert', 'accuracy_edge_expert',
                           'elliptical_right_expert', 'elliptical_wrong_expert', 'accuracy_elliptical_expert',
                           'lens_right_expert', 'lens_wrong_expert', 'accuracy_lens_expert',
                           'merging_right_expert', 'merging_wrong_expert', 'accuracy_merging_expert',
                           'spiral_right_expert', 'spiral_wrong_expert', 'accuracy_spiral_expert',
                           'tidal_right_expert', 'tidal_wrong_expert', 'accuracy_tidal_expert',

                            'dt_bar','dt_bulge','dt_dust','dt_edge','dt_elliptical','dt_lens',
                            'dt_merging','dt_spiral','dt_tidal',

                            'content_dt_bar','content_dt_bulge','content_dt_dust','content_dt_edge','content_dt_elliptical',
                            'content_dt_lens','content_dt_merging','content_dt_spiral','content_dt_tidal',

                            'avrg_speed',
                            
                           'pre_wrong','pre_correct','pre_uncertain','post_wrong','post_correct','post_uncertain',
                           # 'dt_pre_scheme','dt_pre_elliptical','dt_pre_merger','dt_pre_tidal','dt_pre_lens',
                           # 'dt_pre_dust','dt_pre_properties','dt_pre_bulges','dt_pre_not','dt_pre_formation',

                           # 'dt_post_scheme','dt_post_elliptical','dt_post_merger','dt_post_tidal','dt_post_lens',
                           #  'dt_post_dust','dt_post_properties','dt_post_bulges','dt_post_not','dt_post_formation'

                ))

i=0
for ID,user in dictUser_data.iteritems():
    print "UserID: " , user[0].user.username
    if user[0].user.username =='admin':
        continue
    ID  = int(user[0].user.username)
    img_classified = 0
    restart_count = 0 
    examples_count =0 
    hints_count = 0
    max_level = 0
    parent_correct=parent_wrong = edge_correct = edge_wrong = bar_correct = bar_wrong = pattern_correct= pattern_wrong = 0
    prominence_correct = prominence_wrong = round_correct = round_wrong = bulge_correct = bulge_wrong =0
    odd_correct = odd_wrong = sa_correct = sa_wrong = sa_num_correct = sa_num_wrong =0 
    #############################
    ###    ACURRACY RATES    ####
    #############################        
    if DEBUG : print "Computing Classification Accuracy"
    counts_gz_accuracy = compute_all_accuracy(gz_subset,gz_options_list,user)
    counts_expert_accuracy = compute_all_accuracy(expert_subset,expert_options_list,user)
    #################################
    ### Time Elapsed (Question) #####
    #################################
    result = compute_all_dt(user)
    print "result: ", result
    average_time= result[0]
    speed  = result[1]
    print speed
    # How many questions of what difficulty did the user see
    ct = Counter([_i.difficulty for _i in user])
    easy_count = [ct.get(0) if ct.get(0)!=None else 0][0]
    med_count = [ct.get(1) if ct.get(1)!=None else 0][0]
    hard_count = [ct.get(2) if ct.get(2)!=None else 0][0]
    print "easy_count: ", easy_count
    print "med_count: ", med_count
    print "hard_count:", hard_count
    
    for session in user:

        ###############################
        ###  SUMMARY STATISTICS     ###
        ###############################

        img_classified+=1
        restart_count += session.restart_count
        examples_count  += sum(map(convert_count2,[session.bar_example,session.bulge_example,session.dust_example,session.edge_example,
                                             session.elliptical_example,session.lens_example,session.merging_example,
                                             session.spiral_example,session.tidal_example]))
        hints_count  += sum(map(convert_count2,[session.bar_hint,session.bulge_hint,session.dust_hint,session.edge_hint,
                                     session.elliptical_hint,session.lens_hint,session.merging_hint,
                                     session.spiral_hint,session.tidal_hint]))

    if DEBUG:
        print "Number for image classified:" ,img_classified
        print "Number for restarts:" ,restart_count
        print "Number of times Examples page is pressed", examples_count
        print "Number of times Hints page is pressed", hints_count

    # Putting all the user summary statistics into a DataFrame
    user_info = [ID, img_classified, restart_count,examples_count,hints_count,easy_count,med_count,hard_count]
    user_info.extend(counts_gz_accuracy)
    user_info.extend(counts_expert_accuracy)
    user_info.extend(average_time) #average time user spent on each question / content (dt_*)
    # user_info.append(np.mean(average_time)) #average time user spents on answering any question 
    user_info.append(speed)
    ##################
    ## PrePost test ##
    ##################
    dictPrePost_data = create_PrePost()
    test = dictPrePost_data[ID]
    # Accuracy
    pre_count = count_prepost(test,P="pre")
    post_count = count_prepost(test,P="post")
    user_info.extend(pre_count)
    user_info.extend(post_count)

    print len(user_info)
    # # Time 
    # if not (post_count[0] ==0 and post_count[1] ==0 and post_count[2]==0):
    #     user_info.extend(dt_prepost(test,P="pre"))
    # else: 
    #     user_info.extend(-np.ones(10))
    # if not (post_count[0] ==0 and post_count[1] ==0 and post_count[2]==0):
    #     user_info.extend(dt_prepost(test,P="post"))
    # else:
    #     user_info.extend(-np.ones(10))
    df.loc[i] = user_info
    i+=1

# print df
filename = "scripts/analysis/user_summary_statistics.csv"
print "Data Sucessfully saved to ",filename
df.to_csv(filename)
