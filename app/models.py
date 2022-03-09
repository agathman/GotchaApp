from . import db




db.session


#Object Modeling for tables
#Object Modeling for tables



class Test_Table(db.Model):
    __tablename__ = 'Test_Table'
    Test_Data = db.Column(db.Integer, primary_key=True, autoincrement= True)
    Test_Data2 = db.Column(db.String)

    def __repr__(self, Test_Data, Test_Data2):
            self.Test_Data = Test_Data 
            self.Test_Data2 = Test_Data2
            