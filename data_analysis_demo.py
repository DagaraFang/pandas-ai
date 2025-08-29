"""
使用Ollama本地模型进行数据分析

这个示例展示如何使用Ollama的CodeLlama模型来分析数据并生成图表
"""
import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib

# 设置中文字体支持
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

class OllamaLLM:
    """简单的Ollama LLM包装器"""
    
    def __init__(self, model: str = "codellama:7b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
    
    def generate(self, prompt: str) -> str:
        """生成回复"""
        url = f"{self.base_url}/api/generate"
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=data, timeout=60)
            if response.status_code == 200:
                return response.json().get('response', '')
            else:
                return f"错误: {response.status_code}"
        except Exception as e:
            return f"请求失败: {e}"


def analyze_sales_data():
    """分析销售数据示例"""
    print("📊 开始数据分析...")
    
    # 创建示例数据
    data = {
        '销售员': ['张三', '李四', '王五', '赵六', '钱七'],
        '销售额': [10000, 15000, 8000, 12000, 9000],
        '地区': ['北京', '上海', '广州', '深圳', '杭州'],
        '产品': ['笔记本', '台式机', '平板', '手机', '耳机']
    }
    
    df = pd.DataFrame(data)
    print("✅ 示例数据创建成功：")
    print(df)
    print("\n🔍 正在分析数据...")
    
    # 创建LLM实例
    llm = OllamaLLM()
    
    # 生成分析提示
    prompt = f"""
你是一个专业的数据分析师，我将提供给你一个销售数据表格，你需要分析这些数据并回答以下问题：
1. 哪个销售员的销售额最高？
2. 每个地区的平均销售额是多少？
3. 哪种产品的总销售额最高？
4. 总结数据的主要特点

数据表格：
{df.to_string()}

请用中文回答，并提供详细的分析过程。
"""
    
    # 获取分析结果
    result = llm.generate(prompt)
    
    print("\n🤖 AI分析结果：")
    print(result)
    
    # 生成图表
    print("\n📈 正在生成图表...")
    generate_charts(df)
    
    return df


def generate_charts(df):
    """生成数据分析图表"""
    # 创建图表窗口
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('销售数据分析图表', fontsize=16, fontweight='bold')
    
    # 1. 销售员销售额柱状图
    axes[0, 0].bar(df['销售员'], df['销售额'], color='skyblue', edgecolor='navy')
    axes[0, 0].set_title('销售员销售额对比', fontweight='bold')
    axes[0, 0].set_xlabel('销售员')
    axes[0, 0].set_ylabel('销售额（元）')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # 在柱子上显示数值
    for i, v in enumerate(df['销售额']):
        axes[0, 0].text(i, v + 200, str(v), ha='center', va='bottom')
    
    # 2. 地区销售额饼状图
    region_sales = df.groupby('地区')['销售额'].sum()
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
    wedges, texts, autotexts = axes[0, 1].pie(region_sales.values, labels=region_sales.index, 
                                              autopct='%1.1f%%', colors=colors, startangle=90)
    axes[0, 1].set_title('各地区销售额占比', fontweight='bold')
    
    # 3. 产品销售额水平柱状图
    product_sales = df.groupby('产品')['销售额'].sum().sort_values(ascending=True)
    axes[1, 0].barh(product_sales.index, product_sales.values, color='lightgreen', edgecolor='darkgreen')
    axes[1, 0].set_title('产品销售额排名', fontweight='bold')
    axes[1, 0].set_xlabel('销售额（元）')
    axes[1, 0].set_ylabel('产品')
    
    # 在条形图上显示数值
    for i, v in enumerate(product_sales.values):
        axes[1, 0].text(v + 100, i, str(v), ha='left', va='center')
    
    # 4. 销售额趋势线图（按索引排序）
    sorted_data = df.sort_values('销售额')
    axes[1, 1].plot(range(len(sorted_data)), sorted_data['销售额'], 
                    marker='o', linewidth=2, markersize=8, color='red')
    axes[1, 1].set_title('销售额趋势分析', fontweight='bold')
    axes[1, 1].set_xlabel('排名顺序')
    axes[1, 1].set_ylabel('销售额（元）')
    axes[1, 1].grid(True, alpha=0.3)
    
    # 标记数据点
    for i, (idx, row) in enumerate(sorted_data.iterrows()):
        axes[1, 1].annotate(f"{row['销售员']}\n{row['销售额']}", 
                           (i, row['销售额']), 
                           textcoords="offset points", 
                           xytext=(0,10), ha='center')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    chart_filename = 'sales_analysis_charts.png'
    plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
    print(f"✅ 图表已保存为: {chart_filename}")
    
    # 显示图表
    plt.show()
    
    # 生成数据总结
    print("\n📈 数据分析总结:")
    print(f"• 最高销售额: {df['销售员'][df['销售额'].idxmax()]} - {df['销售额'].max():,}元")
    print(f"• 最低销售额: {df['销售员'][df['销售额'].idxmin()]} - {df['销售额'].min():,}元")
    print(f"• 平均销售额: {df['销售额'].mean():,.0f}元")
    print(f"• 总销售额: {df['销售额'].sum():,}元")
    print(f"• 销售额标准差: {df['销售额'].std():,.0f}元")


def main():
    """主函数"""
    print("🚀 开始数据分析演示")
    print("="*50)
    
    # 运行分析
    df = analyze_sales_data()
    
    print("\n" + "="*50)
    print("🎯 演示完成！你可以：")
    print("1. 查看生成的图表文件: sales_analysis_charts.png")
    print("2. 修改示例数据，测试不同的分析场景")
    print("3. 添加更多复杂的分析问题")
    print("4. 将这个分析器集成到你的项目中")
    print("5. 尝试其他模型，如llama2或mistral")
    print("\n📈 生成的图表包括：")
    print("• 销售员销售额对比柱状图")
    print("• 各地区销售额占比饼状图")
    print("• 产品销售额排名水平柱状图")
    print("• 销售额趋势分析线图")

if __name__ == "__main__":
    main()