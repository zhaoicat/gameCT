#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF to Markdown 转换器
使用PyPDF2提取PDF文本并格式化为Markdown
"""

import PyPDF2
import re
import sys
import os

def clean_text(text):
    """清理和格式化文本"""
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text)
    # 移除页眉页脚等常见模式
    text = re.sub(r'第\s*\d+\s*页.*?共\s*\d+\s*页', '', text)
    text = re.sub(r'\d+\s*$', '', text, flags=re.MULTILINE)
    return text.strip()

def format_as_markdown(text, title=""):
    """将文本格式化为Markdown"""
    lines = text.split('\n')
    markdown_lines = []
    
    if title:
        markdown_lines.append(f"# {title}")
        markdown_lines.append("")
    
    current_paragraph = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_paragraph:
                markdown_lines.append(' '.join(current_paragraph))
                markdown_lines.append("")
                current_paragraph = []
            continue
            
        # 检测可能的标题
        if (len(line) < 100 and 
            (line.endswith('：') or line.endswith(':') or 
             any(keyword in line for keyword in ['摘要', '关键词', '引言', '方法', '结果', '讨论', '结论', '参考文献']))):
            if current_paragraph:
                markdown_lines.append(' '.join(current_paragraph))
                markdown_lines.append("")
                current_paragraph = []
            markdown_lines.append(f"## {line}")
            markdown_lines.append("")
        else:
            current_paragraph.append(line)
    
    # 添加最后一个段落
    if current_paragraph:
        markdown_lines.append(' '.join(current_paragraph))
    
    return '\n'.join(markdown_lines)

def pdf_to_markdown(pdf_path, output_path=None):
    """将PDF转换为Markdown"""
    if not os.path.exists(pdf_path):
        print(f"错误: 文件 {pdf_path} 不存在")
        return False
    
    if output_path is None:
        output_path = os.path.splitext(pdf_path)[0] + '.md'
    
    try:
        with open(pdf_path, 'rb') as file:
            # 创建PDF阅读器对象
            pdf_reader = PyPDF2.PdfReader(file)
            
            # 提取所有页面的文本
            full_text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                full_text += text + "\n"
            
            # 清理文本
            cleaned_text = clean_text(full_text)
            
            # 从文件名获取标题
            title = os.path.splitext(os.path.basename(pdf_path))[0]
            title = title.replace('_', ' ')  # 替换下划线为空格
            
            # 格式化为Markdown
            markdown_content = format_as_markdown(cleaned_text, title)
            
            # 写入Markdown文件
            with open(output_path, 'w', encoding='utf-8') as md_file:
                md_file.write(markdown_content)
            
            print(f"✅ 转换成功!")
            print(f"📄 输入文件: {pdf_path}")
            print(f"📝 输出文件: {output_path}")
            print(f"📊 总页数: {len(pdf_reader.pages)}")
            print(f"📈 文本长度: {len(cleaned_text)} 字符")
            
            return True
            
    except Exception as e:
        print(f"❌ 转换失败: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
    else:
        pdf_file = "2_马雪峰_重复经颅磁刺激对自然态下吸烟成瘾者神经同步性的影响.pdf"
    
    success = pdf_to_markdown(pdf_file)
    sys.exit(0 if success else 1) 