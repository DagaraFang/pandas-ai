"""
智能文件数据分析器

支持从指定路径读取各种格式的数据文件，并进行AI驱动的数据分析和可视化
"""
import pandas as pd
import numpy as np
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
        
        # 默认问题 - 更丰富的报表类型
        if questions is None:
            questions = [
                "请生成完整的数据质量评估报告，包括缺失值、重复值、数据类型一致性分析",
                "制作详细的描述性统计分析报表，包含分布特征、集中趋势、离散程度",
                "生成数据趋势分析报告，识别时间序列模式、季节性变化、异常点检测",
                "创建相关性分析矩阵报表，发现变量间的关联关系和潜在因果关系",
                "制作业务洞察仪表板，提供关键指标、预警信号、决策建议",
                "生成异常值检测报告，使用统计学方法识别离群点并分析原因",
                "创建数据分布分析报表，包含正态性检验、偏度峰度分析",
                "制作预测性分析报告，基于历史数据预测未来趋势"
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
        """为数据生成丰富的可视化图表报表"""
        try:
            # 确定数值列和分类列
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
            
            # 尝试识别日期列
            for col in df.columns:
                if col not in datetime_cols:
                    try:
                        pd.to_datetime(df[col].dropna().head(100))
                        datetime_cols.append(col)
                    except:
                        pass
            
            # 创建更大的图表网格
            fig_size = (20, 24)
            fig, axes = plt.subplots(4, 3, figsize=fig_size)
            fig.suptitle(f'智能数据分析报表 - {Path(file_path).name}', fontsize=18, fontweight='bold')
            
            # 1. 数据集概览信息
            ax1 = axes[0, 0]
            overview_text = f"""
📊 数据集基本信息

文件: {Path(file_path).name}
📈 行数: {df.shape[0]:,}
📊 列数: {df.shape[1]}
🔢 数值列: {len(numeric_cols)}
🏷️ 分类列: {len(categorical_cols)}
📅 日期列: {len(datetime_cols)}
⚠️ 缺失值: {df.isnull().sum().sum()}
💾 内存: {df.memory_usage(deep=True).sum() / 1024:.1f} KB
🔄 重复行: {df.duplicated().sum()}
            """
            ax1.text(0.1, 0.5, overview_text, transform=ax1.transAxes, fontsize=11, 
                    verticalalignment='center', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
            ax1.set_title('数据集概览', fontsize=14, fontweight='bold')
            ax1.axis('off')
            
            # 2. 数值列分布直方图
            ax2 = axes[0, 1]
            if numeric_cols:
                cols_to_plot = numeric_cols[:3]
                colors = ['skyblue', 'lightcoral', 'lightgreen']
                for i, col in enumerate(cols_to_plot):
                    ax2.hist(df[col].dropna(), alpha=0.7, label=col, bins=30, 
                            color=colors[i % len(colors)], edgecolor='black', linewidth=0.5)
                ax2.set_title('数值列分布直方图', fontsize=14, fontweight='bold')
                ax2.legend()
                ax2.grid(True, alpha=0.3)
            else:
                ax2.text(0.5, 0.5, '⚠️ 无数值列数据', ha='center', va='center', 
                        transform=ax2.transAxes, fontsize=12, 
                        bbox=dict(boxstyle='round', facecolor='lightyellow'))
                ax2.set_title('数值列分布直方图', fontsize=14, fontweight='bold')
            
            # 3. 缺失值热力图
            ax3 = axes[0, 2]
            missing_data = df.isnull().sum()
            if missing_data.sum() > 0:
                missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
                if len(missing_data) > 0:
                    bars = ax3.barh(range(len(missing_data)), missing_data.values, 
                                   color='lightcoral', edgecolor='darkred', linewidth=1)
                    ax3.set_yticks(range(len(missing_data)))
                    ax3.set_yticklabels(missing_data.index, fontsize=10)
                    ax3.set_title('缺失值统计热力图', fontsize=14, fontweight='bold')
                    ax3.set_xlabel('缺失值数量')
                    # 添加数值标签
                    for i, bar in enumerate(bars):
                        width = bar.get_width()
                        ax3.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                                f'{int(width)}', ha='left', va='center')
                    ax3.grid(True, alpha=0.3)
            else:
                ax3.text(0.5, 0.5, '✅ 无缺失值\n数据质量优秀', ha='center', va='center', 
                        transform=ax3.transAxes, fontsize=12, 
                        bbox=dict(boxstyle='round', facecolor='lightgreen'))
                ax3.set_title('缺失值统计热力图', fontsize=14, fontweight='bold')
            
            # 4. 分类列数据饼状图（增强版）
            ax4 = axes[1, 0]
            if categorical_cols:
                col = categorical_cols[0]
                value_counts = df[col].value_counts().head(8)
                colors = plt.cm.Set3(np.linspace(0, 1, len(value_counts)))
                wedges, texts, autotexts = ax4.pie(value_counts.values, labels=value_counts.index, 
                                                  autopct='%1.1f%%', colors=colors, startangle=90,
                                                  explode=[0.05]*len(value_counts))
                # 美化文本
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                ax4.set_title(f'{col} 分布饼状图', fontsize=14, fontweight='bold')
            else:
                ax4.text(0.5, 0.5, '⚠️ 无分类列数据', ha='center', va='center', 
                        transform=ax4.transAxes, fontsize=12,
                        bbox=dict(boxstyle='round', facecolor='lightyellow'))
                ax4.set_title('分类列分布饼状图', fontsize=14, fontweight='bold')
            
            # 5. 相关性热力图（增强版）
            ax5 = axes[1, 1]
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols].corr()
                im = ax5.imshow(corr_matrix, cmap='RdYlBu_r', aspect='auto', vmin=-1, vmax=1)
                ax5.set_xticks(range(len(numeric_cols)))
                ax5.set_yticks(range(len(numeric_cols)))
                ax5.set_xticklabels(numeric_cols, rotation=45, ha='right')
                ax5.set_yticklabels(numeric_cols)
                ax5.set_title('相关性热力图', fontsize=14, fontweight='bold')
                
                # 添加数值标注和颜色条
                for i in range(len(numeric_cols)):
                    for j in range(len(numeric_cols)):
                        text_color = 'white' if abs(corr_matrix.iloc[i, j]) > 0.5 else 'black'
                        ax5.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}', 
                                ha='center', va='center', color=text_color, fontweight='bold')
                # 添加颜色条
                plt.colorbar(im, ax=ax5, shrink=0.8, label='相关系数')
            else:
                ax5.text(0.5, 0.5, '⚠️ 数值列不足\n无法计算相关性', ha='center', va='center', 
                        transform=ax5.transAxes, fontsize=12,
                        bbox=dict(boxstyle='round', facecolor='lightyellow'))
                ax5.set_title('相关性热力图', fontsize=14, fontweight='bold')
            
            # 6. 数据质量仪表板（增强版）
            ax6 = axes[1, 2]
            completeness = ((df.size - df.isnull().sum().sum()) / df.size * 100)
            uniqueness = (df.nunique().sum() / df.size * 100)
            duplicates = df.duplicated().sum()
            
            quality_metrics = {
                '完整性': completeness,
                '唯一性': uniqueness,
                '重复率': (duplicates / len(df) * 100) if len(df) > 0 else 0
            }
            
            quality_info = f"""
📊 数据质量仪表板

✅ 完整性: {completeness:.1f}%
🔍 唯一性: {uniqueness:.1f}%
⚠️ 重复率: {quality_metrics['重复率']:.1f}%
📊 数值列占比: {(len(numeric_cols) / len(df.columns) * 100):.1f}%

🔍 详细检查:
• 重复行: {duplicates:,}
• 空白值: {(df == '').sum().sum() if df.select_dtypes(include=['object']).size > 0 else 0}
• 零值: {(df == 0).sum().sum() if len(numeric_cols) > 0 else 0}
• 负值: {(df[numeric_cols] < 0).sum().sum() if len(numeric_cols) > 0 else 0}
            """
            ax6.text(0.1, 0.5, quality_info, transform=ax6.transAxes, fontsize=10,
                     verticalalignment='center', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
            ax6.set_title('数据质量仪表板', fontsize=14, fontweight='bold')
            ax6.axis('off')
            
            # 7. 数值列箱线图（新增）
            ax7 = axes[2, 0]
            if numeric_cols:
                cols_to_plot = numeric_cols[:4]
                box_data = [df[col].dropna() for col in cols_to_plot]
                bp = ax7.boxplot(box_data, labels=cols_to_plot, patch_artist=True, 
                               notch=True, showmeans=True)
                # 美化箱线图
                colors = ['lightblue', 'lightcoral', 'lightgreen', 'lightyellow']
                for patch, color in zip(bp['boxes'], colors):
                    patch.set_facecolor(color)
                    patch.set_alpha(0.7)
                ax7.set_title('数值列箱线图（异常值检测）', fontsize=14, fontweight='bold')
                ax7.set_ylabel('数值')
                ax7.grid(True, alpha=0.3)
                plt.setp(ax7.get_xticklabels(), rotation=45, ha='right')
            else:
                ax7.text(0.5, 0.5, '⚠️ 无数值列数据', ha='center', va='center', 
                        transform=ax7.transAxes, fontsize=12,
                        bbox=dict(boxstyle='round', facecolor='lightyellow'))
                ax7.set_title('数值列箱线图', fontsize=14, fontweight='bold')
            
            # 8. 数据分布Q-Q图（新增）
            ax8 = axes[2, 1]
            if numeric_cols:
                try:
                    from scipy import stats
                    col = numeric_cols[0]
                    data = df[col].dropna()
                    if len(data) > 10:
                        stats.probplot(data, dist="norm", plot=ax8)
                        ax8.set_title(f'{col} 正态性Q-Q图', fontsize=14, fontweight='bold')
                        ax8.grid(True, alpha=0.3)
                    else:
                        ax8.text(0.5, 0.5, '数据量不足', ha='center', va='center', transform=ax8.transAxes)
                        ax8.set_title('数据分布Q-Q图', fontsize=14, fontweight='bold')
                except ImportError:
                    ax8.text(0.5, 0.5, '需要scipy库', ha='center', va='center', transform=ax8.transAxes)
                    ax8.set_title('数据分布Q-Q图', fontsize=14, fontweight='bold')
            else:
                ax8.text(0.5, 0.5, '无数值列数据', ha='center', va='center', transform=ax8.transAxes)
                ax8.set_title('数据分布Q-Q图', fontsize=14, fontweight='bold')
            
            # 9. 数据量级对比（新增）
            ax9 = axes[2, 2]
            if len(df.columns) > 1:
                # 各列的数据量级对比
                col_stats = []
                col_names = []
                for col in df.columns:
                    if df[col].dtype in ['int64', 'float64']:
                        col_stats.append(df[col].count())
                        col_names.append(f'{col}\n(有效值)')
                    else:
                        col_stats.append(df[col].nunique())
                        col_names.append(f'{col}\n(唯一值)')
                
                if col_stats:
                    bars = ax9.bar(range(len(col_stats)), col_stats, 
                                  color=['lightblue' if i % 2 == 0 else 'lightcoral' for i in range(len(col_stats))],
                                  edgecolor='black', linewidth=0.5)
                    ax9.set_xticks(range(len(col_names)))
                    ax9.set_xticklabels(col_names, rotation=45, ha='right', fontsize=9)
                    ax9.set_title('各列数据量级对比', fontsize=14, fontweight='bold')
                    ax9.set_ylabel('数量')
                    ax9.grid(True, alpha=0.3)
                    
                    # 添加数值标签
                    for bar, value in zip(bars, col_stats):
                        height = bar.get_height()
                        ax9.text(bar.get_x() + bar.get_width()/2., height + max(col_stats)*0.01,
                                f'{value:,}', ha='center', va='bottom', fontsize=8)
            else:
                ax9.text(0.5, 0.5, '数据列不足', ha='center', va='center', transform=ax9.transAxes)
                ax9.set_title('各列数据量级对比', fontsize=14, fontweight='bold')
            
            # 10. 数据类型分布（新增）
            ax10 = axes[3, 0]
            dtype_counts = df.dtypes.value_counts()
            if len(dtype_counts) > 0:
                colors = ['lightblue', 'lightcoral', 'lightgreen', 'lightyellow', 'lightpink']
                wedges, texts, autotexts = ax10.pie(dtype_counts.values, 
                                                   labels=[str(dtype) for dtype in dtype_counts.index],
                                                   autopct='%1.1f%%', colors=colors[:len(dtype_counts)],
                                                   startangle=90)
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                ax10.set_title('数据类型分布', fontsize=14, fontweight='bold')
            else:
                ax10.text(0.5, 0.5, '无数据类型', ha='center', va='center', transform=ax10.transAxes)
                ax10.set_title('数据类型分布', fontsize=14, fontweight='bold')
            
            # 11. 业务指标仪表板（新增）
            ax11 = axes[3, 1]
            business_metrics = f"""
📊 业务指标仪表板

📊 数据量级:
• 总记录数: {len(df):,}
• 平均每列数据: {df.count().mean():.1f}

🔍 数据密度:
• 数据密度: {(df.count().sum() / df.size * 100):.1f}%
• 非空率: {(df.notna().sum().sum() / df.size * 100):.1f}%

📈 变化程度:
• 平均唯一值: {df.nunique().mean():.1f}
• 数据多样性: {(df.nunique().sum() / df.size * 100):.1f}%
            """
            ax11.text(0.1, 0.5, business_metrics, transform=ax11.transAxes, fontsize=10,
                     verticalalignment='center', bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
            ax11.set_title('业务指标仪表板', fontsize=14, fontweight='bold')
            ax11.axis('off')
            
            # 12. 数据趋势分析（新增）
            ax12 = axes[3, 2]
            if datetime_cols and numeric_cols:
                # 尝试创建时间序列分析
                date_col = datetime_cols[0]
                value_col = numeric_cols[0]
                try:
                    df_temp = df[[date_col, value_col]].dropna()
                    df_temp[date_col] = pd.to_datetime(df_temp[date_col])
                    df_temp = df_temp.sort_values(date_col)
                    
                    ax12.plot(df_temp[date_col], df_temp[value_col], marker='o', 
                             linewidth=2, markersize=4, color='steelblue')
                    ax12.set_title(f'{value_col} 时间趋势', fontsize=14, fontweight='bold')
                    ax12.set_xlabel('时间')
                    ax12.set_ylabel(value_col)
                    ax12.grid(True, alpha=0.3)
                    plt.setp(ax12.get_xticklabels(), rotation=45, ha='right')
                except:
                    ax12.text(0.5, 0.5, '无法解析时间数据', ha='center', va='center', transform=ax12.transAxes)
                    ax12.set_title('数据趋势分析', fontsize=14, fontweight='bold')
            else:
                trend_info = f"""
📈 趋势分析摘要

日期列: {len(datetime_cols)}
数值列: {len(numeric_cols)}

现有数据类型:
{chr(10).join([f'• {col}: {str(df[col].dtype)}' for col in df.columns[:5]])}
{'...' if len(df.columns) > 5 else ''}
                """
                ax12.text(0.1, 0.5, trend_info, transform=ax12.transAxes, fontsize=9,
                         verticalalignment='center', bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))
                ax12.set_title('数据趋势分析', fontsize=14, fontweight='bold')
                ax12.axis('off')
            
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