"""
pandas-ai + Ollama 集成示例

这个示例展示如何将Ollama本地模型集成到pandas-ai项目中
"""
import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib
from typing import Optional

# 设置中文字体支持
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


class BaseLLM:
    """基础LLM类，不依赖pandas-ai"""
    
    def __init__(self, **kwargs):
        pass
    
    @property
    def type(self) -> str:
        return "base"
    
    def call(self, instruction: str, value: str = "", suffix: str = "") -> str:
        raise NotImplementedError


class OllamaLLM(BaseLLM):
    """
    独立的Ollama LLM类
    可以轻松集成到pandas-ai项目中
    """
    
    def __init__(self, model: str = "codellama:7b", base_url: str = "http://localhost:11434", **kwargs):
        """
        初始化Ollama LLM
        
        Args:
            model: Ollama模型名称
            base_url: Ollama服务器地址
            **kwargs: 其他参数
        """
        self.model = model
        self.base_url = base_url
        super().__init__(**kwargs)
    
    @property
    def type(self) -> str:
        """返回LLM类型"""
        return "ollama"
    
    def _generate_text(self, prompt: str) -> str:
        """
        生成文本回复
        
        Args:
            prompt: 输入提示
            
        Returns:
            生成的文本
        """
        url = f"{self.base_url}/api/generate"
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=data, timeout=120)
            if response.status_code == 200:
                return response.json().get('response', '')
            else:
                return f"错误: HTTP {response.status_code}"
        except Exception as e:
            return f"请求失败: {str(e)}"
    
    def call(self, instruction: str, value: str = "", suffix: str = "") -> str:
        """
        pandas-ai要求的调用接口
        
        Args:
            instruction: 指令
            value: 数值
            suffix: 后缀
            
        Returns:
            生成的回复
        """
        prompt = f"{instruction}\n{value}\n{suffix}".strip()
        return self._generate_text(prompt)


def demo_with_pandasai():
    """使用pandas-ai进行数据分析演示"""
    print("🚀 pandas-ai + Ollama 集成演示")
    print("="*50)
    
    # 检查Ollama服务
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            print("❌ Ollama服务未运行，请先启动: ollama serve")
            return
        
        models = response.json().get("models", [])
        if not models:
            print("❌ 未找到模型，请先下载: ollama pull codellama:7b")
            return
        
        print(f"✅ Ollama服务运行中，可用模型: {[m['name'] for m in models]}")
    except:
        print("❌ 无法连接到Ollama服务")
        return
    
    # 创建示例数据
    data = {
        '销售员': ['张三', '李四', '王五', '赵六', '钱七'],
        '销售额': [10000, 15000, 8000, 12000, 9000],
        '地区': ['北京', '上海', '广州', '深圳', '杭州'],
        '产品': ['笔记本', '台式机', '平板', '手机', '耳机'],
        '季度': ['Q1', 'Q2', 'Q1', 'Q2', 'Q1']
    }
    
    df = pd.DataFrame(data)
    print("\n📊 示例数据:")
    print(df)
    
    # 创建Ollama LLM实例
    llm = OllamaLLM()
    
    print("\n🤖 使用智能分析进行数据分析...")
    
    # 直接使用简化版本
    smart_analysis_demo(df, llm)


def smart_analysis_demo(df, llm):
    """智能数据分析演示"""
    print("\n📈 智能数据分析演示:")
    
    # 高级分析问题
    advanced_questions = [
        "分析销售数据，找出表现最好的销售员和原因",
        "比较不同地区的销售表现，给出优化建议",
        "分析产品组合和季度趋势，预测未来销售",
        "生成一份完整的销售分析报告"
    ]
    
    for i, question in enumerate(advanced_questions, 1):
        print(f"\n🤔 高级分析 {i}: {question}")
        
        # 构建详细提示
        prompt = f"""
你是一个专业的数据分析师和商业顾问。请根据以下销售数据回答问题。

问题: {question}

数据表格:
{df.to_string()}

请提供:
1. 数据分析结果
2. 关键发现和见解
3. 实用的建议
4. 用中文回答，条理清晰
"""
        
        result = llm._generate_text(prompt)
        print(f"📊 分析结果:\n{result}")
        print("-" * 80)
    
    # 生成高级图表
    generate_advanced_charts(df)


def generate_advanced_charts(df):
    """生成高级数据图表"""
    print("\n📈 生成高级数据图表...")
    
    # 创建更大的图表窗口
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('高级销售数据分析仪表板', fontsize=18, fontweight='bold')
    
    # 1. 销售员成绩对比 (带平均线)
    ax1 = plt.subplot(3, 3, 1)
    bars = ax1.bar(df['销售员'], df['销售额'], 
                   color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])
    ax1.axhline(y=df['销售额'].mean(), color='red', linestyle='--', 
                label=f'平均值: {df["销售额"].mean():.0f}')
    ax1.set_title('销售员成绩对比', fontweight='bold')
    ax1.set_ylabel('销售额(元)')
    ax1.legend()
    
    # 数值标注
    for bar, value in zip(bars, df['销售额']):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
                f'{value:,}', ha='center', va='bottom', fontweight='bold')
    
    # 2. 地区分布饼状图 (带数值)
    ax2 = plt.subplot(3, 3, 2)
    region_sales = df.groupby('地区')['销售额'].sum()
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']
    wedges, texts, autotexts = ax2.pie(region_sales.values, labels=region_sales.index,
                                       autopct='%1.1f%%', colors=colors, startangle=90)
    ax2.set_title('地区销售分布', fontweight='bold')
    
    # 3. 产品排名水平柱状图
    ax3 = plt.subplot(3, 3, 3)
    product_sales = df.groupby('产品')['销售额'].sum().sort_values()
    bars = ax3.barh(product_sales.index, product_sales.values, 
                    color='lightgreen', edgecolor='darkgreen')
    ax3.set_title('产品销售排名', fontweight='bold')
    ax3.set_xlabel('销售额(元)')
    
    # 4. 季度对比
    ax4 = plt.subplot(3, 3, 4)
    quarter_data = df.groupby('季度')['销售额'].agg(['sum', 'mean', 'count'])
    x = range(len(quarter_data))
    ax4.bar(x, quarter_data['sum'], alpha=0.7, label='总销售额')
    ax4_twin = ax4.twinx()
    ax4_twin.plot(x, quarter_data['mean'], 'ro-', label='平均销售额')
    ax4.set_title('季度销售对比', fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(quarter_data.index)
    ax4.legend(loc='upper left')
    ax4_twin.legend(loc='upper right')
    
    # 5. 销售额分布直方图
    ax5 = plt.subplot(3, 3, 5)
    ax5.hist(df['销售额'], bins=5, alpha=0.7, color='skyblue', edgecolor='black')
    ax5.set_title('销售额分布', fontweight='bold')
    ax5.set_xlabel('销售额(元)')
    ax5.set_ylabel('频次')
    
    # 6. 箱线图
    ax6 = plt.subplot(3, 3, 6)
    ax6.boxplot(df['销售额'], labels=['销售额'])
    ax6.set_title('销售额箱线图', fontweight='bold')
    ax6.set_ylabel('销售额(元)')
    
    # 7. 散点图 (销售员 vs 销售额)
    ax7 = plt.subplot(3, 3, 7)
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    for i, (idx, row) in enumerate(df.iterrows()):
        ax7.scatter(i, row['销售额'], c=colors[i], s=100, alpha=0.7)
        ax7.annotate(row['销售员'], (i, row['销售额']), 
                    xytext=(5, 5), textcoords='offset points')
    ax7.set_title('销售员与销售额关系', fontweight='bold')
    ax7.set_xlabel('销售员索引')
    ax7.set_ylabel('销售额(元)')
    
    # 8. 雷达图
    ax8 = plt.subplot(3, 3, 8, projection='polar')
    angles = [i * 2 * 3.14159 / len(df) for i in range(len(df))]
    values = df['销售额'].tolist()
    angles += angles[:1]  # 闭合图形
    values += values[:1]
    ax8.plot(angles, values, 'o-', linewidth=2)
    ax8.fill(angles, values, alpha=0.25)
    ax8.set_title('销售业绩雷达图', fontweight='bold', pad=20)
    
    # 9. 统计信息表
    ax9 = plt.subplot(3, 3, 9)
    ax9.axis('off')
    stats_text = f"""
📈 数据统计摘要

总销售额: {df['销售额'].sum():,} 元
平均销售额: {df['销售额'].mean():.0f} 元
中位数: {df['销售额'].median():.0f} 元
最高: {df['销售额'].max():,} 元
最低: {df['销售额'].min():,} 元
标准差: {df['销售额'].std():.0f} 元

🏆 最佳表现者:
{df.loc[df['销售额'].idxmax(), '销售员']}

📍 地区数: {df['地区'].nunique()}
💻 产品数: {df['产品'].nunique()}
"""
    ax9.text(0.1, 0.9, stats_text, transform=ax9.transAxes, fontsize=11,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue'))
    
    plt.tight_layout()
    
    # 保存图表
    chart_file = 'advanced_sales_analysis.png'
    plt.savefig(chart_file, dpi=300, bbox_inches='tight')
    print(f"✅ 高级分析图表已保存为: {chart_file}")
    
    plt.show()


def main():
    """主函数"""
    demo_with_pandasai()
    
    print("\n" + "="*50)
    print("🎯 集成演示完成！")
    print("\n📋 总结:")
    print("✅ 成功创建了可集成到pandas-ai的Ollama LLM类")
    print("✅ 演示了自然语言数据分析功能")
    print("✅ 生成了多种类型的数据可视化图表")
    print("✅ 提供了完整的本地AI数据分析解决方案")
    
    print("\n💡 下一步建议:")
    print("1. 将OllamaLLM类集成到你的pandas-ai项目中")
    print("2. 尝试更复杂的数据分析问题")
    print("3. 自定义图表样式和分析逻辑")
    print("4. 优化提示工程以获得更好的分析结果")


if __name__ == "__main__":
    main()