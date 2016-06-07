import operator
import numpy as np 
import pandas as pd
import os
# os.chdir("..")
import environment
from crowdclass.models import UserSession
from crowdclass.models import PrePostTest

#Helper Functions for Group B Analysis
def clear_users():
    '''
    Clearing user data  (only for testing purposes)
    '''
    for user in UserSession.objects.all():
        user.delete()

def create_dictUser():
    '''
    Group all the UserSessions per user 
    together in a dictionary 
    '''
    dictUser_data = {}
    for user in UserSession.objects.all():
        #user.user is the unique identifier for the user 
        #user.id is the id for each of the question per user
        if (user.user.id in dictUser_data):
            dictUser_data[user.user.id].append(user)
        else:
            dictUser_data[user.user.id]=[user]
    return dictUser_data
def convert_count(x):
    if x==None:
        return 0
    else:
        return x
def convert_count2(x):
    if x==False:
        return 0
    elif x==True:
        return 1
def create_PrePost():
    '''
    Group all the PrePostObject per user 
    together in a dictionary 
    '''
    dictPrePost_data = {}
    for test in  PrePostTest.objects.all():
        ID = int(test.user.username)
        dictPrePost_data[ID]=test
    return dictPrePost_data
def accuracy(N_correct,N_wrong):
    '''
    returns accuracy based on correct/wrong counts
    
    Some users never get to some questions so they might not have 
    N_correct and N_wrong counts. But this is different from accuracy=0
    So we put a flag of -1 if user accuracy N/A
    '''
    if N_correct+N_wrong ==0:
        return -1
    else:
        return N_correct/ float(N_correct+N_wrong)

def dt(t_final,t_initial):
    if t_final ==None or t_initial ==None:
        return -1
    else:
        return (t_final-t_initial).seconds
def count_prepost(test,P=""):
    '''
    Input a PrePostTest object
    return the [number of -1,1,?]
    ? : "I don't know"
    -1 : wrong answer
    1: correct answer
    '''
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
        print "WARNING: Incomplete record of User", test.user.username
        print "Only ",total," questions answered"
    return [wrong,correct,uncertain]    

def dt_prepost(test,P=""):
    '''
    Return time spent on pre/post test
    '''
    keys = ['scheme','elliptical','merger','tidal','lens','dust','properties','bulges','not','formation']
    if P=="pre":
        t_list = [test.pre_scheme_time, test.pre_elliptical_time,test.pre_mergers_time,test.pre_tidal_time,test.pre_lens_time,
                 test.pre_dust_time,test.pre_properties_time,test.pre_bulges_time,test.pre_not_time,test.pre_formation_time, 
                 dictUser_data[test.user_id][0].elliptical_time]
    elif P == "post":
        #dictUser_data[int(test.user.username)][-1].end_time
        end_time = test.end_time
        if end_time ==None:
            print "WARNING:  No recorded endtime"
            t_list = [test.post_scheme_time, test.post_elliptical_time,test.post_mergers_time,test.post_tidal_time,test.post_lens_time,
                 test.post_dust_time,test.post_properties_time,test.post_bulges_time,test.post_not_time,test.post_formation_time]
        else:
            t_list = [test.post_scheme_time, test.post_elliptical_time,test.post_mergers_time,test.post_tidal_time,test.post_lens_time,
                 test.post_dust_time,test.post_properties_time,test.post_bulges_time,test.post_not_time,test.post_formation_time, 
                 end_time]
    dic= dict(zip(keys,t_list))
    #rearrange in sorted order so that we can compute dt from consecutive items
    sorted_dic = sorted(dic.items(), key=operator.itemgetter(1))
    ordered_names = [x[0] for x in sorted_dic]
    t_list = sorted(t_list)
    dt_list = []
    for i in (t_list-np.roll(t_list,1))[1:]:
        dt_list.append(i.total_seconds())
    #rearranging the list so that it follows the order we want in the DataFrame 
    dic_dt= dict(zip(ordered_names,dt_list))
    dt = []
    for i in keys:
        try:
            dt.append(dic_dt[i])
        except KeyError:
            print "Missing ",i 
            dt.append(-1) #stuffer value, remove these in analysis (Shouldn't happen though..)
    return dt_list
def compute_all_accuracy(gz_subset, options_list , user):
    '''
    Compute accuracy of all the questions answered by a user
    to the classification result gz_subset which can either be
    the majority vote from GZ2 or classification by an expert
    options_list connects the options used in the gz_subset table with the options variables
    ex) gz_bar_option = 't03_bar_a06_bar_weighted_fraction'
    can be either a list or a string
    '''
    gz_bar_options , gz_bulge_options, gz_dust_options,gz_edge_options, \
    gz_elliptical_options, gz_lens_options, gz_merging_options, gz_spiral_options, gz_tidal_options= options_list

    bar_right =0 
    bar_wrong = 0
    bulge_right =0 
    bulge_wrong = 0    
    dust_right =0 
    dust_wrong = 0
    edge_right =0 
    edge_wrong = 0
    elliptical_right =0 
    elliptical_wrong = 0    
    lens_right =0 
    lens_wrong = 0
    merging_right =0 
    merging_wrong = 0
    spiral_right =0 
    spiral_wrong = 0
    tidal_right =0 
    tidal_wrong = 0
    
    for session in user:
        if session.image==0 or session.image==99:
        #this  shouldn't happen, bug remanant from pilot
            continue
        else:
            idx  =np.where(gz_subset['img_name']==str(session.image))[0][0]
                # bar
        gz_ans = convert_prob_to_ans(np.sum(gz_subset[gz_bar_options].iloc[idx]))
        if session.bar_correct== 0:
            #didn't answer this question 
            pass
        # session.*_correct =1 means that the user thinks that the object IS in that class
        # gz_ans =1  means the GZ majority result thinks that object IS in that class
        elif session.bar_correct== gz_ans:
            bar_right +=1
        elif session.bar_correct!= gz_ans:
            bar_wrong +=1
        # bulge
        gz_ans = convert_prob_to_ans(np.sum(gz_subset[gz_bulge_options].iloc[idx]))
        if session.bulge_correct== 0:
            pass
        elif session.bulge_correct== gz_ans:
            bulge_right +=1
        elif session.bulge_correct!= gz_ans:
            bulge_wrong +=1
        # dust
        gz_ans = convert_prob_to_ans(np.sum(gz_subset[gz_dust_options].iloc[idx]))
        if session.dust_correct== 0:
            pass
        elif session.dust_correct== gz_ans:
            dust_right +=1
        elif session.dust_correct!= gz_ans:
            dust_wrong +=1

        # edge
        gz_ans = convert_prob_to_ans(np.sum(gz_subset[gz_edge_options].iloc[idx]))
        if session.edge_correct== 0:
            pass
        elif session.edge_correct== gz_ans:
            edge_right +=1
        elif session.edge_correct!= gz_ans:
            edge_wrong +=1
        # Ellipticals
        gz_ans = convert_prob_to_ans(np.sum(gz_subset[gz_elliptical_options].iloc[idx]))
        if session.elliptical_correct== 0:
            pass
        elif session.elliptical_correct== gz_ans:
            elliptical_right +=1
        elif session.elliptical_correct!= gz_ans:
            elliptical_wrong +=1
        # lens
        gz_ans = convert_prob_to_ans(np.sum(gz_subset[gz_lens_options].iloc[idx]))
        if session.lens_correct== 0:
            pass
        elif session.lens_correct== gz_ans:
            lens_right +=1
        elif session.lens_correct!= gz_ans:
            lens_wrong +=1

        # merging
        gz_ans = convert_prob_to_ans(np.sum(gz_subset[gz_merging_options].iloc[idx]))
        if session.merging_correct== 0:
            pass
        elif session.merging_correct== gz_ans:
            merging_right +=1
        elif session.merging_correct!= gz_ans:
            merging_wrong +=1            
        # spiral
        gz_ans = convert_prob_to_ans(np.sum(gz_subset[gz_spiral_options].iloc[idx]))
        if session.spiral_correct== 0:
            pass
        elif session.spiral_correct== gz_ans:
            spiral_right +=1
        elif session.spiral_correct!= gz_ans:
            spiral_wrong +=1

        # tidal
        gz_ans = convert_prob_to_ans(np.sum(gz_subset[gz_tidal_options].iloc[idx]))
        if session.tidal_correct== 0:
            pass
        elif session.tidal_correct== gz_ans:
            tidal_right +=1
        elif session.tidal_correct!= gz_ans:
            tidal_wrong +=1
    
            
    return [bar_right, bar_wrong, accuracy(bar_right,bar_wrong),\
           bulge_right, bulge_wrong, accuracy(bulge_right,bulge_wrong),\
           dust_right, dust_wrong, accuracy(dust_right,dust_wrong),\
           edge_right, edge_wrong, accuracy(edge_right,edge_wrong),\
           elliptical_right, elliptical_wrong, accuracy(elliptical_right,elliptical_wrong),\
           lens_right, lens_wrong, accuracy(lens_right,lens_wrong),\
           merging_right, merging_wrong, accuracy(merging_right,merging_wrong),\
           spiral_right, spiral_wrong, accuracy(spiral_right,spiral_wrong),\
           tidal_right, tidal_wrong, accuracy(tidal_right,tidal_wrong)]

def compute_all_dt(user):
    dt_elliptical=[]
    dt_edge = []
    dt_bar=[]
    dt_spiral=[]
    dt_bulge = []
    dt_tidal = []
    dt_merging = []
    dt_dust = []
    dt_lens=[]
    
    # Content
    dt_elliptical_content=[]
    dt_edge_content = []
    dt_bar_content = []
    dt_spiral_content=[]
    dt_bulge_content = []
    dt_tidal_content = []
    dt_merging_content = []
    dt_dust_content = []
    dt_lens_content = []

    scores=[]
    num_image_classified = 0 
    for session in user:
    #     print "Img: ", session.image
        num_image_classified+=1
        scores.append(session.score)
        if session.difficulty==0:
            #Ellipticals
            if session.elliptical_correct==-1:
    #             print "Continue Tree"
#                 print session.edge_description_time
                if session.elliptical_description_time!=None:
                    dt_elliptical_content.append(dt(session.elliptical_time,session.elliptical_description_time))
                if session.edge_description_time == None:
    #                 print "no edge description"
                    dt_elliptical.append(dt(session.edge_time,session.elliptical_time))
                else:
                    dt_elliptical.append(dt(session.edge_description_time,session.elliptical_time))
                    dt_edge_content.append(dt(session.edge_time,session.edge_description_time))
                #Edge
                if session.edge_correct==-1:
                    if session.bar_description_time == None:
                        dt_edge.append(dt(session.bar_time,session.edge_time))
                    else:
                        dt_edge.append(dt(session.bar_description_time,session.edge_time))
                        dt_bar_content.append(dt(session.bar_time,session.bar_description_time))
                else:
                    dt_edge.append(dt(session.end_time,session.edge_time))
                #Bar 
                if session.spiral_description_time == None:
                    dt_bar.append(dt(session.spiral_time,session.bar_time))
                else:
                    dt_bar.append(dt(session.spiral_description_time,session.bar_time))
                    dt_spiral_content.append(dt(session.spiral_time,session.spiral_description_time))
                #Spiral 
                dt_spiral.append(dt(session.end_time,session.spiral_time))
            else:
    #             print "End of tree"
    #             print "session end time: " , session.end_time            
                #session end_time is not being stored correctly currently, but this should soon be fixed 
                dt_elliptical.append(dt(session.end_time,session.elliptical_time))
        elif session.difficulty==1:
            #Elliptical
            if session.elliptical_correct == -1:
                if session.bulge_description_time == None:
                    dt_elliptical.append(dt(session.bulge_time,session.elliptical_time))
                else:
                    dt_elliptical.append(dt(session.bulge_description_time,session.elliptical_time))
                    dt_bulge_content.append(dt(session.bulge_time,session.bulge_description_time))
            else:
                #session end_time is not being stored correctly currently, but this should soon be fixed 
                dt_elliptical.append(dt(session.end_time,session.elliptical_time))
            #Bulge
            dt_bulge.append(dt(session.edge_time,session.bulge_time))
            if session.edge_correct==-1:
                dt_edge.append(dt(session.bar_time,session.edge_time))
            else:
                dt_edge.append(dt(session.end_time,session.edge_time))
            #Spiral
            if session.tidal_description_time == None:
                dt_spiral.append(dt(session.tidal_time,session.spiral_time))
            else:
                dt_spiral.append(dt(session.tidal_description_time,session.spiral_time))
                dt_tidal_content.append(dt(session.tidal_time,session.tidal_description_time))
            #Tidal 
            if session.merging_description_time == None:
                dt_tidal.append(dt(session.merging_time,session.tidal_time))
            else:
                dt_tidal.append(dt(session.merging_description_time,session.tidal_time))
                dt_merging_content.append(dt(session.merging_time,session.merging_description_time))
            #Merging
            dt_merging.append(dt(session.end_time,session.merging_time))
        elif session.difficulty==2:
            #Elliptical
            if session.elliptical_choice==-1:
                dt_elliptical.append(dt(session.bulge_time,session.elliptical_time))
            else:
                if session.dust_description_time == None:
                    dt_elliptical.append(dt(session.dust_time,session.elliptical_time))
                else:
                    dt_elliptical.append(dt(session.dust_description_time,session.elliptical_time))
            #Bulge 
            dt_bulge.append(dt(session.edge_time,session.bulge_time))
            #Edge
            if session.edge_choice==-1:
                dt_edge.append(dt(session.bar_time,session.edge_time))
            else:
                if session.dust_description_time == None:
                    dt_edge.append(dt(session.dust_time,session.edge_time))
                else:
                    dt_edge.append(dt(session.dust_description_time,session.edge_time))
            #Bar, Spiral, Tidal
            dt_bar.append(dt(session.spiral_time,session.bar_time))
            dt_spiral.append(dt(session.tidal_time,session.spiral_time))
            dt_tidal.append(dt(session.merging_time,session.tidal_time))
            # Merging
            if session.dust_description_time == None:
                dt_merging.append(dt(session.dust_time,session.merging_time))
            else:
                dt_merging.append(dt(session.dust_description_time,session.merging_time))
                dt_dust_content.append(dt(session.dust_time,session.dust_description_time))
            if session.lens_description_time == None:
                dt_dust.append(dt(session.lens_time,session.dust_time))
            else:
                dt_dust.append(dt(session.lens_description_time,session.dust_time))
                dt_lens_content.append(dt(session.lens_time,session.lens_description_time))
            dt_lens.append(dt(session.end_time,session.lens_time))
    mega_dt_lst = [dt_bar,dt_bulge,dt_dust,dt_edge,dt_elliptical,dt_lens,dt_merging,dt_spiral,dt_tidal]
    for dt_lst in mega_dt_lst:
        nil = [dt_lst.remove(-1) for i in np.arange(dt_lst.count(-1))]
        if dt_lst ==[]:
            dt_lst.append(0)
    average_time = map(np.mean,mega_dt_lst)    

    print "sum: ",sum([_x for sublist in mega_dt_lst for _x in sublist])
    print "img_cla: ", num_image_classified
    try:
        speed  = float(num_image_classified)/sum([_x for sublist in mega_dt_lst for _x in sublist])
    except (ZeroDivisionError):
        speed = -1
    print "speed: ",speed

    mega_dt_content_lst = [dt_bar_content,dt_bulge_content,dt_dust_content,dt_edge_content,dt_elliptical_content,dt_lens_content,dt_merging_content,dt_spiral_content,dt_tidal_content]
    for dt_lst in mega_dt_content_lst:
        nil = [dt_lst.remove(-1) for i in np.arange(dt_lst.count(-1))]
        if dt_lst ==[]:
            dt_lst.append(0)
    average_content_time = map(np.mean,mega_dt_content_lst)    
#     print len(average_time)
#     print len(average_content_time)
    average_time.extend(average_content_time)
    return average_time,speed

dictUser_data = create_dictUser()

def convert_prob_to_ans(prob):
    '''
    correspond to the output from views.py
    1 if belong to that class
    -1 if don't belong to that class
    0 if unanswered
    '''
    if prob>=0.5:
        return 1
    else:
        return -1