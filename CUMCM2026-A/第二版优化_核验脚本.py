from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import pymupdf as fitz
pdf=fitz.open(r'C:\codex\tmp\v2_opt\render_final4\药材烘干问题_论文第二版优化.pdf')
print('pages',len(pdf),'blank',[i+1 for i,p in enumerate(pdf) if len(p.get_text().strip())<10])
for h in ['一、问题重述','二、问题分析','2.1 总体技术路线','三、模型假设与符号说明','四、通用模型与数值方法','五、问题一预热平衡阶段','六、问题二变物性烘干过程','七、问题三烘干终止时间','八、问题四考虑尺寸收缩','九、模型检验与讨论','十、模型评价与改进','参考文献','附录A 程序与完整结果说明','附录B 数值求解完整源程序','附录C 绘图完整源程序']:
 print(h,[i+1 for i,p in enumerate(pdf) if h in p.get_text()])
with ZipFile(r'C:\Users\twili\Downloads\CUMCM2026Problems(1)\A题\论文修改版\药材烘干问题_论文第二版优化.docx') as z: root=etree.fromstring(z.read('word/document.xml'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
t=''.join(root.xpath('.//w:t/text()|.//m:t/text()',namespaces=ns));print('math',len(root.xpath('.//m:oMath',namespaces=ns)),'empty',len(root.xpath('.//m:e[not(*)]',namespaces=ns)),'old_export_appendix', '附录C 结果表导出完整源程序' in t,'new_plot_appendix','附录C 绘图完整源程序' in t)
print('TOC page2:\n',pdf[1].get_text())
