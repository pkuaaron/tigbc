from os import listdir
import os
import shutil
import pandas as pd
def make_links():
    fp=open(r'more_links.txt')
    lines=fp.readlines()
    projs=[]
    task_list=[]
    videos=[]
    previous_proj=''

    prefix=['0'+str(i) if i<10 else str(i) for i in range(130)]
    i=0
    for s in lines:
        i=i+1
        l=s.split('/')
        proj=l[l.index('projects')+1]
        proj_name=proj.replace('-',' ').title()
        projs.append(proj_name)

        task=l[l.index('tasks')+1]
        video=task[task.index('?wvideo=')+len('?wvideo='):task.index('"><img')]

        task_name=task[:task.index('?wvideo=')]
        tl=[t for t in task_name.split('-') if not any(char.isdigit() for char in t)]
        task_name=' '.join(tl).title()
        task_list.append(prefix[i]+' '+task_name)
        videos.append(video)

    df=pd.DataFrame.from_dict({'Project':projs, 'Task':task_list,'Video':videos})
    df.to_csv(r'more_links.csv',index=False)

def rename_files():
    d=r'E:\Websites'
    files=listdir(d)
    df=pd.read_excel(r'E:\Websites\All_links.xlsx','Sheet1')
    for f in files:
        unique_id=f.split('-')[-1].split('.')[0]
        row=df[df['Video']==unique_id].to_dict(orient='records')
        if row:
            new_folder=os.path.join(d,row[0]['Folder'])
            if not os.path.exists(new_folder):
                os.mkdir(new_folder)
            shutil.move(os.path.join(d,f),os.path.join(new_folder,row[0]['Task']+'.mp4'))

    print(df)


if __name__=='__main__':
    rename_files()

