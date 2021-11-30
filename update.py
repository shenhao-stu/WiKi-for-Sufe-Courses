import os
import zipfile
from urllib.parse import quote

EXCLUDE_DIRS = ['.git', 'docs', '.vscode', '.idea', '.circleci',
                'site', 'overrides', '.github', 'script', 'images', 'zips']
README_MD = ['README.md', 'readme.md', 'index.md']

TXT_EXTS = ['md', 'txt']
TXT_URL_PREFIX = 'https://github.com/shenhao-stu/WiKi-for-Sufe-Courses/blob/master/'
BIN_URL_PREFIX = 'https://github.com/shenhao-stu/WiKi-for-Sufe-Courses/raw/master/'
CDN_PREFIX = 'https://curly-shape-d178.qinse.workers.dev/'
CDN_RAW_PREFIX = 'https://github.com/shenhao-stu/WiKi-for-Sufe-Courses/blob/zips/'


def make_zip(dir_path: str, zip_path: str):
    zip = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dir_path):
        fpath = path.replace(dir_path, "")
        for filename in filenames:
            zip.write(os.path.join(path, filename),
                      os.path.join(fpath, filename))
    zip.close()


def size_format(size: int):
    if size < 1024:
        return '{}B'.format(size)
    elif size < 1024 * 1024:
        return '{:.2f}KB'.format(size / 1024)
    elif size < 1024 * 1024 * 1024:
        return '{:.2f}MB'.format(size / 1024 / 1024)
    else:
        return '{:.2f}GB'.format(size / 1024 / 1024 / 1024)


def get_file_size(path: str):
    return size_format(os.path.getsize(path))


def list_files(course: str):
    filelist_texts = '## 文件列表\n\n'
    filelist_texts_cdn = '### 一键下载（CDN加速）\n\n'
    zip_path = os.path.join('zips', '{}.zip'.format(course))
    print(course, get_file_size(zip_path))
    filelist_texts_cdn += f"- [{os.path.basename(course)}.zip({get_file_size(zip_path)})]({CDN_PREFIX}/{CDN_RAW_PREFIX}/{course}.zip)\n\n"

    filelist_texts_org = '### GitHub原始链接\n\n'
    readme_path = ''
    for root, dirs, files in os.walk(course):
        files.sort()
        level = root.replace(course, '').count(os.sep)
        indent = ' ' * 4 * level
        filelist_texts_org += '{}- {}\n'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if f not in README_MD:
                if f.split('.')[-1] in TXT_EXTS:
                    filelist_texts_org += '{}- [{}]({})\n'.format(subindent,
                                                                  f, TXT_URL_PREFIX + quote('{}/{}'.format(root, f)))
                else:
                    filelist_texts_org += '{}- [{}]({})\n'.format(subindent,
                                                                  f, BIN_URL_PREFIX + quote('{}/{}'.format(root, f)))
            elif root == course and readme_path == '':
                readme_path = '{}/{}'.format(root, f)
    return filelist_texts + filelist_texts_cdn + filelist_texts_org, readme_path


def generate_md(course: str, filelist_texts: str, readme_path: str, topic: str):
    final_texts = ['\n\n', filelist_texts]
    if readme_path:
        with open(readme_path, 'r', encoding='utf-8') as file:
            final_texts = file.readlines() + final_texts
    topic_path = os.path.join('docs', topic)
    if not os.path.isdir(topic_path):
        os.mkdir(topic_path)
    with open(os.path.join(topic_path, '{}.md'.format(course)), 'w', encoding='utf-8') as file:
        file.writelines(final_texts)


if __name__ == '__main__':
    global PROJECT_PATH
    PROJECT_PATH = os.path.abspath(__file__)

    if not os.path.isdir('docs'):
        os.mkdir('docs')

    if not os.path.isdir('zips'):
        os.mkdir('zips')

    topics = list(filter(lambda x: os.path.isdir(x) and (
        x not in EXCLUDE_DIRS), os.listdir('.')))  # list topics

    for topic in topics:
        topic_path = os.path.join('.', topic)
        if not os.path.isdir(os.path.join('zips', topic)):
            os.mkdir(os.path.join('zips', topic))

        courses = list(filter(lambda x: os.path.isdir(os.path.join(topic_path, x)) and (
            x not in EXCLUDE_DIRS), os.listdir(topic_path)))  # list courses

        for course in courses:
            course_path = os.path.join(".", topic, course)

            make_zip(course_path,
                     os.path.join('zips', topic, '{}.zip'.format(course)))
            filelist_texts, readme_path = list_files(course_path)

            generate_md(course, filelist_texts, readme_path, topic)

    with open('README.md', 'r', encoding='utf-8') as file:
        mainreadme_lines = file.readlines()

    with open('docs/index.md', 'w', encoding='utf-8') as file:
        file.writelines(mainreadme_lines)
