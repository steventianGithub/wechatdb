from wechatdb import app, db
from wechatdb.models import tbl_admission, tbl_rank, tbl_admission_liberalart, tbl_rank_liberalart
from flask import url_for, render_template
from flask import request, redirect, flash, session
from sqlalchemy import and_
from sqlalchemy.ext.declarative import DeclarativeMeta  
import json
import decimal, datetime

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)     # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:    # 添加了对datetime的处理
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.date):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.timedelta):
                        fields[field] = (datetime.datetime.min + data).time().isoformat()
                    else:
                        fields[field] = None
            # a json-encodable dict
            return fields
 
        return json.JSONEncoder.default(self, obj)

# 按学校查询录取结果， 返回值先按年份排序再按分数排序
def query_by_school(table, schoolname):
    return table.query.filter(table.school_name.
                like("%" + schoolname + "%")).order_by(
                    table.admission_year.desc()).order_by(
                        table.admission_score.desc())

# 按分数查询录取结果， 返回值先按年份排序再按分数排序
def query_by_score(table, maxscore, minscore):
    return table.query.filter(
                table.admission_score <= maxscore, 
                table.admission_score >= minscore).order_by(
                    table.admission_year.desc()).order_by(
                        table.admission_score.desc())

# 按分数查询一分一段表
def query_rank_by_score(table, score):
    return table.query.filter(
                table.score == score).order_by(
                    table.year.desc())

# 查询所一分一段表所有记录
def query_rank(table):
    return table.query.order_by(
                table.year.desc())

#文理科通用查询成绩路由函数
def base_query_admission(table, science):
    if science == 0:
        schoolname = session.get('science_schoolname')
        maxscore = session.get('science_maxscore')
        minscore = session.get('science_minscore')
        year = session.get('science_year')
    else:
        schoolname = session.get('liberalarts_schoolname')
        maxscore = session.get('liberalarts_maxscore')
        minscore = session.get('liberalarts_minscore')
        year = session.get('liberalarts_year')        

    if year == "*":
        # 查询所有年份
        if schoolname != "*":
            # 在所有年份中，按学校查询
            flash("按学校：{}，最高分：{}，最低分：{}，查询{}年录取情况".format(
                schoolname, maxscore, minscore, year))
            tables = query_by_school(table, schoolname)
            return tables   
        else:
            # 在所有年份中，按分数查询
            if maxscore < minscore:
                # 提示最高分必须大于最低分
                flash("最高分必须大于最低分")
                return None
            else:
                flash("按学校：{}，最高分：{}，最低分：{}，查询{}年录取情况".format(
                    schoolname, maxscore, minscore, year))
                tables = query_by_score(table, maxscore, minscore)
                return tables
    else:
        # 查询指定年份
        if schoolname != "*":
            # 按指定年份，按学校查询
            flash("按学校：{}，最高分：{}，最低分：{}，查询{}年录取情况".format(
                schoolname, maxscore, minscore, year))
            tables = query_by_school(table, schoolname).filter(
                table.admission_year == year)
            return tables
        else:
            # 按指定年份，按分数查询
            if maxscore < minscore:
                # 提示最高分必须大于最低分
                flash("最高分必须大于最低分")
                return None
            else:
                flash("按学校：{}，最高分：{}，最低分：{}，查询{}年录取情况".format(
                    schoolname, maxscore, minscore, year))
                tables = query_by_score(table, maxscore, minscore).filter( 
                    table.admission_year==year)
                return tables          



# 文理科通用查询一分一段表
def base_query_rank(table, science):
    if science == 0:
        score = session.get('science_score')
        year = session.get('science_year')
    else:
        score = session.get('liberalarts_score')
        year = session.get('liberalarts_year')

    if year == "*":
        # 查询所有年份的一分一段表
        if score != "*":
            # 在所有年份中，查询指定分数的人数
            flash("按分数：{}分查询一分一段表".format(score))
            tables = query_rank_by_score(table, score)
            return tables
        else:
            # 在所有年份中，查询所有一分一段表
            flash("查询全部一分一段表")
            tables = query_rank(table)
            return tables
    else:
        # 查询指定年份的一分一段表
        if score != "*":
            # 在指定年份中，查询指定分数的人数
            flash("按分数：{}，查询{}年一分一段表".format(score, year))
            tables = query_rank_by_score(table, score).filter(
                table.year == year).order_by(
                    table.year.desc())
            return tables
        else:
            # 在指定年份中，查询所有一分一段表
            flash("查询{}年一分一段表".format(year))
            tables = query_rank(table).filter(
                table.year == year).order_by(
                    table.year.desc())
            return tables     

@app.before_request
def check_source():

    """进行验证是否来自微信服务器"""
    """
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    # echostr = request.args.get('echostr')
    tmp = [WECHAT_TOKEN, timestamp, nonce]
    tmp.sort()
    tmp = "".join(tmp).encode('utf-8')
    tmp = hashlib.sha1(tmp).hexdigest()
    if tmp != signature:
        return 'error'
    """
    return

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# 查询理科成绩路由
@app.route('/science', methods=['GET', 'POST'])
def science():
    html_url = 'science.html'

    #初始化查询返回值变量为空，如果查询结果为空，则返回空值

    queryResult = []

    if request.method == 'POST': 
        session['science_schoolname'] = request.values.get("schoolname")
        session['science_maxscore'] = request.values.get("maxscore")
        session['science_minscore'] = request.values.get("minscore")
        session['science_year'] = request.values.get("year")

    if session.get('science_schoolname'):
        queryResult = base_query_admission(tbl_admission, 0).all()

    rts=[]

    for item in queryResult:
        temp=dict(schoolserial=item.school_serial, 
            schoolname=item.school_name,
            admissionscore=item.admission_score, 
            year=item.admission_year,
            #school_related_batch是外链
            batch=item.school_related_batch.batch_name)
        rts.append(temp)

    #rts = json.dumps(queryResult, cls=AlchemyEncoder,ensure_ascii=False)
    return json.dumps(rts,ensure_ascii=False) 

# 查询理科一分一段表路由
@app.route('/sciencerank', methods=['GET', 'POST'])
def sciencerank():
    html_url = 'sciencerank.html'
    page=request.args.get('page',1,type=int)

    if request.method == 'POST': 
        session['science_score'] = request.form.get('score')
        session['science_year'] = request.form.get('year')

    if session.get('science_score'):
        pagination = base_query_rank(tbl_rank, 0).paginate(
            page,per_page=app.config['ITEMS_PER_PAGE'] ,error_out=False)
            
        if pagination:
            return render_template(html_url, pagination=pagination)
        else:
            return render_template(html_url)

    return render_template(html_url)

# 查询文科成绩路由
@app.route('/liberalarts', methods=['GET', 'POST'])
def liberalarts():
    html_url = 'liberalarts.html'
    page=request.args.get('page',1,type=int)

    if request.method == 'POST': 
        session['liberalarts_schoolname'] = request.form.get('schoolname')
        session['liberalarts_maxscore'] = request.form.get('maxscore')
        session['liberalarts_minscore'] = request.form.get('minscore')
        session['liberalarts_year'] = request.form.get('year')

    if session.get('liberalarts_schoolname'):
        pagination = base_query_admission(tbl_admission_liberalart, 1).paginate(
            page,per_page=app.config['ITEMS_PER_PAGE'] ,error_out=False)
        if pagination:
            return render_template(html_url, pagination=pagination)
        else:
            return render_template(html_url)

    return render_template(html_url)
    
# 查询文科一分一段表路由
@app.route('/liberalartsrank', methods=['GET', 'POST'])
def liberalartsrank():
    html_url = 'liberalartsrank.html'
    page=request.args.get('page',1,type=int)

    if request.method == 'POST': 
        session['liberalarts_score'] = request.form.get('score')
        session['liberalarts_year'] = request.form.get('year')

    if session.get('liberalarts_score'):
        pagination = base_query_rank(tbl_rank_liberalart, 1).paginate(
            page,per_page=app.config['ITEMS_PER_PAGE'] ,error_out=False)
        if pagination:
            return render_template(html_url, pagination=pagination)
        else:
            return render_template(html_url)

    return render_template(html_url )