import pandas as pd
import csv
import random
import copy
import os

# path to the CSV files with participant data
participants_csv = "CC Participants.csv"

# header names in the CSV file (name and e-mail of participants)
header_name = "Name"
header_email = "E-mail"

# path to TXT file that stores the groups of this round
new_groups_txt = "Coffee Chats New Groups.txt"

# path to CSV file that stores the groups of this round
new_groups_csv = "Coffee Chats New Groups.csv"

# path to CSV file that stores all groups (to avoid repetition)
all_groups_csv = "Coffee Chats All Groups.csv"

# path to CSV file that stores the conversation starters
convo_start_csv = "Conversation Starters.csv"

#path to txt file that stores individual messages
new_convo_starter_txt = "New Convo Starter.txt"
        
# init set of old groups
ogroups = set()

DELIMITER=','

# load all previous groups (to avoid redundancies)
if os.path.exists(all_groups_csv):
    try: 
        with open(all_groups_csv, "r") as file:
            csvreader = csv.reader(file, delimiter=DELIMITER)
            for row in csvreader:
                group = []
                for i in range(0,len(row)):
                    group.append(row[i])                        
                ogroups.add(tuple(group))
    except FileNotFoundError:
        print("File not found.")

# load participant's data
formdata = pd.read_csv(participants_csv, sep=DELIMITER)

#load conversation starter data
convodata= pd.read_csv(convo_start_csv, sep=DELIMITER)

# create duplicate-free list of participants
participants = list(set(formdata[header_email]))

 # init set of new groups
ngroups = set()

# running set of participants
nparticipants = copy.deepcopy(participants)

# Boolean flag to check if new grouping has been found
new_groups_found = False

# try creating new grouping until successful
while not new_groups_found:   # to do: add a maximum number of tries
  
    # while still participants left to group...
    while len(nparticipants) > 0:
  
        group_size = random.randint(2, len(nparticipants))
        
        # if the randomly chosen group size leaves one spare participant, the group size randomizer is re-run.
        if group_size == len(nparticipants)-1:
            continue
        
        # randomly choose the participants that are able to join the group
        else:
            plist = []
            for i in range(0, group_size):
                p = random.choice(nparticipants)
                plist += p
                nparticipants.remove(p)
            plist.sort()
            
            # add alphabetically sorted list to set of groups
            ngroups.add(tuple(plist))

 
    # check if all new groups are indeed new, else reset
    if ngroups.isdisjoint(ogroups):
        new_groups_found = True
    else:
        ngroups = set()
        nparticipants = copy.deepcopy(participants)


# assemble output for printout
output_string = ""

output_string += "------------------------\n"
output_string += "Today's coffee groups:\n"
output_string += "------------------------\n"

for pair in ngroups:
    pair = list(pair)
    output_string += "* "
    for i in range(0,len(pair)):
        name_email_pair = f"{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]} ({pair[i]})"
        convo_starter_pair = f"{random.choice(convodata[convodata['Conversation Starters']])}"
        if i < len(pair)-1:
            output_string += name_email_pair + ", "
        else:
            output_string += name_email_pair + "\n"
        
    
# write output to console
print(output_string)

# write output into text file for later use
try: 
    with open(new_groups_txt, "wb") as file:
        file.write(output_string.encode("utf8"))
except FileNotFoundError:
        print("File not found.")
    

# write new pairs into CSV file (for e.g. use in MailMerge)
try: 
    with open(new_groups_csv, "w") as file:
        header = ["name1", "email1", "name2", "email2", "name3", "email3"]
        file.write(DELIMITER.join(header) + "\n")
        for pair in ngroups:
            pair = list(pair)
            for i in range(0,len(pair)):
                name_email_pair = f"{formdata[formdata[header_email] == pair[i]].iloc[0][header_name]}{DELIMITER} {pair[i]}"
                if i < len(pair)-1:
                    file.write(name_email_pair + DELIMITER + " ")
                else:
                    file.write(name_email_pair + "\n")
except FileNotFoundError:
        print("File not found.")
    
#indiviudal message with groups and conversation starters  
try:               
    with open(new_convo_starter_txt, "w") as file:
        for pair in ngroups:
            for i in range(0, len(pair)):
                file.write(f"Hello {pair[i]}.iloc[0][header_name], {pair[i]}.iloc[0][header_name] You have been matched for a meeting! To start off, the conversation starter is {convo_starter_pair}. Have fun. ")
                    
except FileNotFoundError:
        print("File not found.")
    
# append pairs to history file
if os.path.exists(all_groups_csv):
    mode = "a"
else:
    mode = "w"
try: 
    with open(all_groups_csv, mode) as file:
        for pair in ngroups:
            pair = list(pair)
            for i in range(0,len(pair)):
                if i < len(pair)-1:
                    file.write(pair[i] + DELIMITER)
                else:
                    file.write(pair[i] + "\n")
except FileNotFoundError:
        print("File not found.")

          
# print finishing message
print()
print("Job done.")
