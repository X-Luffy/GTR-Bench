import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, List

class ResultDisplay:
    """结果显示组件类"""
    
    @staticmethod
    def display_result(result: Dict, case: Dict) -> None:
        """显示答题结果"""
        st.markdown('<h3 class="sub-header">📊 答题结果</h3>', unsafe_allow_html=True)
        
        if result['accuracy_score'] > 0:
            st.markdown('<div class="result-correct">✅ 回答正确！</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-incorrect">❌ 回答错误</div>', unsafe_allow_html=True)
        
        # 显示详细信息
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("总得分", f"{result['score']:.2f}")
            st.metric("准确率得分", f"{result['accuracy_score']:.2f}")
            st.metric("时间得分", f"{result['time_score']:.2f}")
        
        with col2:
            st.metric("答题时间", f"{result['elapsed_time']:.1f}秒")
            st.metric("题目类型", result['task_type'])
            st.metric("题目ID", result['case_id'])
        
        # 显示正确答案
        st.markdown('<h4>📋 正确答案</h4>', unsafe_allow_html=True)
        st.info(f"**正确答案:** {result['ground_truth']}")
        
        # 显示用户答案
        st.markdown('<h4>👤 您的答案</h4>', unsafe_allow_html=True)
        user_answers = result['user_answers']
        
        if 'options' in user_answers:
            st.write(f"**选项答案:** {', '.join(user_answers['options'])}")
        
        time_answers = {k: v for k, v in user_answers.items() if k.endswith('_time')}
        if time_answers:
            st.write("**时间答案:**")
            for field, answer in time_answers.items():
                st.write(f"- {field}: {answer}")
    
    @staticmethod
    def display_results_summary(results: List[Dict]) -> None:
        """显示答题结果汇总"""
        if not results:
            st.warning("暂无答题记录")
            return
        
        st.markdown('<h3 class="sub-header">📈 答题结果汇总</h3>', unsafe_allow_html=True)
        
        # 创建结果DataFrame
        df = pd.DataFrame(results)
        
        # 显示统计信息
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("总题目数", len(df))
        
        with col2:
            correct_count = len(df[df['accuracy_score'] > 0])
            st.metric("正确题目数", correct_count)
        
        with col3:
            accuracy = correct_count / len(df) * 100 if len(df) > 0 else 0
            st.metric("正确率", f"{accuracy:.1f}%")
        
        with col4:
            avg_score = df['score'].mean() if len(df) > 0 else 0
            st.metric("Average Score", f"{avg_score:.2f}")
        
        # 显示详细结果表格
        st.markdown('<h4>📋 详细结果</h4>', unsafe_allow_html=True)
        
        # 简化显示列
        display_df = df[['case_id', 'task_type', 'score', 'accuracy_score', 'time_score', 'elapsed_time']].copy()
        display_df['elapsed_time'] = display_df['elapsed_time'].round(1)
        display_df['score'] = display_df['score'].round(2)
        display_df['accuracy_score'] = display_df['accuracy_score'].round(2)
        display_df['time_score'] = display_df['time_score'].round(2)
        
        st.dataframe(display_df, use_container_width=True)
        
        # 导出结果
        if st.button("📥 导出结果"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV File",
                data=csv,
                file_name=f"answer_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    @staticmethod
    def display_score_breakdown(score_breakdown: Dict) -> None:
        """显示得分分解"""
        st.markdown('<h4>🔍 得分分解</h4>', unsafe_allow_html=True)
        
        # 准确率分解
        accuracy_breakdown = score_breakdown.get('accuracy_breakdown', {})
        st.write("**准确率分解:**")
        st.write(f"- 选项得分: {accuracy_breakdown.get('option_score', 0):.2f}")
        st.write(f"- 时间答案得分: {accuracy_breakdown.get('time_answer_score', 0):.2f}")
        st.write(f"- 总准确率得分: {accuracy_breakdown.get('total_accuracy', 0):.2f}")
        
        # 时间分解
        time_breakdown = score_breakdown.get('time_breakdown', {})
        st.write("**时间分解:**")
        st.write(f"- 答题时间: {time_breakdown.get('elapsed_time', 0):.1f}秒")
        st.write(f"- 时间得分: {time_breakdown.get('time_score', 0):.2f}")
        st.write(f"- 时间阈值: {time_breakdown.get('time_threshold', 0)}秒")
        
        # 权重信息
        weights = score_breakdown.get('weights', {})
        st.write("**权重信息:**")
        st.write(f"- 准确率权重: {weights.get('accuracy_weight', 0):.2f}")
        st.write(f"- 时间权重: {weights.get('time_weight', 0):.2f}")
    
    @staticmethod
    def display_progress_chart(results: List[Dict]) -> None:
        """显示进度图表"""
        if not results:
            return
        
        st.markdown('<h4>📊 答题进度</h4>', unsafe_allow_html=True)
        
        # 创建进度数据
        df = pd.DataFrame(results)
        df['cumulative_score'] = df['score'].cumsum()
        df['cumulative_accuracy'] = (df['accuracy_score'] > 0).cumsum()
        df['question_number'] = range(1, len(df) + 1)
        
        # 显示累计得分图表
        st.line_chart(df.set_index('question_number')['cumulative_score'])
        
        # 显示正确率趋势
        accuracy_rate = df['cumulative_accuracy'] / df['question_number'] * 100
        st.line_chart(accuracy_rate)
    
    @staticmethod
    def display_task_analysis(results: List[Dict]) -> None:
        """显示任务类型分析"""
        if not results:
            return
        
        st.markdown('<h4>📈 任务类型分析</h4>', unsafe_allow_html=True)
        
        df = pd.DataFrame(results)
        
        # 按任务类型分组统计
        task_stats = df.groupby('task_type').agg({
            'score': ['mean', 'std', 'count'],
            'accuracy_score': lambda x: (x > 0).sum(),
            'elapsed_time': 'mean'
        }).round(2)
        
        # 重命名列
        task_stats.columns = ['平均得分', '得分标准差', '题目数量', '正确数量', '平均时间']
        task_stats['正确率'] = (task_stats['正确数量'] / task_stats['题目数量'] * 100).round(1)
        
        st.dataframe(task_stats, use_container_width=True)
