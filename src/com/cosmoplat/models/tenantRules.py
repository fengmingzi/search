from app import db


class TenantRules(db.Model):
    __tablename__ = 'sc_tenant_crawling_rules'
    id = db.Column(db.BigInteger, primary_key=True)
    tenant_id = db.Column(db.BigInteger)  # 租户id
    tenant_uni_code = db.Column(db.String(100))  # 租户唯一标识
    task_name = db.Column(db.String(100))   # 任务名称
    dictionary_data_annotation = db.Column(db.String(100))  # 数据标注
    index_name = db.Column(db.String(100))  # 索引名称 租户id_归类名称的md5值小写
    target_domain = db.Column(db.String(100))   # 目标域名
    list_url = db.Column(db.String(100))    # 入口url
    detail_page_url_xpath = db.Column(db.String(100))   # 详情页url的xpath
    dictionary_next_page_type = db.Column(db.String(100))  # 下一页爬取的规则类型 1-带href 2-不带页码的点击翻页 3-带页码的点击翻页
    next_page_xpath = db.Column(db.String(100))  # 下一页的爬取规则json(next_page_type 1:href，2：selector，3：selector  totalPage attribute)
    detail_title_xpath = db.Column(db.String(100))  # 详情页标题爬取规则
    detail_content_xpath = db.Column(db.String(100))  # 详情页内容爬取规则
    is_deleted = db.Column(db.Boolean)  # 删除标识 0--未删除  1--删除
    create_time = db.Column(db.DateTime)  # 创建时间
    update_time = db.Column(db.DateTime)    # 更新时间

    def __repr__(self):
        return '<TenantRules {}>'.format(self.tenant_uni_code)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
