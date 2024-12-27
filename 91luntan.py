import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re

# 设置初始tid和结尾tid
start_tid = 721000  # 初始tid
end_tid = 721600  # 结尾tid

# 自定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}

# 初始化总计数
total_saved = 0

# 遍历从 start_tid 到 end_tid 的页面
for tid in range(start_tid, end_tid + 1):
    # 构建当前页面的URL
    url = f"https://t1129.btc760.com/viewthread.php?tid={tid}"

    # 请求网页内容
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析页面内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取网页标题
        page_title = soup.title.string.strip() if soup.title else "untitled"

        # 去除标题中 " - " 后面的部分
        page_title = page_title.split(' - ')[0]

        # 清理标题中的非法字符
        page_title = re.sub(r'[<>:"/\\|?*]', '_', page_title)

        # 查找所有 href="attachment.php?aid=..." 的链接
        attachment_links = soup.find_all('a', href=True)

        # 初始化该页面的计数器
        page_saved = 0

        # 遍历所有找到的链接
        for link in attachment_links:
            href = link['href']

            # 如果 href 包含 "attachment.php?aid="
            if "attachment.php?aid=" in href:
                # 构建完整的下载链接
                download_url = urljoin(url, href)

                # 请求附件内容
                file_response = requests.get(download_url, headers=headers)

                # 检查请求是否成功
                if file_response.status_code == 200:
                    # 构造文件名：使用 tid 参数、清理后的页面标题和递增数字
                    file_name = f"{tid}_{page_title}_{page_saved + 1}.jpg"  # 你可以根据实际文件类型调整扩展名

                    # 创建保存文件的文件夹
                    os.makedirs('91luntan_pic', exist_ok=True)
                    # 保存文件
                    file_path = os.path.join('91luntan_pic', file_name)
                    with open(file_path, 'wb') as f:
                        f.write(file_response.content)
                    print(f"附件 {file_name} 已保存！")

                    # 增加页面保存的计数
                    page_saved += 1
                    total_saved += 1
                else:
                    print(f"无法下载附件: {download_url}")

        # 输出当前网址完成情况
        print(f"网址 {url} 完成情况：{page_saved} 张图片已保存，总数量：{total_saved} 张图片")
    else:
        print(f"网页请求失败，状态码: {response.status_code}，tid: {tid}")

# 输出全部爬取情况
print(f"\n全部爬取完成，共保存 {total_saved} 张图片。")
