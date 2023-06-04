import matplotlib
matplotlib.use('Agg')

import io
import base64
import logomaker
from flask import Flask, render_template, request, send_file, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                # 没有选择文件
                # 执行相应的逻辑
                sequence_list = request.form['sequence_list']
                sequence_list = sequence_list.split('\n')  # 将字符串按换行符分割成列表
                sequence_list = [seq.strip().upper() for seq in sequence_list]  # 去除每个序列前后的空白并转换为大写
            else:
                # 已选择文件
                # 执行相应的逻辑
                sequence_list = file.read().decode('utf-8').split('\n')
                sequence_list = [sequence.strip().upper() for sequence in sequence_list]
        else:
            sequence_list = request.form.get('sequence_list').split('\n')
            sequence_list = [sequence.strip().upper() for sequence in sequence_list]
        
        # 移除空行和换行符号
        sequence_list = [sequence for sequence in sequence_list if sequence != '']
        # 将序列转换为字符串形式
        sequence_list = [''.join(sequence) for sequence in sequence_list]
        # 将序列列表转换为 logomaker 的 dataframe 对象
        df = logomaker.alignment_to_matrix(sequence_list)

        # 设置每个氨基酸的颜色
        color_scheme = {
            'A': 'green',
            'C': 'blue',
            'D': 'olive',
            'E': 'yellow',
            'F': 'purple',
            'G': 'orange',
            'H': 'cyan',
            'I': 'magenta',
            'K': 'lime',
            'L': 'pink',
            'M': 'teal',
            'N': 'lavender',
            'P': 'brown',
            'Q': 'beige',
            'R': 'maroon',
            'S': 'lightgreen',
            'T': 'red',
            'V': 'coral',
            'W': 'navy',
            'Y': 'grey',
        }
        # 创建 Sequence Logo
        logo = logomaker.Logo(df,color_scheme)

        # 设置图表标题
        logo.ax.set_title('Sequence Logo')

        # 将图表转换为图片
        img_data = io.BytesIO()
        logo.fig.savefig(img_data, format='png')
        img_data.seek(0)

        # 将图片数据转换为 base64 编码字符串
        img_base64 = base64.b64encode(img_data.read()).decode('utf-8')

        if 'action' in request.form and request.form['action'] == 'Download PNG':
            # 创建新的 BytesIO 对象并写入图像数据
            png_data = io.BytesIO()
            logo.fig.savefig(png_data, format='png')
            png_data.seek(0)
            # 下载 PNG 图片
            return send_file(png_data, as_attachment=True, attachment_filename='logo.png', mimetype='image/png')
        elif 'action' in request.form and request.form['action'] == 'Download JPEG':
            # 创建新的 BytesIO 对象并写入图像数据
            jpeg_data = io.BytesIO()
            logo.fig.savefig(jpeg_data, format='jpeg')
            jpeg_data.seek(0)
            # 下载 JPEG 图片
            return send_file(jpeg_data, as_attachment=True, attachment_filename='logo.jpeg', mimetype='image/jpeg')
        elif 'action' in request.form and request.form['action'] == 'Download SVG':
            # 创建新的 BytesIO 对象并写入图像数据
            svg_data = io.BytesIO()
            logo.fig.savefig(svg_data, format='svg')
            svg_data.seek(0)
            # 下载 SVG 图片
            return send_file(svg_data, as_attachment=True, attachment_filename='logo.svg', mimetype='image/svg+xml')
        else:
            chart_url = url_for('show_image', img_base64=img_base64, sequence_list='\n'.join(sequence_list))
            return redirect(chart_url)
    else:
        # 默认序列列表
        sequence_list = []
        return render_template('index.html', sequence_list='\n'.join(sequence_list))

@app.route('/show_image')
def show_image():
    img_base64 = request.args.get('img_base64')
    sequence_list = request.args.get('sequence_list')
    return render_template('show_image.html', img_base64=img_base64, sequence_list=sequence_list)

@app.route('/information')
def information():
    return render_template('information.html')

if __name__ == '__main__':
    app.run()