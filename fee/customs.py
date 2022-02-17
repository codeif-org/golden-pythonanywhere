from locale import currency
from fee.models import Month, FeeStructByMonth, FeeStruct, FeeSubmit, FeeSubmitByMonth
from school.models import Classes, School, Session, Current
import uuid

# test for customs
def monthIterate():
    month_qs = Month.objects.all()
    print(month_qs)
    

# create fee struct by month object (only for once)
def createFeeStructByMonth():
    month_qs = Month.objects.all()
    clas_qs = Classes.objects.all()
    school_obj = School.objects.all()[0]
    current = Current.objects.all()[0]
    for month_q in month_qs:
        for clas_q in clas_qs:
            fee_struct_by_month_obj = FeeStructByMonth(school=school_obj, month=month_q, clas=clas_q, session=current.session)
            fee_struct_by_month_obj.save()
            print("object created")

# complete update fee struct by month and class
def updateFeeStructByMonth():
    current = Current.objects.all()[0]
    fee_struct_by_month_qs = FeeStructByMonth.objects.filter(session=current.session)
    for fee_struct_by_month_q in fee_struct_by_month_qs:
        print(fee_struct_by_month_q)
        print(fee_struct_by_month_q.month.month, fee_struct_by_month_q.clas.clas)
        fee_struct_qs = FeeStruct.objects.filter(clas=fee_struct_by_month_q.clas, month=fee_struct_by_month_q.month, session=current.session)
        print(fee_struct_qs)
        month_amount = 0
        for fee_struct_q in fee_struct_qs:
             month_amount = month_amount + fee_struct_q.amount
        fee_struct_by_month_q.amount = month_amount
        fee_struct_by_month_q.save()
        print("updated")

        
# partially update fee struct for a month and class 
def partialUpdateFeeStructByMonth(month_id, class_id):
    current = Current.objects.all()[0]
    fee_struct_by_month_q = FeeStructByMonth.objects.get(month=month_id, clas=class_id, session=current.session)
    fee_struct_qs = FeeStruct.objects.filter(clas=class_id, month=month_id, session=current.session)             
    month_amount = 0
    for fee_struct_q in fee_struct_qs:
        month_amount = month_amount + fee_struct_q.amount
    fee_struct_by_month_q.amount = month_amount
    fee_struct_by_month_q.save()
    print("updated")
    
    
# Generate Transaction Number 
def txnNumber():
    txn_no = 'TXN' + str(uuid.uuid4().hex[:12].upper())
    # print(txn_no)
    return txn_no

# create fee struct
def createFee(class_no, fee_amount):
    month_qs = Month.objects.all()
    class_obj = Classes.objects.get(class_no=class_no)
    class_id = class_obj.id 
    current = Current.objects.all()[0]
    for month_q in month_qs:
        fee_struct = FeeStruct(clas=class_obj, month=month_q, fee_type="Tuition Fee", amount=fee_amount, session=current.session)
        fee_struct.save()
        month_id = month_q.id
        partialUpdateFeeStructByMonth(month_id, class_id)
        print("object created")   