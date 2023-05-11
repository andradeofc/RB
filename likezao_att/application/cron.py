from application.models import User

def execute():
    users = User.objects.all().filter(is_superuser=False).all()
    for user in users:
        user.today_earning = 0
        user.save()
