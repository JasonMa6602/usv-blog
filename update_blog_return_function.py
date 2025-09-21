#!/usr/bin/env python3
"""
批量更新博客文件，添加返回首页功能
脚本会处理所有 blog-post-*.html 文件，添加返回首页按钮和相应功能
"""

import os
import re
import shutil
from pathlib import Path

def add_return_home_functionality(file_path):
    """为单个博客文件添加返回首页功能"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经存在返回首页功能
        if 'return-home' in content:
            print(f"⏭️  {file_path.name} 已存在返回首页功能，跳过")
            return True, "已存在"
        
        # 备份原始文件
        backup_path = file_path.with_suffix('.html.backup')
        shutil.copy2(file_path, backup_path)
        
        # 添加返回首页按钮（在Back to Top按钮之前）
        back_to_top_pattern = r'(<button id="backToTop" class="back-to-top" aria-label="Back to top">)'
        return_home_button = '''    <!-- Return to Homepage Button -->
    <a href="index.html" class="return-home" aria-label="Return to homepage">
        <i class="fas fa-home"></i>
    </a>

'''
        
        content = re.sub(back_to_top_pattern, return_home_button + r'\1', content)
        
        # 更新JavaScript功能
        old_script_pattern = r'(function toggleMenu\(\) \{[^}]*\}[^}]*\})'
        new_script = r'''\1

        // Return to Homepage functionality
        const returnHomeButton = document.querySelector('.return-home');
        
        // Show/hide return home button based on scroll position
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 200) {
                returnHomeButton.classList.add('show');
            } else {
                returnHomeButton.classList.remove('show');
            }
        });'''
        
        content = re.sub(old_script_pattern, new_script, content, flags=re.DOTALL)
        
        # 写入更新后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {file_path.name} 更新成功")
        return True, "更新成功"
        
    except Exception as e:
        print(f"❌ {file_path.name} 更新失败: {str(e)}")
        return False, str(e)

def validate_update(file_path):
    """验证文件更新是否成功"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含返回首页按钮
        has_return_button = 'return-home' in content
        has_return_script = 'Return to Homepage functionality' in content
        has_home_link = 'href="index.html"' in content
        
        if has_return_button and has_return_script and has_home_link:
            return True, "验证通过"
        else:
            missing = []
            if not has_return_button: missing.append("返回首页按钮")
            if not has_return_script: missing.append("JavaScript功能")
            if not has_home_link: missing.append("首页链接")
            return False, f"缺少: {', '.join(missing)}"
            
    except Exception as e:
        return False, f"验证失败: {str(e)}"

def main():
    """主函数：批量处理所有博客文件"""
    print("🚀 开始批量更新博客文件，添加返回首页功能...")
    print("=" * 60)
    
    # 获取当前目录
    current_dir = Path(".")
    
    # 查找所有 blog-post-*.html 文件
    blog_files = list(current_dir.glob("blog-post-*.html"))
    
    if not blog_files:
        print("❌ 未找到博客文件")
        return
    
    print(f"📁 找到 {len(blog_files)} 个博客文件")
    
    # 处理结果统计
    success_count = 0
    failed_files = []
    skipped_files = []
    
    for file_path in blog_files:
        print(f"\n📄 处理: {file_path.name}")
        
        # 更新文件
        success, message = add_return_home_functionality(file_path)
        
        if success:
            if message == "已存在":
                skipped_files.append(file_path.name)
            else:
                # 验证更新
                is_valid, validation_msg = validate_update(file_path)
                if is_valid:
                    success_count += 1
                    print(f"   🔍 验证: {validation_msg}")
                else:
                    failed_files.append((file_path.name, f"验证失败: {validation_msg}"))
        else:
            failed_files.append((file_path.name, message))
    
    # 输出统计结果
    print("\n" + "=" * 60)
    print("📊 处理结果统计:")
    print(f"✅ 成功更新: {success_count} 个文件")
    print(f"⏭️  跳过处理: {len(skipped_files)} 个文件")
    print(f"❌ 处理失败: {len(failed_files)} 个文件")
    
    if skipped_files:
        print(f"\n⏭️  跳过的文件: {', '.join(skipped_files)}")
    
    if failed_files:
        print(f"\n❌ 失败的文件:")
        for filename, error in failed_files:
            print(f"   - {filename}: {error}")
    
    # 清理备份文件（可选）
    print(f"\n🧹 清理备份文件...")
    backup_files = list(current_dir.glob("blog-post-*.html.backup"))
    if backup_files:
        print(f"   找到 {len(backup_files)} 个备份文件")
        response = input("是否删除备份文件? (y/n): ").lower()
        if response == 'y':
            for backup in backup_files:
                try:
                    os.remove(backup)
                    print(f"   🗑️  删除: {backup.name}")
                except Exception as e:
                    print(f"   ❌ 删除失败 {backup.name}: {str(e)}")
    
    print(f"\n🎉 批量更新完成！")
    
    # 测试功能
    print(f"\n🧪 测试返回首页功能...")
    test_file = current_dir / "blog-post-1.html"
    if test_file.exists():
        is_valid, validation_msg = validate_update(test_file)
        if is_valid:
            print("✅ 功能测试通过！返回首页按钮已正确添加")
        else:
            print(f"⚠️  功能测试未通过: {validation_msg}")

if __name__ == "__main__":
    main()
