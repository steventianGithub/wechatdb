from wechatdb import app, db

# 2018年各高校高考录取分数表 - 理科
class tbl_admission(db.Model):
    # 
    __tablename__ = 'tbl_admission'
    id = db.Column(db.Integer, primary_key=True)    #主键
    school_serial = db.Column(db.String(4))         # 学校编码
    school_name = db.Column(db.String(20))          # 学校名称
    admission_year = db.Column(db.Integer)
    admission_score = db.Column(db.Integer)
    batch_id = db.Column(db.Integer, db.ForeignKey(
        'tbl_batch.batch_id'))                 # 录取批次


#2018年一分一段表 - 理科
class tbl_rank(db.Model):
    # 
    __tablename__ = 'tbl_rank'
    rank_id = db.Column(db.Integer, primary_key=True)    #主键
    score = db.Column(db.Integer)                        # 高考分数
    student_within = db.Column(db.Integer)               # 该分数有多少学生
    student_sum = db.Column(db.Integer)                  # 从最高分到该分数所有学生总数
    year = db.Column(db.Integer)
    
#2018年录取批次表 - 理科
class tbl_batch(db.Model):
    # 
    __tablename__ = 'tbl_batch'
    batch_id = db.Column(db.Integer, primary_key=True)  #主键
    batch_name = db.Column(db.String(20))               # 录取批次
    year = db.Column(db.Integer)

    batch_related_school = db.relationship('tbl_admission', 
        backref = 'school_related_batch')               # 添加一对多的反向引用

# 2018年各高校高考录取分数表 - 文科
class tbl_admission_liberalart(db.Model):
    # 
    __tablename__ = 'tbl_admission_liberalart'
    id = db.Column(db.Integer, primary_key=True)    #主键
    school_serial = db.Column(db.String(4))         # 学校编码
    school_name = db.Column(db.String(20))          # 学校名称
    admission_year = db.Column(db.Integer)
    admission_score = db.Column(db.Integer)
    batch_id = db.Column(db.Integer, db.ForeignKey(
        'tbl_batch_liberalart.batch_id'))            # 录取批次


#2018年一分一段表 - 文科
class tbl_rank_liberalart(db.Model):
    # 
    __tablename__ = 'tbl_rank_liberalart'
    rank_id = db.Column(db.Integer, primary_key=True)    #主键
    score = db.Column(db.Integer)                        # 高考分数
    student_within = db.Column(db.Integer)               # 该分数有多少学生
    student_sum = db.Column(db.Integer)                  # 从最高分到该分数所有学生总数
    year = db.Column(db.Integer)
    
#2018年录取批次表 - 文科
class tbl_batch_liberalart(db.Model):
    # 
    __tablename__ = 'tbl_batch_liberalart'
    batch_id = db.Column(db.Integer, primary_key=True)  #主键
    batch_name = db.Column(db.String(20))               # 录取批次
    year = db.Column(db.Integer)

    batch_related_school = db.relationship('tbl_admission_liberalart', 
        backref = 'school_related_batch')               # 添加一对多的反向引用