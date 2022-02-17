from school.models import *
from fee.models import *
import pandas as pd 
import datetime

# custom functions for school
def addStudentData():
    wb = pd.read_excel('golden_data/golden_data_8.xlsx')
    # print(type(wb))
    # print(wb.iloc[:,1])
    # item[1][item_index]
    current = Current.objects.all()[0]
    for item in wb.iterrows():
        print(item[1][3])
        print(item[1][1])
        # dob
        try:
            dob_str = str(item[1][1])
            dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d %H:%M:%S').date()
            print(1, dob)
        except:
            dob_str = str(item[1][1])
            dob = datetime.datetime.strptime(dob_str, '%d-%m-%Y').date()  
            print(2, dob)
        phone = str(item[1][5]).split('.')[0]
        # print("phone", phone)    
        class_obj = Classes.objects.get(id=item[1][2])
        student_obj = Student(add_no=item[1][0], dob=dob, fname=item[1][3], fathername=item[1][4], phone=phone, gender=item[1][6], religion=item[1][7], category=item[1][8], session=current.session, Class=class_obj) 
        student_obj.save()
        print(student_obj)

        # feesubmitbymonth save
        fee_submit_by_month_obj = FeeSubmitByMonth(student=student_obj, session=current.session)
        fee_submit_by_month_obj.save() 
     
if __name__ == '__main__':
    addStudentData()     