"""
智能文件数据分析器

支持从指定路径读取各种格式的数据文件，并进行AI驱动的数据分析和可视化
"""
import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any, List

# 设置中文字体支持
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


class FileDataAnalyzer:
    """智能文件数据分析器"""
    
    def __init__(self, ollama_model: str = "codellama:7b", ollama_url: str = "http://localhost:11434"):
        self.model = ollama_model
        self.ollama_url = ollama_url
        self.supported_formats = {
            '.csv': self._read_csv,
            '.xlsx': self._read_excel,
            '.xls': self._read_excel,
            '.json': self._read_json,
            '.parquet': self._read_parquet,
            '.tsv': self._read_tsv,
            '.txt': self._read_txt
        }
        
    def _read_csv(self, file_path: str, **kwargs) -> pd.DataFrame:
        """读取CSV文件"""
        return pd.read_csv(file_path, **kwargs)
    
    def _read_excel(self, file_path: str, **kwargs) -> pd.DataFrame:
        """读取Excel文件"""
        return pd.read_excel(file_path, **kwargs)
    
    def _read_json(self, file_path: str, **kwargs) -> pd.DataFrame:
        """读取JSON文件"""
        return pd.read_json(file_path, **kwargs)
    
    def _read_parquet(self, file_path: str, **kwargs) -> pd.DataFrame:
        """读取Parquet文件"""
        return pd.read_parquet(file_path, **kwargs)
    
    def _read_tsv(self, file_path: str, **kwargs) -> pd.DataFrame:
        """读取TSV文件"""
        return pd.read_csv(file_path, sep='\t', **kwargs)
    
    def _read_txt(self, file_path: str, **kwargs) -> pd.DataFrame:
        """读取TXT文件（假设是分隔符分隔的数据）"""
        # 尝试不同的分隔符
        separators = [',', '\t', ';', '|', ' ']
        for sep in separators:
            try:
                df = pd.read_csv(file_path, sep=sep, **kwargs)
                if len(df.columns) > 1:
                    return df
            except:
                continue
        # 如果都失败，按行读取
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return pd.DataFrame({'content': [line.strip() for line in lines]})
    
    def read_file(self, file_path: str, **kwargs) -> Optional[pd.DataFrame]:
        """
        从指定路径读取数据文件
        
        Args:
            file_path: 文件路径
            **kwargs: 传递给读取函数的额外参数
            
        Returns:
            DataFrame或None
        """
        file_path = Path(file_path)
        
        # 检查文件是否存在
        if not file_path.exists():
            print(f"❌ 文件不存在: {file_path}")
            return None
        
        # 获取文件扩展名
        file_ext = file_path.suffix.lower()
        
        # 检查是否支持该格式
        if file_ext not in self.supported_formats:
            print(f"❌ 不支持的文件格式: {file_ext}")
            print(f"支持的格式: {list(self.supported_formats.keys())}")
            return None
        
        try:
            print(f"📖 正在读取文件: {file_path}")
            df = self.supported_formats[file_ext](str(file_path), **kwargs)
            print(f"✅ 成功读取数据，形状: {df.shape}")
            return df
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            return None
    
    def list_directory(self, dir_path: str) -> List[str]:
        """
        列出目录下的所有支持的数据文件
        
        Args:
            dir_path: 目录路径
            
        Returns:
            文件路径列表
        """
        dir_path = Path(dir_path)
        if not dir_path.exists():
            print(f"❌ 目录不存在: {dir_path}")
            return []
        
        files = []
        for file_path in dir_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                files.append(str(file_path))
        
        return sorted(files)
    
    def chat_with_llm(self, prompt: str) -> str:
        """与LLM对话"""
        url = f"{self.ollama_url}/api/generate"
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
    
    def analyze_file(self, file_path: str, questions: List[str] = None, **read_kwargs) -> Dict[str, Any]:
        """
        分析指定文件的数据
        
        Args:
            file_path: 文件路径
            questions: 分析问题列表
            **read_kwargs: 读取文件的额外参数
            
        Returns:
            分析结果字典
        """
        # 读取数据
        df = self.read_file(file_path, **read_kwargs)
        if df is None:
            return {"error": "无法读取文件"}
        
        # 默认问题
        if questions is None:
            questions = [
                "请分析这个数据集的基本统计信息",
                "数据中有哪些主要的趋势和模式？",
                "有什么异常值或需要注意的数据质量问题吗？",
                "基于这些数据，你有什么业务洞察和建议？"
            ]
        
        # 数据预览
        print(f"\n📊 数据预览:")
        print(f"文件: {file_path}")
        print(f"形状: {df.shape}")
        print(f"列名: {list(df.columns)}")
        print("\n前5行数据:")
        print(df.head())
        
        # 数据类型信息
        print(f"\n📋 数据类型:")
        print(df.dtypes)
        
        # 基本统计
        print(f"\n📈 基本统计:")
        print(df.describe())
        
        # AI分析
        results = {"file_info": {
            "path": str(file_path),
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict()
        }, "analyses": []}
        
        for i, question in enumerate(questions, 1):
            print(f"\n🤔 分析问题 {i}: {question}")
            
            # 构建详细提示
            prompt = f"""
你是一个专业的数据分析师。请分析以下数据并回答问题。

文件信息:
- 路径: {file_path}
- 形状: {df.shape}
- 列名: {list(df.columns)}

数据预览:
{df.head().to_string()}

数据统计:
{df.describe().to_string()}

问题: {question}

请提供:
1. 详细的数据分析
2. 关键发现和洞察
3. 实用的建议
4. 用中文回答，条理清晰
"""
            
            answer = self.chat_with_llm(prompt)
            print(f"📊 AI分析结果:\n{answer}")
            
            results["analyses"].append({
                "question": question,
                "answer": answer
            })
            print("-" * 80)
        
        # 生成图表
        chart_path = self.generate_charts(df, file_path)
        results["chart_path"] = chart_path
        
        return results
    
    def generate_charts(self, df: pd.DataFrame, file_path: str) -> str:
        """为数据生成可视化图表"""
        try:
            # 确定数值列和分类列
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            # 创建图表
            fig_size = (16, 12)
            fig, axes = plt.subplots(2, 3, figsize=fig_size)
            fig.suptitle(f'数据分析报告 - {Path(file_path).name}', fontsize=16, fontweight='bold')
            
            # 1. 数据形状信息
            ax1 = axes[0, 0]
            ax1.text(0.1, 0.5, f"""
📊 数据基本信息

文件: {Path(file_path).name}
行数: {df.shape[0]:,}
列数: {df.shape[1]}
数值列数: {len(numeric_cols)}
分类列数: {len(categorical_cols)}
缺失值: {df.isnull().sum().sum()}
内存使用: {df.memory_usage(deep=True).sum() / 1024:.1f} KB
            """, transform=ax1.transAxes, fontsize=10, verticalalignment='center',
                     bbox=dict(boxstyle='round', facecolor='lightblue'))
            ax1.set_title('数据集概览')
            ax1.axis('off')
            
            # 2. 数值列分布（如果有）
            ax2 = axes[0, 1]
            if numeric_cols:
                # 选择前几个数值列
                cols_to_plot = numeric_cols[:3]
                for i, col in enumerate(cols_to_plot):
                    ax2.hist(df[col].dropna(), alpha=0.7, label=col, bins=20)
                ax2.set_title('数值列分布')
                ax2.legend()
            else:
                ax2.text(0.5, 0.5, '无数值列', ha='center', va='center', transform=ax2.transAxes)
                ax2.set_title('数值列分布')
            
            # 3. 缺失值分析
            ax3 = axes[0, 2]
            missing_data = df.isnull().sum()
            if missing_data.sum() > 0:
                missing_data = missing_data[missing_data > 0].sort_values(ascending=True)
                if len(missing_data) > 0:
                    ax3.barh(range(len(missing_data)), missing_data.values)
                    ax3.set_yticks(range(len(missing_data)))
                    ax3.set_yticklabels(missing_data.index)
                    ax3.set_title('缺失值统计')
                    ax3.set_xlabel('缺失值数量')
            else:
                ax3.text(0.5, 0.5, '无缺失值', ha='center', va='center', transform=ax3.transAxes)
                ax3.set_title('缺失值统计')
            
            # 4. 分类列分布（如果有）
            ax4 = axes[1, 0]
            if categorical_cols:
                col = categorical_cols[0]
                value_counts = df[col].value_counts().head(10)
                ax4.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
                ax4.set_title(f'{col} 分布')
            else:
                ax4.text(0.5, 0.5, '无分类列', ha='center', va='center', transform=ax4.transAxes)
                ax4.set_title('分类列分布')
            
            # 5. 相关性矩阵（如果有多个数值列）
            ax5 = axes[1, 1]
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols].corr()
                im = ax5.imshow(corr_matrix, cmap='coolwarm', aspect='auto')
                ax5.set_xticks(range(len(numeric_cols)))
                ax5.set_yticks(range(len(numeric_cols)))
                ax5.set_xticklabels(numeric_cols, rotation=45)
                ax5.set_yticklabels(numeric_cols)
                ax5.set_title('相关性矩阵')
                
                # 添加数值标注
                for i in range(len(numeric_cols)):
                    for j in range(len(numeric_cols)):
                        ax5.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}', 
                                ha='center', va='center')
            else:
                ax5.text(0.5, 0.5, '数值列不足', ha='center', va='center', transform=ax5.transAxes)
                ax5.set_title('相关性矩阵')
            
            # 6. 数据质量摘要
            ax6 = axes[1, 2]
            quality_info = f"""
📋 数据质量摘要

完整性: {((df.size - df.isnull().sum().sum()) / df.size * 100):.1f}%
唯一性: {(df.nunique().sum() / df.size * 100):.1f}%
数值列占比: {(len(numeric_cols) / len(df.columns) * 100):.1f}%

🔍 检查项目:
- 重复行: {df.duplicated().sum()}
- 空白字符串: {(df == '').sum().sum() if df.select_dtypes(include=['object']).size > 0 else 0}
- 零值数量: {(df == 0).sum().sum() if len(numeric_cols) > 0 else 0}
            """
            ax6.text(0.1, 0.5, quality_info, transform=ax6.transAxes, fontsize=9,
                     verticalalignment='center', bbox=dict(boxstyle='round', facecolor='lightyellow'))
            ax6.set_title('数据质量评估')
            ax6.axis('off')
            
            plt.tight_layout()
            
            # 保存图表
            chart_filename = f"analysis_{Path(file_path).stem}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
            print(f"✅ 图表已保存为: {chart_filename}")
            
            plt.show()
            return chart_filename
            
        except Exception as e:
            print(f"❌ 生成图表失败: {e}")
            return None
    
    def interactive_analysis(self):
        """交互式数据分析"""
        print("🚀 智能文件数据分析器")
        print("=" * 50)
        
        while True:
            print("\n📋 可用操作:")
            print("1. 分析单个文件")
            print("2. 浏览目录中的文件")
            print("3. 自定义分析问题")
            print("4. 退出")
            
            choice = input("\n请选择操作 (1-4): ").strip()
            
            if choice == '1':
                self._analyze_single_file()
            elif choice == '2':
                self._browse_directory()
            elif choice == '3':
                self._custom_analysis()
            elif choice == '4':
                print("👋 再见！")
                break
            else:
                print("❌ 无效选择，请重试")
    
    def _analyze_single_file(self):
        """分析单个文件"""
        file_path = input("请输入文件路径: ").strip()
        if not file_path:
            return
        
        # 询问是否有特殊的读取参数
        print("\n📋 可选的读取参数:")
        print("例如: encoding=utf-8, sep=';', sheet_name=0")
        params_str = input("请输入参数 (回车跳过): ").strip()
        
        read_kwargs = {}
        if params_str:
            try:
                # 简单解析参数
                for param in params_str.split(','):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('\'"')
                        # 尝试转换数值
                        if value.isdigit():
                            value = int(value)
                        elif value.replace('.', '').isdigit():
                            value = float(value)
                        read_kwargs[key] = value
            except Exception as e:
                print(f"⚠️ 参数解析失败，使用默认设置: {e}")
        
        self.analyze_file(file_path, **read_kwargs)
    
    def _browse_directory(self):
        """浏览目录"""
        dir_path = input("请输入目录路径: ").strip()
        if not dir_path:
            return
        
        files = self.list_directory(dir_path)
        if not files:
            print("❌ 目录中没有找到支持的数据文件")
            return
        
        print(f"\n📁 找到 {len(files)} 个数据文件:")
        for i, file_path in enumerate(files, 1):
            file_size = Path(file_path).stat().st_size / 1024
            print(f"{i:2d}. {Path(file_path).name} ({file_size:.1f} KB)")
        
        try:
            choice = int(input(f"\n请选择要分析的文件 (1-{len(files)}): "))
            if 1 <= choice <= len(files):
                selected_file = files[choice - 1]
                self.analyze_file(selected_file)
            else:
                print("❌ 无效选择")
        except ValueError:
            print("❌ 请输入数字")
    
    def _custom_analysis(self):
        """自定义分析问题"""
        file_path = input("请输入文件路径: ").strip()
        if not file_path:
            return
        
        print("\n📝 请输入分析问题 (每行一个，空行结束):")
        questions = []
        while True:
            question = input().strip()
            if not question:
                break
            questions.append(question)
        
        if not questions:
            print("❌ 没有输入问题")
            return
        
        self.analyze_file(file_path, questions)


def main():
    """主函数"""
    analyzer = FileDataAnalyzer()
    
    # 检查Ollama服务
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                print(f"✅ Ollama服务正常，可用模型: {[m['name'] for m in models]}")
                analyzer.interactive_analysis()
            else:
                print("❌ 未找到Ollama模型，请先下载模型")
        else:
            print("❌ Ollama服务异常")
    except:
        print("❌ 无法连接到Ollama服务，请确保服务已启动")


if __name__ == "__main__":
    main()