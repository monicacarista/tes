import django.contrib.auth.models as model
permit = model.Permission.objects.all()
users = model.User.objects.all()

def set_permissions(user_lst, permissions_lst):
    permissions = permit.filter(id__in = permissions_lst)
    for i in user_lst:
        user = users.get(id = i)
        user.user_permissions.clear()
        user.user_permissions.set(permissions)
        user.save()

def add_permissions(user_lst, permissions_lst):
    permissions = permit.filter(id__in = permissions_lst)
    for i in user_lst:
        user = users.get(id = i)
        for j in permissions_lst:
            user.user_permissions.add(j)
        user.save()


# Admin PC dan KD
permissions_lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 36, 40, 68, 72, 76, 80, 116, 128, 132, 136, 144, 148, 152]
user_lst = [3, 4,]
set_permissions(user_lst, permissions_lst)

# Admin dengan privilege ubah master barang
permissions_lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 36, 40, 68, 72, 76, 80, 116, 128, 132, 136, 144, 148, 152, 37, 38, 39, 65, 66, 67, 77, 78, 79, ]
user_lst = [5, 6, 7, 9, 15, 18, 20, 21, ]
set_permissions(user_lst, permissions_lst)

# Admin dengan packaging
permissions_lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 36, 40, 68, 72, 76, 80, 116, 128, 132, 136, 144, 148, 152, 37, 38, 39, 65, 66, 67, 77, 78, 79, 121, 122, 123, 124, 140, ]
user_lst = [11]
set_permissions(user_lst, permissions_lst)

# Only see report
permissions_lst = [4, 8, 12, 16, 20, 36, 68, 76, 84, 116, 128, 132, 136, 140, 148, 152]
user_lst = [12, 13, 16, 17, 19, 26, 27, 28, 29]
set_permissions(user_lst, permissions_lst)

# PPIC
permissions_lst = [1, 2, 3, 4, 77, 78, 79, 80]
user_lst = [22, 23, 24, 25]
set_permissions(user_lst, permissions_lst)

# New Report
permissions_lst = [164, 148, 168]
user_lst = [12, 13, 16, 17, 19, 26, 27, 28, 29] + [11] + [5, 6, 7, 9, 15, 18, 20, 21, ] + [3, 4,]
add_permissions(user_lst, permissions_lst)