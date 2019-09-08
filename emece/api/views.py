import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.db import connection
from django.template import RequestContext

from api.models import User


class TopRankings:
    def set_global_user_rankings(self):
        cursor = connection.cursor()
        cursor.execute('SELECT uid, sum(pts) as spts '
                       'FROM ('
                       'SELECT u.id as uid, 2 * SUM(e.point) as pts '
                       'FROM user u, event e '
                       'WHERE u.id=e.creatorId AND e.approved = TRUE '
                       'GROUP BY u.id '
                       'UNION '
                       'SELECT u.id as uid, SUM(e.point) AS pts '
                       'FROM user u, event e, `user-event` ue '
                       'WHERE u.id=ue.userId and e.id=ue.eventId and ue.approved=TRUE '
                       'GROUP BY u.id) as tbl '
                       'GROUP BY uid '
                       'HAVING spts IS NOT NULL '
                       'ORDER BY spts DESC;')
        self.rows = cursor.fetchall()

    def set_global_city_rankings(self):
        cursor = connection.cursor()
        cursor.execute('SELECT city, sum(pts) as spts '
                       'FROM ('
                       'SELECT e.city as city, 2 * SUM(e.point) as pts '
                       'FROM user u, event e '
                       'WHERE u.id=e.creatorId AND e.approved = TRUE '
                       'GROUP BY city '
                       'UNION '
                       'SELECT e.city as city, SUM(e.point) AS pts '
                       'FROM user u, event e, `user-event` ue '
                       'WHERE u.id=ue.userId and e.id=ue.eventId and ue.approved=TRUE '
                       'GROUP BY city) as tbl '
                       'GROUP BY city '
                       'HAVING spts IS NOT NULL '
                       'ORDER BY spts DESC;')
        self.rows = cursor.fetchall()

    def get_user(self, id, pts):
        user = User.objects.get(id=id)
        appended_name = ' '.join([user.first_name if user.first_name else '',
                                  user.middle_name if user.middle_name else '',
                                  user.last_name if user.last_name else '']).strip()
        return {
            'id': user.id,
            'tc': user.tckn,
            'name': appended_name if appended_name else 'NA',
            'city': user.city if user.city else 'NA',
            'email': user.email if user.email else 'NA',
            'pts': pts
        }

    def rows_as_json(self):
        users = []
        self.set_global_user_rankings()
        for row in self.rows:
            users.append(self.get_user(row[0], row[1]))

        cities = []
        self.set_global_city_rankings()
        for row in self.rows:
            cities.append({'name': row[0], 'pts': str(row[1])})

        return {'users': users, 'cities': cities}

@staff_member_required
def global_rankings_view(request):
    ranks = TopRankings()
    context = ranks.rows_as_json()

    r = render_to_response('global_ranking.html', context, RequestContext(request))
    return HttpResponse(r)
