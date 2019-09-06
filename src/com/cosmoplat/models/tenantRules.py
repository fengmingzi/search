from app import db


class TenantRules(db.Model):
    __tablename__ = 'sc_tenant_crawling_rules'
    id = db.Column(db.BigInteger, primary_key=True)
    tenant_uni_code = db.Column(db.String(100))
    category_name = db.Column(db.String(100))
    index_name = db.Column(db.String(100))
    target_domain = db.Column(db.String(100))
    entrance_url = db.Column(db.String(100))
    detail_page_url_xpath = db.Column(db.String(100))
    next_page_type = db.Column(db.Integer)
    total_page = db.Column(db.Integer)
    next_page_xpath = db.Column(db.String(100))
    detail_title_xpath = db.Column(db.String(100))
    detail_content_xpath = db.Column(db.String(100))
    is_deleted = db.Column(db.Boolean)
    create_time = db.Column(db.String(100))
    category_name = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<TenantRules {}>'.format(self.tenant_uni_code)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
