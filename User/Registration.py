import cgi


def test():
    form_data = cgi.FieldStorage()
    print(form_data)
