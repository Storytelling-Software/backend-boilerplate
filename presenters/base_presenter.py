class BasePresenter:
    def present_time(self, datetime):
        if datetime:
            return datetime.strftime('%Y-%m-%d %H:%M:%S')
        return None

    def present_date(self, datetime):
        if datetime:
            return datetime.strftime('%Y-%m-%d')
        return None

    def present_time_iso(self, datetime):
        if datetime:
            return datetime.strftime('%Y-%m-%dT%H:%M:%S')
        return None
