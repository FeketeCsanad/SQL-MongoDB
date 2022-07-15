from tkinter import *
from tkinter import messagebox
import mysql.connector
from pymongo import MongoClient

root =Tk()
root.title("Tantargy felvetel")
root.geometry("800x400")
global e1
global e2
global e3
global e4
global e5
global e6

#SQL
Label(root, text="Tantargy").place(x=30,y=20)
Label(root, text="Tantargy id:").place(x=10,y=50)
Label(root, text="Tantargy Neve:").place(x=10,y=90)

#MongoDB
Label(root, text="Tanulo").place(x=315,y=20)
Label(root, text="Tanulo Neve:").place(x=300,y=50)
Label(root, text="Tanulo id:").place(x=300,y=90)
Label(root, text="Tantargy id:").place(x=300,y=130)


#SQL
e1=Entry(root)
e1.place(x=100,y=50)

e2=Entry(root)
e2.place(x=100,y=90)

#MongoDB
e3=Entry(root)
e3.place(x=390,y=50)

e4=Entry(root)
e4.place(x=390,y=90)

e5=Entry(root)
e5.place(x=390,y=140)

def Ok():

    mysqldb=mysql.connector.connect(host="localhost",user="root",password="",database="mydb")
    mycursor=mysqldb.cursor()
    client = MongoClient("localhost",port=27017)
    db = client.Osztaly
    col1 = db.Tanulo
    col2=db.Tantargy
    if len(e1.get()) != 0 and len(e2.get()) !=0  :
        tantargy_id=int(e1.get())
        tantargyNeve=e2.get()

        try:
            sql = "INSERT INTO tantargy(id,TantargyNev) VALUES (%s,%s)"
            val = (tantargy_id, tantargyNeve)
            mycursor.execute(sql, val)
            mysqldb.commit()
            tn = str(tantargyNeve)
            ti = str(tantargy_id)
            mydict = {
                    "_id": ti,
                    "Tantargy": tn
                }
            col2.insert_one(mydict)
            messagebox.showinfo("Sikerult")
        except EXCEPTION as e:
            print(e)
            MongoClient.rollback()
            MongoClient.close()
    else:
        tanuloNev=e3.get()
        tanulo_id=e4.get()
        tantargy_id=e5.get()

        try:
            sql="INSERT INTO tanulo(id,Nev,Tantargy_id) VALUES (%s,%s,%s)"
            val=(tanulo_id,tanuloNev,tantargy_id)
            mycursor.execute(sql,val)
            mysqldb.commit()
            TN = e3.get()
            TI = e4.get()
            TT = e5.get()
            tt = str(TT)
            tn = str(TN)
            ti = str(TI)

            col2.update_one({'_id': tt},
                {"$push":{"Tanulok":
                          {"$each": [tn]}}},
                )
            messagebox.showinfo("Sikerult")
        except EXCEPTION as e:
            print(e)
            MongoClient.rollback()
            MongoClient.close()

Button(root,text="Hozzaad",command=Ok,height=3,width=10,).place(x=250,y=170)
root.mainloop()
