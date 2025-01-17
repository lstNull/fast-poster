import base64

from flask import Flask, Response, request
from flask_cors import CORS
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

import C
import R
import dao
import poster
import key

app = Flask(__name__, static_url_path='')
logger = app.logger

# 跨域配置
CORS(app, supports_credentials=True)

# 上传配置
app.config['UPLOADED_PHOTOS_DEST'] = C.STORE_UPLOAD  # 文件储存地址
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # 文件大小限制，默认为16MB


@app.route('/')
def index():
    """
    重定向首页
    :return:
    """
    return app.send_static_file('index.html')


@app.route('/api/login', methods=['POST'])
def login():
    """
    登录
    :return:
    """
    accessKey = request.form['accessKey']
    secretKey = request.form['secretKey']
    if key.check(accessKey, secretKey):
        token = C.code(32)
        dao.save_token(token)
        return R.ok('登录成功').add('token', token).add('user', {'accessKey': accessKey, 'secretKey': secretKey}).json()
    else:
        return R.error('accessKey or secretKey not match!').json()


@app.before_request
def check_token():
    """
    检查token
    :return:
    """
    path = request.path
    filter_list = ['/api/user/posters']
    ignore = True
    for w in filter_list:
        if w in path:
            ignore = False
            break
    if ignore:
        return
    t = request.headers.get('token', None)
    if not t:
        return R.expire('没有token').json()
    dbtoken = dao.query_token(t)
    print(f'token判断: path={path}, token={t}, dbtoken={dbtoken}')
    if not dbtoken:
        return R.expire().json()


@app.route('/api/user/posters', methods=['GET'])
def query_user_posters():
    posters = dao.query_user_posters()
    return R.ok().add('posters', posters).json()


@app.route('/api/user/posters', methods=['POST'])
def save_or_update_user_poster():
    id = dao.save_or_update_user_poster(request.get_json())
    return R.ok().add("id", id).json()


@app.route('/api/user/posters/<id>', methods=['DELETE'])
def delete_user_posters(id):
    dao.db_delete_poster(int(id))
    return R.ok().json()


@app.route('/api/user/posters/copy/<id>', methods=['POST'])
def copy_user_poster(id):
    id = dao.copy_user_poster(id)
    return R.ok().add("id", id).json()


@app.route('/api/upload', methods=['POST'])
def upload_file():
    name = C.code(16)
    filename = photos.save(request.files['file'], name=name + '.')
    # filename = photos.save(request.files['file'], name=name)
    path = photos.path(filename)
    path = C.get_url_path(path)
    return R.ok().add("url", path).json()


@app.route('/api/link', methods=['POST'])
def get_link():
    """获取分享链接"""
    # TODO: 接口参数校验
    # print("获取分享链接")
    param = request.get_json()
    if not key.check(param['accessKey'], param['secretKey']):
        return R.error('accessKey or secretKey not match').json()
    return dao.get_share_link(param)


@app.route('/view/<string:code>', methods=['GET'])
def view(code: str):
    """
    查看海报
    :param code:
    :return:
    """
    code = code[:code.index('.')]
    data = dao.find_share_data(code)
    if data is None:
        # TODO: 返回一张提示图片
        return '不好意思，海报不见了'
    return resp_poster_img(data)


@app.route('/b64/<string:code>', methods=['GET'])
def view_b64(code: str):
    """
    返回base64编码
    :param code:
    :return:
    """
    code = code[:code.index('.')]
    data = dao.find_share_data(code)
    if data is None:
        return '不好意思，海报不见了'
    buf, mimetype = poster.drawio(data)
    base64_data = base64.b64encode(buf.read())
    s = base64_data.decode()
    return s


@app.route('/api/preview', methods=['POST'])
def preview():
    """
    预览
    :return:
    """
    data = request.get_json()
    return resp_poster_img(data)


def resp_poster_img(data):
    """返回海报图片"""
    buf, mimetype = poster.drawio(data)
    resp = Response(buf, mimetype=mimetype)
    resp.add_etag()
    resp.automatically_set_content_length = True
    resp.headers.add('Cache-Control', 'max-age=60')
    # resp.headers.add('Access-Control-Allow-Origin', '*')
    # logger.info('请求返回了')
    return resp


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=9001, debug=True)
    # 调整为4核
    app.run(host="0.0.0.0", port=9001, debug=True, threaded=False, processes=4)
    print('启动...')
