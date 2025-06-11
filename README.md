运行detect_light_colors.py源文件，默认输入输出为：
    input_css_file = 'main.css'
    output_css_file = 'dark_main.css'
它将搜索同级目录下的input_css_file，将其所有可在css文件中修改的颜色，例如
#0c0c04;
rgba(54,57,74,0.54);
全部映射为相反的文件，输出在dark_main.css文件中，然后使用浏览器开发者工具替换网站对应css即可完成修改主题

Run the source file detect_light_colors.py, where the default input and output files are:

input_css_file = 'main.css'
output_css_file = 'dark_main.css'
It will search for the input_css_file in the same directory, and map all modifiable color values in the CSS file—such as

#0c0c04;

rgba(54, 57, 74, 0.54);

—to their dark counterparts, and output the result into the file dark_main.css. Then, use the browser's developer tools to replace the website's corresponding CSS file to complete the theme change.

![Screenshot 2025-06-11 235034](https://github.com/user-attachments/assets/c1159c41-9adc-45f5-b0e1-7c71f81f71bc)
![Screenshot 2025-06-12 001644](https://github.com/user-attachments/assets/82d4ec31-9345-4e98-9652-f9981109d7aa)
![image](https://github.com/user-attachments/assets/b3bd1cf7-f7fc-485e-be4a-f5eb1885fe3b)
