#! python3
import pickle
import sys
import os

#GLOBAL VARIABLES
todo_list={}
home=os.environ['HOME']
GLOBAL_INDEX=0#number of tasks recieved up to date
#function definitions
def save_list():
    "Saves the list to the home direcotry as currently set in the $HOME variable"
    f=open(os.path.join(home,'.todo_list_pickle'),'wb')
    pickle.dump(todo_list,f)
    f.close()
def load_list():
    "Loads the list from home directory as in te $HOME variable"
    f=open(os.path.join(home,'.todo_list_pickle'),'rb')
    todo_list=pickle.load(f)
    f.close()
    GLOBAL_INDEX=len([i for i in todo_list if todo_list[i]['done']])
def add_task(string,deadline=None):
    "Adds task string to the todo list"
    todo_list[index]={'deadline':deadline,'done':False,'string':string}
    GLOBAL_INDEX+=1
def mark_done(index):
    "Marks the task with index as done"
    todo_list[index]['done']=True
def show_undone(limit=None):
    "Shows undone tasks limited by limit"
    undone=[todo_list[i] for i in todo_list.keys() if not todo_list[i]['done']]
    if limit!=None:show=undone[:limit]
    else:show=undone
    for task in undone:
        print(task['string'],task['deadline'])
def show(limit=None):
    "Shows last tasks limited by limit"
    tasks=[todo_list[i] for i in todo_list.keys().sort(reverse=True)]
    if limit!=None:show=tasks[:limit]
    else:show=tasks
def action_caller(args):
    "Calls the above functions and returns an exit code"
    #to be implemented
if __name__=='__main__':
    load_list()
    sys.exit(action_caller(sys.argv))
