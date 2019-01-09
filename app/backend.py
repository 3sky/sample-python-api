#!flask/bin/python
from app import application, db
from app.models import AppStatus
from datetime import datetime
import time

class DefineQuery():
    
    def with_remove_instance_state_and_convert_date(in_query):
        result = in_query
        out_dict = result.__dict__.copy()
        del out_dict['_sa_instance_state']
        d = int(out_dict['updated_date'])
        out_dict['updated_date'] = datetime.fromtimestamp(d) 
        return out_dict
        
    def get_apps_id():
        ids = []
        for i in db.session.query(AppStatus.id).all():
            ids.append(int(i[0]))
        return ids

    def get_app_by_id(i):
        return DefineQuery.with_remove_instance_state_and_convert_date(AppStatus.query.filter_by(id=i).first())

    def add_new_app(app_n, app_v, user):
        t = AppStatus(app_name=app_n, app_version=app_v, updated_date=time.time(), updated_by=user)
        db.session.add(t)
        db.session.commit()

    def get_last_app():
        return DefineQuery.with_remove_instance_state_and_convert_date(AppStatus.query.order_by(AppStatus.id.desc()).first())

    def delete_app_by_id(i):
        d = AppStatus.query.filter_by(id=i).first()
        db.session.delete(d)
        db.session.commit()

    def update_column(col_name, val, i):
        d = AppStatus.query.filter_by(id=i).first()

        if col_name == 'app_name':
            d.app_name = val
        elif col_name == 'version':
            d.app_version = val
        else:
            d.updated_by = val

        db.session.commit()
