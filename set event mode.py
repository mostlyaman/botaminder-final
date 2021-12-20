import time
lt=(time.localtime(time.time())[2:5])
mode=input('enter user mode:')
no=0
s_name=[]
s_st=[]
s_et=[]
if mode=='manual':
    no=int(input('enter the number of events'))
    for i in range(no):
        q='enter the title of event '+str(i+1)+':'
        name=input(q)
        st=int(input('enter start time hour:'))
        et=int(input('enter end time hour:'))
        s_name.append(name)
        s_st.append(st)
        s_et.append(et)
n='"'+s_name[0]+'"'
st1='(long)'+str(s_st[0])+'*3600'
et1='(long)'+str(s_et[0])+'*3600'
for i in s_name[1:]:
    n+=','+'"'+i+'"'
for i in s_st[1:]:
    st1+=','+'(long)'+str(i)+'*3600'
for i in s_et[1:]:
    et1+=','+'(long)'+str(i)+'*3600'
    
    
print('long time[3] = {'+str(lt[0])+','+str(lt[1])+','+str(lt[2])+'};')
print('int events = ',no,';')
print('String eventName[',no,'] = {',n,'};')
print('long eventStartTime[2] = {',st1,'};')
print('long eventEndTime[2] = {',et1,'};')
print('int eventScrollingSpeed = 4;'+'\n'+\
      'long waterReminder = 3*3600;'+'\n'+\
      'long breakReminder = 4*3600;'+'\n'+\
      'long skippingBreak = 17*3600;')
print('String userMode = "'+mode+'";')
       
        
        
        