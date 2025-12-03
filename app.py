import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

# 設定上傳資料夾與允許的檔案類型
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'change_this_to_a_random_secret_key'  # 用於 flash 訊息

# 確保 uploads 資料夾存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename: str) -> bool:
    """檢查檔名是否為允許的圖片格式"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 檢查是否有勾選同意書（前端的 checkbox name="agree"）
        if 'agree' not in request.form:
            flash('請先勾選「我已閱讀並同意研究說明」。')
            return redirect(request.url)

        # 檢查是否有收到檔案
        if 'photo' not in request.files:
            flash('找不到上傳的檔案欄位。')
            return redirect(request.url)

        file = request.files['photo']

        # 檢查是否有選檔案
        if file.filename == '':
            flash('請先選擇一張照片再上傳。')
            return redirect(request.url)

        # 檢查檔案格式
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # 這裡你往後可以加上：使用者ID或時間戳記，避免檔名重複
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            flash('上傳成功，謝謝你的參與！')
            return redirect(url_for('index'))
        else:
            flash('只接受圖片檔案：png, jpg, jpeg, gif。')
            return redirect(request.url)

    # GET 方法：顯示頁面
    return render_template('index.html')


if __name__ == '__main__':
    # 本地測試用，Render 上實際會用 gunicorn 啟動
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
