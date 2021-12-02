# encoding: utf-8
import shutil
import os

src_dir = "."
exclude_ctype = {'00.Sample Courses', '01.财富密码', '02.财遇见你', 'overrides', '.git',
                 '.github', '.vscode', 'zips', 'labs', 'codes', 'doc_imgs', 'notes', 'exams'}
exclude_course = {'大数据处理技术', '102046_大数据处理技术'}

if __name__ == '__main__':
    for ctype in [c for c in os.listdir(src_dir) if os.path.isdir(c)]:
        if ctype in exclude_ctype:
            continue
        ctype_path = os.path.join(src_dir, ctype)
        for course in [c for c in os.listdir(ctype_path) if os.path.isdir(os.path.join(ctype_path, c))]:
            if course in exclude_course:
                continue
            cpath = os.path.join(ctype_path, course)
            shutil.copy("./template.md", os.path.join(cpath, "README.md"))
