#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF简历压缩脚本
将多页简历压缩到单页，保持紧凑排版
"""

import os
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pdfplumber


def compress_resume(input_pdf, output_pdf):
    """
    将PDF简历压缩到单页

    Args:
        input_pdf: 输入PDF路径
        output_pdf: 输出PDF路径
    """
    print(f"正在处理: {input_pdf}")

    # 检查输入文件
    if not os.path.exists(input_pdf):
        print(f"错误: 文件 {input_pdf} 不存在")
        return False

    # 读取原始PDF
    with pdfplumber.open(input_pdf) as pdf:
        print(f"原始页数: {len(pdf.pages)}")

        # 提取所有文本内容
        all_text = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)

    # 创建新的紧凑版PDF
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        rightMargin=0.5*cm,
        leftMargin=0.5*cm,
        topMargin=0.5*cm,
        bottomMargin=0.5*cm
    )

    # 设置样式 - 更紧凑
    styles = getSampleStyleSheet()

    # 自定义紧凑样式
    compact_style = ParagraphStyle(
        'Compact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        spaceAfter=2,
        leading=10,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0
    )

    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        spaceAfter=6,
        spaceBefore=6,
        leading=18
    )

    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        spaceAfter=4,
        spaceBefore=4,
        leading=12
    )

    # 构建内容
    story = []

    # 处理文本内容
    for page_text in all_text:
        lines = page_text.split('\n')
        for line in lines:
            line = line.strip()
            if line:
                # 尝试识别标题行
                if any(keyword in line for keyword in ['教育经历', '工作经历', '项目经验', '技能特长', '自我评价', '联系方式']):
                    story.append(Paragraph(line, heading_style))
                elif line.isupper() or len(line) < 30 and ':' in line:
                    # 可能是小标题
                    story.append(Paragraph(line, heading_style))
                else:
                    story.append(Paragraph(line, compact_style))
                story.append(Spacer(1, 0.1*cm))

    # 生成PDF
    try:
        doc.build(story)
        print(f"✓ 成功生成紧凑版简历: {output_pdf}")
        print(f"  输出文件: {output_pdf}")

        # 验证输出
        with open(output_pdf, 'rb') as f:
            output_reader = PdfReader(f)
            print(f"  输出页数: {len(output_reader.pages)}")

        return True

    except Exception as e:
        print(f"错误: 生成PDF失败 - {str(e)}")
        return False


def main():
    """主函数"""
    input_pdf = "d:/毕业设计/我的简历最终.pdf"
    output_pdf = "d:/毕业设计/我的简历_紧凑版.pdf"

    print("=" * 60)
    print("PDF简历压缩工具")
    print("=" * 60)

    success = compress_resume(input_pdf, output_pdf)

    print("=" * 60)
    if success:
        print("✓ 处理完成!")
    else:
        print("✗ 处理失败")
    print("=" * 60)


if __name__ == "__main__":
    main()
