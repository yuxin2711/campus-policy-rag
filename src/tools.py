from langchain_core.tools import tool

@tool
def calculate_gpa(scores_str: str) -> str:
    """根据课程成绩计算GPA。参数格式如'高数:85,英语:90,物理:78'，按4.0制计算。"""
    try:
        items = scores_str.split(',')
        total_points = 0
        count = 0
        for item in items:
            course, score = item.split(':')
            score = float(score)
            if score >= 90: point = 4.0
            elif score >= 85: point = 3.7
            elif score >= 82: point = 3.3
            elif score >= 78: point = 3.0
            elif score >= 75: point = 2.7
            elif score >= 72: point = 2.3
            elif score >= 68: point = 2.0
            elif score >= 64: point = 1.5
            elif score >= 60: point = 1.0
            else: point = 0
            total_points += point
            count += 1
        return f"根据输入成绩，GPA为：{total_points/count:.2f}"
    except Exception as e:
        return f"计算GPA失败，请检查输入格式。错误：{e}"

@tool
def query_course_schedule(student_id: str, semester: str) -> str:
    """查询指定学生某学期的课表。参数：student_id（学号），semester（学期，如'2025-2026-1'）"""
    # 模拟数据（真实场景可从数据库或教务系统API获取）
    mock_data = {
        "2023001": {
            "2025-2026-1": "周一 1-2节：高等数学；周三 3-4节：大学物理；周五 5-6节：程序设计基础"
        }
    }
    result = mock_data.get(student_id, {}).get(semester)
    if result:
        return f"学号{student_id}在{semester}学期的课表：{result}"
    else:
        return f"未查询到学号{student_id}在{semester}学期的课表数据。"