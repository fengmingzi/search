from app import db
from src.com.cosmoplat.models.models import User

'''进行数据库操作'''
if __name__ == '__main__':

    #role属性也可使用，虽然它不是真正的数据序列，但却是一对多关系的高级表示。给User表插入3条数据
    user_john = User(name='lucy')

    #在将对象写入数据库之前，先将其添加到会话中，数据库会话db.session和Flask session对象没有关系，数据库会话也称 事物 译作Database Transaction。
    db.session.add_all([user_john])
    #提交会话到数据库
    db.session.commit()

    #修改roles名
    # admin_role.name = 'Administrator'
    # db.session.add(admin_role)
    # db.session.commit()
    #
    # #删除数据库会话，从数据库中删除“Moderator”角色
    # db.session.delete(mod_role)
    # db.session.commit()#注意：删除 和插入、更新一样，都是在数据库会话提交后执行

    #查询
    print(User.query.filter_by(name='john'))