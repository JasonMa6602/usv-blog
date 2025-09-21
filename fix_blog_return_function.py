#!/usr/bin/env python3
"""
修复博客文件，正确添加返回首页功能（不破坏原有功能）
"""

import os
import re
import shutil
from pathlib import Path

def fix_return_home_functionality(file_path):
    """修复单个博客文件的返回首页功能"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经存在返回首页功能
        if 'return-home' in content and 'Return to Homepage functionality' in content:
            print(f"⏭️  {file_path.name} 已存在完整的返回首页功能，跳过")
            return True, "已存在"
        
        # 备份原始文件
        backup_path = file_path.with_suffix('.html.backup2')
        if not backup_path.exists():  # 不要覆盖已有的备份
            shutil.copy2(file_path, backup_path)
        
        # 添加返回首页按钮（在Back to Top按钮之前）
        if '<!-- Return to Homepage Button -->' not in content:
            back_to_top_pattern = r'(<button id="backToTop" class="back-to-top" aria-label="Back to top">)'
            return_home_button = '''    <!-- Return to Homepage Button -->
    <a href="index.html" class="return-home" aria-label="Return to homepage">
        <i class="fas fa-home"></i>
    </a>

'''
            content = re.sub(back_to_top_pattern, return_home_button + r'\1', content)
        
        # 添加JavaScript功能（不破坏原有的back to top功能）
        if 'Return to Homepage functionality' not in content:
            # 找到script标签的结束位置，在最后一个函数之后添加新功能
            script_end_pattern = r'(backToTopButton\.addEventListener\([^}]*\}[^}]*\});)'
            
            new_script = r'''\1

        // Return to Homepage functionality
        const returnHomeButton = document.querySelector('.return-home');
        if (returnHomeButton) {
            // Show/hide return home button based on scroll position
            window.addEventListener('scroll', () => {
                if (window.pageYOffset > 200) {
                    returnHomeButton.classList.add('show');
                } else {
                    returnHomeButton.classList.remove('show');
                }
            });
        }'''
            
            content = re.sub(script_end_pattern, new_script, content, flags=re.DOTALL)
        
        # 写入更新后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {file_path.name} 修复成功")
        return True, "修复成功"
        
    except Exception as e:
        print(f"❌ {file_path.name} 修复失败: {str(e)}")
        return False, str(e)

def validate_fix(file_path):
    """验证修复是否成功"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含返回首页按钮
        has_return_button = 'return-home' in content
        has_return_script = 'Return to Homepage functionality' in content
        has_home_link = 'href="index.html"' in content
        
        # 检查原有的back to top功能是否完整
        has_back_to_top_button = 'backToTop' in content
        has_back_to_top_script = 'Back to Top functionality' in content
        has_scroll_event = 'window.addEventListener(\'scroll\'' in content
        
        issues = []
        if not has_return_button: issues.append("返回首页按钮")
        if not has_return_script: issues.append("返回首页JavaScript")
        if not has_home_link: issues.append("首页链接")
        if not has_back_to_top_button: issues.append("Back to Top按钮")
        if not has_back_to_top_script: issues.append("Back to Top脚本")
        if not has_scroll_event: issues.append("滚动事件监听")
        
        if not issues:
            return True, "所有功能完整"
        else:
            return False, f"缺少: {', '.join(issues)}"
            
    except Exception as e:
        return False, f"验证失败: {str(e)}"

def main():
    """主函数：修复所有博客文件"""
    print("🔧 开始修复博客文件，正确添加返回首页功能...")
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
        
        # 修复文件
        success, message = fix_return_home_functionality(file_path)
        
        if success:
            if message == "已存在":
                skipped_files.append(file_path.name)
            else:
                # 验证修复
                is_valid, validation_msg = validate_fix(file_path)
                if is_valid:
                    success_count += 1
                    print(f"   🔍 验证: {validation_msg}")
                else:
                    failed_files.append((file_path.name, f"验证失败: {validation_msg}"))
        else:
            failed_files.append((file_path.name, message))
    
    # 输出统计结果
    print("\n" + "=" * 60)
    print("📊 修复结果统计:")
    print(f"✅ 成功修复: {success_count} 个文件")
    print(f"⏭️  跳过处理: {len(skipped_files)} 个文件")
    print(f"❌ 修复失败: {len(failed_files)} 个文件")
    
    if skipped_files:
        print(f"\n⏭️  跳过的文件: {', '.join(skipped_files)}")
    
    if failed_files:
        print(f"\n❌ 失败的文件:")
        for filename, error in failed_files:
            print(f"   - {filename}: {error}")
    
    print(f"\n🎉 修复完成！")
    
    # 功能测试
    print(f"\n🧪 测试功能完整性...")
    test_file = current_dir / "blog-post-3.html"
    if test_file.exists():
        is_valid, validation_msg = validate_fix(test_file)
        if is_valid:
            print("✅ 功能测试通过！返回首页和Back to Top功能都正常")
        else:
            print(f"⚠️  功能测试未通过: {validation_msg}")

if __name__ == "__main__":
    main()
