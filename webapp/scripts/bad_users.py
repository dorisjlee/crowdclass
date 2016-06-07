import operator
import numpy as np 
import pandas as pd
import os
import environment
from crowdclass.models import UserSession,PrePostTest
os.chdir("scripts")
from helper import *

dictUser_data = create_dictUser()
dictPrePost_data = create_PrePost()

IMG_COUNT_THRES_MAX = 90
IMG_COUNT_THRES_MIN = 5
SPIRAL_ACC_THRES = 0
ELLIPTICAL_ACC_THRES = 0

import sys
rerun = sys.argv[1]
if rerun=="rerun":
    print "Rerunning analysis script on updated DB: "
    os.system("python analysis.py")
user_study_data = pd.read_csv("analysis/user_summary_statistics.csv")

def check_prepost(test,P=""):
    bad_flag=False
    if P=="pre":
        ans = [test.pre_scheme,test.pre_elliptical ,test.pre_mergers ,test.pre_tidal, test.pre_lens,
             test.pre_dust,test.pre_properties,test.pre_bulges,test.pre_not,test.pre_formation
          ]
    elif P == "post":
        ans = [test.post_scheme,test.post_elliptical ,test.post_mergers ,test.post_tidal, test.post_lens,
             test.post_dust,test.post_properties,test.post_bulges,test.post_not,test.post_formation]
    uncertain = ans.count('?')
    wrong = ans.count('-1')
    correct  =ans.count('1')
    total = wrong+correct+uncertain
    if total !=10: 
        bad_flag = True
        print "BAD: Missing ",P,"-test questions"
    return bad_flag

print "--------------------------------------------------------------------------"
print "LIST OF BAD USERS"
good_user_lst = []
for i in np.arange(len(user_study_data)):
    bad_flag = False
    if user_study_data['img_classified'][i] >IMG_COUNT_THRES_MAX:
        bad_flag = True
        print "Too many image classified: ",user_study_data['img_classified'][i]
    if user_study_data['img_classified'][i] <IMG_COUNT_THRES_MIN:
        bad_flag = True
        print "Too little image classified: ",user_study_data['img_classified'][i]
    # if user_study_data['accuracy_elliptical_gz'][i]<ELLIPTICAL_ACC_THRES:
    #     bad_flag = True
    #     print "Elliptical Accuracy too low: ",user_study_data['accuracy_elliptical_gz'][i]
    # if user_study_data['accuracy_spiral_gz'][i]<SPIRAL_ACC_THRES:
    #     bad_flag = True
    #     print "Spiral Accuracy too low: ",user_study_data['accuracy_spiral_gz'][i]
    num_post_test = user_study_data['post_wrong'][i]+user_study_data['post_correct'][i]+user_study_data['post_uncertain'][i]
    if num_post_test!=10:
        bad_flag=True
        print "Didn't finish post-test, only ", num_post_test ,"done"

    if bad_flag : 
        print "BAD UserID: " ,int(user_study_data.ID[i])
        print "------------------------------"
    else:
        try:
            good_user_lst.append(int(user_study_data.ID[i]))
        except:
            pass
print "List of Good users: ", good_user_lst
print len(good_user_lst)
