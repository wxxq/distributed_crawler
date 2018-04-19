# -*- coding:utf-8 -*-
import sys
from service.base_service import BaseService
from job.xq_user_article_task import UserArticle


class XQUserArticleService(BaseService):

    get_task_sql = "select task_id,user_id,page_no,status, nice, selected, http_code from task_user_article WHERE selected = 0 and http_code =-1 and status = 0  order by nice LIMIT %s"

    def __init__(self, setting):
        BaseService.__init__(self, self.get_task_sql, 'task_user_article', UserArticle, setting)


