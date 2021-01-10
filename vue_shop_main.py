import json
import os
import datetime
import random
import string

from flask import Flask, request, jsonify
from flask_cors import CORS
from copy import deepcopy

app = Flask(__name__)
# 解决跨域问题
cors = CORS(app, supports_credentials=True)


# from flask_login import login_manager, UserMixin, login_required

# login_manager_local = login_manager.LoginManager()
# login_manager_local.init_app(app)
# login_manager_local.session_protection = 'strong'
# login_manager_local.login_view = 'login'

# from flask_login import login_required


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return None
    else:
        data = request.form.to_dict()
        data1 = json.loads(request.get_data().decode())
        if not data:
            username = data1['username']
            password = data1['password']
        else:
            username = data['username']
            password = data['password']
        if username == 'admin' and password == "123456":
            data = {
                'id': 500,
                'rid': 0,
                'username': username,
                'mobile': 12345678,
                'email': 'asfdsfsd@163.com',
                'token': 'Bearer 123456'
            }
            meta = {
                "msg": "登陆成功",
                "stats": 200
            }
            return jsonify({'data': data, 'meta': meta})
        meta = {
            "msg": "登陆失败",
            "stats": 400
        }
        return jsonify({'data': '', 'meta': meta})


def loginValidate():
    token = request.headers.get('Authorization', '')
    if not token:
        return False
    if token == 'Bearer 123456':
        return True
    return False


@app.route('/abc')
# @login_required
def abc():
    return '1'


# 菜单数据
menus_dict = [
    {
        'id': 1,
        'authName': '用户管理',
        "path": "null",
        'pid': 0,
        'level': 0,
        "children": [
            {
                'id': 7,
                'authName': '用户列表',
                'path': 'users',
                'children': [
                    {
                        'id': 15,
                        'authName': '添加用户',
                        "path": "null",
                        'pid': 7,
                        'level': 2,
                    }
                ],
                'pid': 1,
                'level': 1
            }
        ]
    },

    {
        'id': 2,
        'authName': '权限管理',
        "path": "null",
        'pid': 0,
        'level': 0,
        "children": [
            {
                'id': 8,
                'authName': '角色列表',
                'path': 'roles',
                'children': [
                    {
                        'id': 16,
                        'authName': '添加角色',
                        "path": "null",
                        'pid': 8,
                        'level': 2,
                    }
                ],
                'level': 1,
                'pid': 2
            },
            {
                'id': 11,
                'authName': '权限列表',
                'path': 'rights',
                'children': [

                    {
                        'id': 17,
                        'authName': '添加权限',
                        "path": "null",
                        'pid': 11,
                        'level': 2,
                    }

                ],
                'level': 1,
                'pid': 2
            },

        ]
    },
    {
        'id': 3,
        'authName': '商品管理',
        "path": "null",
        'pid': 0,
        'level': 0,
        "children": [
            {
                'id': 10,
                'authName': '商品列表',
                'path': 'goods',
                'children': [
                    {
                        'id': 22,
                        'authName': "添加商品",
                        'path': 'null'
                    }
                ],
                'level': 1,
                'pid': 3
            },
            {
                'id': 12,
                'authName': '分类参数',
                'path': 'params',
                'children': [

                ],
                'level': 1,
                'pid': 3
            },
            {
                'id': 13,
                'authName': '商品分类',
                'path': 'categories',
                'children': [
                    {

                        'id': 25,
                        'authName': '添加分类',
                        "path": "null",
                        'pid': 13,
                        'level': 2,

                    },
                    {
                        'id': 19,
                        'authName': '修改分类',
                        "path": "null",
                        'pid': 13,
                        'level': 2,
                    },
                    {

                        'id': 33,
                        'authName': '删除分类',
                        "path": "null",
                        'pid': 13,
                        'level': 2,

                    },
                ],
                'level': 1,
                'pid': 3
            },
        ]
    },
    {
        # 订单 = mock
        'id': 4,
        'authName': '订单管理',
        "path": "null",
        'pid': 0,
        'level': 0,
        "children": [
            {
                'id': 9,
                'authName': '订单列表',
                'path': 'null',
                'children': [
                    {

                        'id': 26,
                        'authName': '添加订单',
                        "path": "null",
                        'pid': 9,
                        'level': 2,

                    }
                ],
                'level': 1,
                'pid': 4
            }
        ]
    },
    {
        # 　添加俩字 -- 日志
        'id': 5,
        'authName': '日志数据统计',
        "path": "null",
        'pid': 0,
        'level': 0,
        "children": [
            {
                'id': 6,
                'authName': '日志数据',
                'path': 'null',
                'children': [
                    {
                        'id': 28,
                        'authName': '添加数据',
                        "path": "null",
                        'pid': 6,
                        'level': 2,
                    }
                ],
                'level': 1,
                'pid': 5
            }
        ]
    }
]
meta_error = {
    'msg': 'token不存在或错误',
    'state': 404
}
# 用户列表
users_list = {
    'data': {
        'pagenum': 1,
        'total': '',
        'users': [
            {
                'id': 500,
                'role_name': '超级管理员',
                'username': 'admin',
                'create_time': '1486720211',
                'mobile': 13313029856,
                'email': '123@163.com',
                'mg_state': True,
                'password': 123456
            },
            {
                'id': 502,
                'role_name': '测试角色2',
                'username': 'linken',
                'create_time': '1486720211',
                'mobile': 13313029823,
                'email': '123214@163.com',
                'mg_state': False,
                'password': 123456
            },
            {
                'id': 503,
                'role_name': '测试角色3',
                'username': 'linken1',
                'create_time': '1486720211',
                'mobile': 13313023823,
                'email': '1232124@163.com',
                'mg_state': False,
                'password': 123456
            },
            {
                'id': 504,
                'role_name': '测试角色4',
                'username': 'linken2',
                'create_time': '1486720211',
                'mobile': 13413029823,
                'email': '12321114@163.com',
                'mg_state': True,
                'password': 123456
            },
        ]
    },
    'meta': {
        'msg': "获取管理员列表成功",
        'state': 200
    }
}
users_list['data']['total'] = len(users_list['data']['users'])


@app.route('/api/menus')
def menus():
    if loginValidate():
        # print(1, loginValidate())
        meta = {
            'msg': '获取菜单列表成功',
            'state': 200
        }
        return jsonify({'data': menus_dict, 'meta': meta})

    return jsonify({'data': '', 'meta': meta_error})


id = 600


@app.route('/api/users', methods=['GET', 'POST'])
def userList():
    if request.method == 'GET':
        print(555555)
        data = request.args.to_dict()
        users_list_data = deepcopy(users_list)
        users_list_data_user = []
        if data['query']:
            query = data['query']
            for x in users_list['data']['users']:
                for y in x.values():
                    if query in str(y):
                        users_list_data_user.append(x)
            users_list_data['data']['users'] = users_list_data_user
            users_list_data['data']['total'] = len(users_list_data['data']['users'])
            print(users_list_data)
            return jsonify(users_list_data)
    elif request.method == 'POST':
        global id
        id += 1
        data = json.loads(request.get_data().decode())
        # print(data)
        data['id'] = id
        data['role_name'] = '暂无'
        data['create_time'] = '1486720211'
        data['mg_state'] = True
        users_list['data']['users'].append(data)
        users_list['data']['total'] += 1
        users_list1 = deepcopy(users_list)
        # print(users_list1)
        users_list1['meta']['state'] = 201
        return jsonify(users_list1)

    return jsonify(users_list)


@app.route('/api/users/<int:uid>/state/<type>', methods=['PUT'])
def insert_users(uid, type):
    if request.method == 'PUT':
        for x in users_list['data']['users']:
            if x['id'] == uid:
                x['mg_state'] = type
                return jsonify(users_list)
    return jsonify({'data': '', 'meta': {'msg': "失败", 'state': 404}})


@app.route('/api/users/<int:id>', methods=['PUT', 'GET', 'DELETE'])
def update_users(id):
    if request.method == 'GET':
        # print(id)
        for x in users_list['data']['users']:
            if x['id'] == id:
                # print(100000000)
                data = {
                    'id': id,
                    'username': x['username'],
                    'role_id': '暂无',  ##################################################
                    'mobile': x['mobile'],
                    'email': x['email']
                }
                break
        meta = {
            'msg': '查询成功',
            'status': 200
        }
        return jsonify({'data': data, 'meta': meta})
    elif request.method == 'PUT':
        data1 = json.loads(request.get_data().decode())
        # print(data1)
        for x in users_list['data']['users']:
            # print(id,x['id'],type(id),type(x['id']))
            if x['id'] == id:
                # print(22222222)
                x['mobile'] = data1['mobile']
                x['email'] = data1['email']
                meta = {
                    'msg': '更新成功',
                    'status': 200
                }
                # print(111111,users_list)
                return jsonify({'data': x, 'meta': meta})
    elif request.method == 'DELETE':
        for x in range(len(users_list['data']['users'])):
            # print(users_list['data']['users'][x]['id'],id)
            if users_list['data']['users'][x]['id'] == id:
                a = users_list['data']['users'].pop(x)
                # print(1111111,a)
                break
        meta = {
            'msg': '删除成功',
            'status': 200
        }
        # print(users_list['data']['users'])
        return jsonify({'data': 'null', 'meta': meta})


@app.route('/api/rights/<type>')
def rights(type):
    meta = {
        'status': 200,
        'msg': '获取权限数据成功'
    }
    menus_dict1 = deepcopy(menus_dict)
    if type == 'tree':

        return jsonify({'data': menus_dict, 'meta': meta})
    elif type == 'list':
        menus_dict1 = deepcopy(menus_dict)
        for x in menus_dict1:
            if 'children' in x.keys():
                for y in x['children']:
                    menus_dict1.append(y)
                del x['children']
        return jsonify({'data': menus_dict1, 'meta': meta})


roles_list = [
    {
        'id': 30,
        'roleName': "主管",
        'roleDesc': '技术负责人',
        'children': [
            menus_dict[0],
            menus_dict[1],
            menus_dict[2],
            menus_dict[3],
            menus_dict[4]
        ]
    },
    {
        'id': 31,
        'roleName': "测试负责人",
        'roleDesc': '测试负责人',
        'children': [
            menus_dict[2]
        ]
    },
    {
        'id': 32,
        'roleName': "产品负责人",
        'roleDesc': '产品负责人',
        'children': [
            menus_dict[3]
        ]
    }
]


@app.route('/api/roles', methods=['GET', "POST", "PUT", "DELETE"])
def roles():
    if request.method == 'GET':
        meta = {
            'status': 200,
            'msg': '获取成功'
        }
        return jsonify({'data': roles_list, 'meta': meta})
    elif request.method == 'POST':
        global id
        id += 1
        data = json.loads(request.get_data().decode())
        # print(data)
        meta = {
            'status': 201,
            'msg': '添加成功'
        }
        data1 = {
            'id': id,
            'roleName': data['roleName'],
            'roleDesc': data['roleDesc'],
            'children': [
                menus_dict[2]
            ]
        }
        roles_list.append(data1)
        return jsonify({'data': data1, 'meta': meta})
    elif request.method == 'PUT':
        data = json.loads(request.get_data().decode())
        # print(data)
        for x in roles_list:
            if x['id'] == data['id']:
                x['roleName'] = data['roleName']
                x['roleDesc'] = data['roleDesc']
                meta = {
                    'status': 200,
                    'msg': '更新成功'
                }
                # print(1111111,roles_list)
                return jsonify({'data': '', 'meta': meta})


@app.route('/api/roles/find/<int:id>', methods=['GET', "POST", 'DELETE'])
def findRoles(id):
    if request.method == 'GET':
        for x in roles_list:
            if x['id'] == id:
                meta = {
                    'msg': '查询成功',
                    'status': 200
                }
                data = x
                return jsonify({'data': data, 'meta': meta})
    elif request.method == 'DELETE':
        for x in range(len(roles_list)):
            if roles_list[x]['id'] == id:
                print(11111111, id)
                del roles_list[x]
                meta = {
                    'status': 200,
                    'msg': '删除成功'
                }
                print(roles_list)
                return jsonify({'data': 'null', 'meta': meta})


@app.route('/api/roles/<int:id>/rights/<int:childrenId>', methods=['DELETE'])
def rolesDEL(id, childrenId):
    if request.method == 'DELETE':
        meta = {
            'msg': '删除成功',
            'status': 200
        }
        print('start', id, childrenId)
        for x in roles_list:
            if x['id'] == id:
                # input('1111寻找')
                # for y in x['children']:
                for y in range(len(x['children'])):
                    if x['children'][y]['id'] == childrenId:
                        del x['children'][y]
                        return jsonify({'data': x['children'], 'meta': meta})
                    for k1 in range(len(x['children'][y]['children'])):
                        if x['children'][y]['children']:
                            if x['children'][y]['children'][k1]['id'] == childrenId:
                                del x['children'][y]['children'][k1]
                                return jsonify({'data': x['children'], 'meta': meta})
                        for k2 in range(len(x['children'][k1]['children'])):
                            if x['children'][y]['children'][k1]['children']:
                                # print(x['children'][y]['children'][k1]['children'])
                                # input('@@@')
                                if x['children'][y]['children'][k1]['children'][k2]['id'] == childrenId:
                                    del x['children'][y]['children'][k1]['children'][k2]
                                    return jsonify({'data': x['children'], 'meta': meta})


@app.route('/api/roles/<int:roleId>/rights', methods=['POST'])
def UpdateRoles(roleId):
    data = json.loads(request.get_data().decode())
    datalist = data['rids']
    # 角色人
    resultRoles = {}
    # print(data,11111,datalist)
    for x in roles_list:
        if x['id'] == roleId:
            resultRoles = x
            break
    datalist1 = []
    for x in datalist:
        if x != ',':
            datalist1.append(x)
    alist = []
    for x in menus_dict:
        for y in datalist1:
            # print(222222,y, x['id'])
            if int(x['id']) == int(y):
                if x['id'] not in alist:
                    alist.append(x['id'])
                    print(11111, x, resultRoles)
                    resultRoles['children'].append(x)

    meta = {
        'status': 200,
        'msg': '成功'
    }
    # print(resultRoles,roles_list)

    return jsonify({'data': x, 'meta': meta})


# 分配角色
@app.route('/api/users/<int:id>/role', methods=['PUT'])
def distributionRoles(id):
    if request.method == 'PUT':
        for x in users_list['data']['users']:
            if x['id'] == id:
                data = json.loads(request.get_data().decode())
                print(data)
                rid = data['rid']
                if rid == 30:
                    x['role_name'] = "主管"
                elif rid == 31:
                    x['role_name'] = "测试负责人"
                elif rid == 32:
                    x['role_name'] = "产品负责人"
                msg = {
                    'msg': "设置角色成功",
                    'status': 200
                }
                # print(11111,x)
                return jsonify({'data': x, 'meta': msg})


# 商品分类数据
goods = [
    {
        'cate_id': 500,
        'cate_name': '茄子',
        'cate_pid': 0,
        'cate_level': 0,
        'cate_delete': 'false',
        'children': [
            {
                'cate_id': 505,
                'cate_name': '茄子1',
                'cate_pid': 500,
                'cate_level': 1,
                'cate_delete': 'false',
                'children': []
            },
        ]
    },
    {
        'cate_id': 501,
        'cate_name': '红烧猪蹄子',
        'cate_pid': 0,
        'cate_level': 0,
        'cate_delete': 'true',
        'children': [
            {
                'cate_id': 506,
                'cate_name': '红烧猪蹄子',
                'cate_pid': 501,
                'cate_level': 1,
                'cate_delete': 'true',
                'children': []
            },
        ]
    },
    {
        'cate_id': 502,
        'cate_name': '苹果1',
        'cate_pid': 0,
        'cate_level': 0,
        'cate_delete': 'false',
        'children': []
    },
    {
        'cate_id': 503,
        'cate_name': '创世纪',
        'cate_pid': 0,
        'cate_level': 0,
        'cate_delete': 'true',
        'children': [
            {
                'cate_id': 504,
                'cate_name': '创世纪1',
                'cate_pid': 503,
                'cate_level': 1,
                'cate_delete': 'true',
                'children': [
                    {
                        'cate_id': 505,
                        'cate_name': '创世纪2',
                        'cate_pid': 504,
                        'cate_delete': 'true',
                        'cate_level': 2,
                    },
                ]
            },
        ]
    },

]
goodsId = 505


@app.route('/api/categories', methods=['GET', 'POST'])
def categoriesList():
    if request.method == 'GET':
        # type 1 一级分类  2是 1-2级分类 3是全部分类
        # 页数跟页也是
        date = request.args.to_dict()
        # print(date)
        if 'type' not in date.keys():
            date['type'] = 4
        date['type'] = int(date['type'])
        if date['type'] == 1:
            goods1 = []
            for x in goods:
                if x['cate_level'] == 1:
                    goods1.append(x)
        elif date['type'] == 2:
            # goods1 = []
            # for x in goods:
            #     print(x['cate_level'])
            #     if x['cate_level'] == 0 or x['cate_level'] == 1:
            #         goods1.append(x)
            goods1 = [
                {
                    'cate_id': 500,
                    'cate_name': '茄子',
                    'cate_pid': 0,
                    'cate_level': 0,
                    'cate_delete': 'false',
                    'children': [
                        {
                            'cate_id': 505,
                            'cate_name': '茄子1',
                            'cate_pid': 500,
                            'cate_level': 1,
                            'cate_delete': 'false',
                        },
                    ]
                },
                {
                    'cate_id': 501,
                    'cate_name': '红烧猪蹄子',
                    'cate_pid': 0,
                    'cate_level': 0,
                    'cate_delete': 'true',
                    'children': [
                        {
                            'cate_id': 506,
                            'cate_name': '红烧猪蹄子',
                            'cate_pid': 501,
                            'cate_level': 1,
                            'cate_delete': 'true',
                        },
                    ]
                },
                {
                    'cate_id': 502,
                    'cate_name': '苹果1',
                    'cate_pid': 0,
                    'cate_level': 0,
                    'cate_delete': 'false',
                },
                {
                    'cate_id': 503,
                    'cate_name': '创世纪',
                    'cate_pid': 0,
                    'cate_level': 0,
                    'cate_delete': 'true',
                    'children': [
                        {
                            'cate_id': 504,
                            'cate_name': '创世纪1',
                            'cate_pid': 503,
                            'cate_level': 1,
                            'cate_delete': 'true'
                        },
                    ]
                },

            ]
            meta = {
                'msg': '查询成功',
                'status': 200
            }
            total = len(goods1)
            # print(goods1)
            return jsonify({'data': goods1, 'meta': meta})
        elif date['type'] == 4:
            meta = {
                'msg': '查询成功',
                'status': 200
            }
            return jsonify({'data': goods, 'meta': meta})
        else:
            goods1 = goods
        # input('111111')
        meta = {
            'msg': '查询成功',
            'status': 200
        }
        total = len(goods1)
        data = {'result': goods1, 'total': total}

        return jsonify({'data': data, 'meta': meta})
    if request.method == 'POST':
        global goodsId
        goodsId += 1
        data = json.loads(request.get_data().decode())
        # print(1111111,data)
        # input('99999')
        good = {
            'cate_id': goodsId,
            'cate_name': data['cate_name'],
            'cate_pid': data['cate_pid'],
            'cate_level': data['cate_level']
        }
        if data['cate_level'] == 0:

            goods.append(good)
        elif data['cate_level'] == 1:
            for x in goods:
                if x['cate_id'] == data['cate_pid']:
                    x['children'].append(good)
                    # print(1111,x)
                    # print(22222222,goods)
        elif data['cate_level'] == 2:
            for x in goods:
                if len(x['children']) != 0:
                    for y in x['children']:
                        if y['cate_id'] == data['cate_pid']:
                            # print(1111, y)
                            y['children'].append(good)

                            # print(22222222, goods)

        meta = {
            'msg': '创建成功',
            'status': 201
        }
        return jsonify({'data': good, 'meta': meta})


attributesOnlyList = [
    {
        'attr_id': 2,
        'attr_name': '静态版式1',
        'cate_id': 505,
        'attr_sel': 'only',
        'attr_write': '',
        'attr_vals': '好看 超好看 静态'  # 可选项 空格分割
    },
{
        'attr_id': 3,
        'attr_name': '静态版式2',
        'cate_id': 506,
        'attr_sel': 'only',
        'attr_write': '',
        'attr_vals': '好看 超好看 静态'  # 可选项 空格分割
    }
]

attributesManyList = [
    {
        'attr_id': 1,
        'attr_name': '动态版式1',
        'cate_id': 505,
        'attr_sel': 'many',
        'attr_write': 'list',
        'attr_vals': '动态 嗯，不错 你猜猜 哈哈，得了， nihaoc'  # 可选项 空格分割
    },
{
        'attr_id': 0,
        'attr_name': '动态版式2',
        'cate_id': 506,
        'attr_sel': 'many',
        'attr_write': 'list',
        'attr_vals': '1动态 1嗯，1不错 1你猜猜 1哈哈，1得了， nihaoc'  # 可选项 空格分割
    },
]

attr_id = 10


@app.route('/api/categories/<int:id>/attributes', methods=['GET', 'POST'])
def attributes(id):
    if request.method == 'GET':
        data = request.args.to_dict()
        print(2222, data)
        # input('dddd')
        sel = data['sel']
        # 静态参数
        # result = {
        #     'attr_id': 1,
        #     'attr_name': '静态版式',
        #     'cate_id': 505,
        #     'attr_sel': '',
        #     'attr_write': '',
        #     'attr_vals': '1,2,3'
        # }
        meta = {
            'msg': '',
            'status': 200
        }
        if id == 505 and sel == 'only':
            # result['attr_sel'] = 'only'
            # result['attr_write'] = 'manual'
            # result['attr_vals'] = ''
            return jsonify({'data': attributesOnlyList, 'meta': meta})
        # 动态参数
        if id == 505 and sel == 'many':
            # result['attr_sel'] = 'many'
            # result['attr_write'] = 'list'
            # result['attr_name'] = '动态版式'
            return jsonify({'data': attributesManyList, 'meta': meta})
    elif request.method == 'POST':
        global attr_id
        attr_id += 1
        data = json.loads(request.get_data().decode())
        attr_name = data['attr_name']
        attr_sel = data['attr_sel']
        print(4444, data)
        # input('333333')
        result = {
            'attr_id': attr_id,
            'attr_name': attr_name,
            'cate_id': id,
            'attr_sel': attr_sel,
            'attr_write': '',
            'attr_vals': ''
        }
        if attr_sel == 'many':
            attributesManyList.append(result)
        elif attr_sel == 'only':
            attributesOnlyList.append(result)
        meta = {
            'msg': '',
            'status': 201
        }
        return jsonify({'data': data, 'meta': meta})


@app.route('/api/categories/<int:cateId>/attributes/<int:attr_id>', methods=['GET', 'PUT', 'DELETE'])
def findCategories(cateId, attr_id):
    if request.method == 'GET':
        data = request.args.to_dict()

        # print(data)
        # input('2222')
        sel = data['attr_sel']
        meta = {
            'msg': '',
            'status': 200
        }
        if sel == 'only':
            for x in attributesOnlyList:
                if x['attr_id'] == attr_id and x['cate_id'] == cateId:
                    return jsonify({'data': x, 'meta': meta})
        elif sel == 'many':
            for x in attributesManyList:
                if x['attr_id'] == attr_id and x['cate_id'] == cateId:
                    return jsonify({'data': x, 'meta': meta})
    elif request.method == 'PUT':
        data = json.loads(request.get_data().decode())
        print(2222, data)
        # input('@@@@@@@@@')
        attr_name = data['attr_name']
        attr_sel = data['attr_sel']
        data1 = ''
        if attr_sel == 'only':
            for x in attributesOnlyList:
                if x['attr_id'] == attr_id:
                    x['attr_name'] = attr_name
                    x['attr_vals'] = data['attr_vals']
                    data1 = x
        elif attr_sel == 'many':
            for x in attributesManyList:
                if x['attr_id'] == attr_id:
                    x['attr_name'] = attr_name
                    x['attr_vals'] = data['attr_vals']
                    data1 = x
        meta = {
            'msg': '',
            'status': 200
        }
        return jsonify({'data': data1, 'meta': meta})
    elif request.method == 'DELETE':
        for x in range(len(attributesManyList)):
            if attributesManyList[x]['attr_id'] == attr_id:
                del attributesManyList[x]
        for x in range(len(attributesOnlyList)):
            if attributesOnlyList[x]['attr_id'] == attr_id:
                del attributesOnlyList[x]
        meta = {
            'msg': '删除成功',
            'status': 200
        }
        return jsonify({'data': '', 'meta': meta})


# @app.route('/api/categories/<int:id>/attributes/<int:attr_id>',methods=['DELETE','PUT'])
# def attributesDel(id,attr_id):
#     if request.method == 'DELETE':
#         for x in range(len(attributesManyList)):
#             if attributesManyList[x]['attr_id'] == attr_id:
#                 del attributesManyList[x]
#         for x in range(len(attributesOnlyList)):
#             if attributesOnlyList[x]['attr_id'] == attr_id:
#                 del attributesOnlyList[x]
#         meta = {
#            'msg':'删除成功',
#            'status':200
#         }
#         return jsonify({'data':'','meta':meta})
#     elif request.method == 'PUT':
#         data = json.loads(request.get_data().decode())
#         # print(data)
#         attr_sel = data['attr_sel']
#         data1 = ''
#         if attr_sel == 'many':
#             for x in attributesManyList:
#                 if x['attr_id'] == attr_id:
#                     x['attr_name'] = data['attr_name']
#                     x['attr_vals'] = data['attr_vals']
#                     data1 = x
#         elif attr_sel == 'only':
#             for x in attributesOnlyList:
#                 if x['attr_id'] == attr_id:
#                     x['attr_name'] = data['attr_name']
#                     x['attr_vals'] = data['attr_vals']
#                     data1 = x
#         meta = {
#             'msg':'',
#             'status':200
#         }
#         return jsonify({'data':data1,'meta':meta})

goods_list = [
    {
        'goods_id': 1,
        'goods_name': '手机1我是填充字符效果的东西我是填充字符效果的东西我是填充字符效果的东西',
        'goods_price': 1000,
        'goods_number': 5,
        'goods_weight': 100,
        'good_state': 'null',
        'add_time': 1512954923,
        'upd_time': 1512954923,
        'host_number': 0,
        'is_promote': 'false'
    },
    {
        'goods_id': 2,
        'goods_name': '手机2',
        'goods_price': 1000,
        'goods_number': 5,
        'goods_weight': 100,
        'good_state': 'null',
        'add_time': 1512954923,
        'upd_time': 1512954923,
        'host_number': 0,
        'is_promote': 'false'
    },
    {
        'goods_id': 3,
        'goods_name': '手机3',
        'goods_price': 1000,
        'goods_number': 5,
        'goods_weight': 100,
        'good_state': 'null',
        'add_time': 1512954923,
        'upd_time': 1512954923,
        'host_number': 0,
        'is_promote': 'false'
    }
]

goods_id = 4


@app.route('/api/goods', methods=['GET','POST'])
def Goods():
    if request.method == 'GET':
        total = len(goods_list)
        data = request.args.to_dict()
        print(1111, data)
        query = data['query']
        # input('##########')
        meta = {
            'msg': '',
            'status': 200
        }
        if query:
            goods_list1 = []
            for x in goods_list:
                if query in x['goods_name']:
                    goods_list1.append(x)
            return jsonify({'data': {'goods': goods_list1, 'total': total}, 'meta': meta})

        return jsonify({'data': {'goods': goods_list, 'total': total}, 'meta': meta})
    elif request.method == 'POST':
        global goods_id
        goods_id += 1
        # data = request.form.to_dict()
        data = json.loads(request.get_data().decode())
        print(f'111111{data}')
        # input('@@@@')
        dict1 = {
            'goods_id': goods_id,
            'goods_name': data['goods_name'],
            'goods_price': data['goods_price'],
            'goods_number': data['goods_number'],
            'goods_weight': data['goods_weight'],
            'good_state': 'null',
            'add_time': 1512954923,
            'upd_time': 1512954923,
            'host_number': 'null',
            'is_promote': 'false',
            'goods_weight': data['goods_weight'],
            'goods_cate': data['goods_cate'],  #1,2,3 商品分类登记
            'goods_introduce':data['goods_introduce'],
            'pics':data['pics'],
            'attrs':data['attrs']
        }
        goods_list.append(dict1)

        meta = {
            'msg':'添加成功',
            'status':201
        }
    return jsonify({'data':dict1,'meta':meta})

@app.route('/api/goods/<int:id>', methods=['DELETE'])
def delGoods(id):
    if request.method == 'DELETE':
        for x in goods_list:
            if x['goods_id'] == id:
                goods_list.remove(x)
                meta = {
                    'status': 200,
                    'msg': '删除成功'
                }
                return jsonify({'data': '', 'meta': meta})

basedir = os.path.abspath(os.path.dirname(__file__)) #定义一个根目录 用于保存图片用
path = basedir + "/static/img/"          #定义一个图片存放的位置 存放在static下面
@app.route('/api/upload',methods=['POST'])
def upload():
    files = request.files

    print(f'file{files}')
    # 生成随机字符串，防止图片名字重复
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    # 获取图片文件
    img = request.files.get('file')
    #定义一个图片存放的位置 存放在static下面
    path = basedir + "/static/img/"
    #图片名称 给图片重命名 为了图片名称的唯一性
    imgName = ran_str + img.filename
    #图片path和名称组成图片的保存路径
    file_path = path + imgName
    #保存图片
    img.save(file_path)
    #这个是图片的访问路径，需返回前端（可有可无）
    url = '/static/img/'+imgName
    # print(1111, f'file{imgName},获取图片文件{img}')
    # input('@@@@@@')
    data = {
       'tmp_path':url,
        'url': f'http://127.0.0.1:8080/{url}'
    }
    meta = {
        'msg':'上传成功',
        'status':200
    }
    return jsonify({'meta':meta,'data':data})


########从这里开始 功能数据全部写死 没时间搞那么多了 写学好前端

if __name__ == '__main__':
    app.run(port=8080, debug=True)
