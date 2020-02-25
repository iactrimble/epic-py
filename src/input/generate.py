import csv
with open('user_input.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(['User','First Name','Last Name','Site','Work Email','Home Email','Work Phone','Home Phone','Mobile Phone','Mobile Phone 2','Personal Mobile Phone','Personal Mobile Phone 2','SMS Phone','SMS Phone 2','Personal SMS Phone','Personal SMS Phone 2','Pager','Pager Provider','Fax','IVR','Department','Job Title'])
    for num in range(100000):
        csvwriter.writerow(['User '+str(num+1),'First Name ' +str(num+1),'Last Name ' +str(num+1),'Default Site','user_'+str(num+1)+'@xmatters.com','','','','+12158502870','','','','+12158502870','','','','','','','','Department ' + str(num+1),'Job Title ' + str(num+1)])
