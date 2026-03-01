#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复Front Matter格式问题
"""

import os
import re

def fix_frontmatter(filepath):
    """修复单个文件的Front Matter"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式修复
    # 修复 draft: False -> draft: false
    content = re.sub(r'draft:\s*False', 'draft: false', content)
    content = re.sub(r'draft:\s*True', 'draft: true', content)
    
    # 修复标题中的冒号问题
    lines = content.split('\n')
    in_frontmatter = False
    frontmatter_lines = []
    body_lines = []
    
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
                frontmatter_lines.append(line)
            else:
                frontmatter_lines.append(line)
                body_lines = lines[i+1:]
                break
        elif in_frontmatter:
            frontmatter_lines.append(line)
    
    # 处理Front Matter行
    new_frontmatter = []
    for line in frontmatter_lines:
        if ': ' in line and not line.strip().startswith('---'):
            key, value = line.split(': ', 1)
            value = value.strip()
            
            # 特殊处理tags和categories（应该是YAML数组）
            if key in ['tags', 'categories']:
                # 如果是数组格式，保持原样
                if value.startswith('[') and value.endswith(']'):
                    # 已经是数组格式，不做修改
                    pass
                else:
                    # 转换为数组格式
                    line = f'{key}: [{value}]'
            else:
                # 如果值需要引号
                needs_quotes = False
                if value and not (value.startswith('"') and value.endswith('"')) and \
                   not (value.startswith("'") and value.endswith("'")):
                    if ':' in value or '(' in value or ')' in value or \
                       value.lower() in ['true', 'false', 'yes', 'no', 'on', 'off']:
                        needs_quotes = True
                
                if needs_quotes:
                    # 转义内部的双引号
                    value = value.replace('"', '\\"')
                    line = f'{key}: "{value}"'
        
        new_frontmatter.append(line)
    
    # 重新组合内容
    new_content = '\n'.join(new_frontmatter + body_lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    """主函数"""
    posts_dir = 'content/posts'
    
    if not os.path.exists(posts_dir):
        print(f"目录不存在: {posts_dir}")
        return
    
    fixed_count = 0
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(posts_dir, filename)
            try:
                if fix_frontmatter(filepath):
                    print(f"✅ 已修复: {filename}")
                    fixed_count += 1
            except Exception as e:
                print(f"❌ 修复失败 {filename}: {e}")
    
    print(f"\n修复完成！共修复 {fixed_count} 个文件")

if __name__ == "__main__":
    main()