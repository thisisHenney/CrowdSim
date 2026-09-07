# -*- coding: utf-8 -*-
"""토큰으로부터 QSS를 생성합니다.

QSS를 문자열로 여기저기 흩어놓지 않는 것이 요점입니다.
테마 전환은 build_qss(DARK)를 다시 호출해 setStyleSheet 하면 끝납니다.
"""
from tokens import LIGHT, DARK, RADIUS


def build_qss(theme=None) -> str:
    T = theme or LIGHT
    R = RADIUS
    return f"""
/* ---------- 바탕 ---------- */
#root, #pane, QScrollArea {{ background:{T['surface']}; }}
QWidget {{ color:{T['ink']}; }}

/* ---------- 툴바 ---------- */
#toolbar {{ background:{T['surface']}; border-bottom:1px solid {T['line']}; }}
#tbtn {{ border:1px solid transparent; border-radius:{R['md']}px; padding:5px 10px;
         color:{T['ink2']}; background:transparent; }}
#tbtn:hover {{ background:{T['surface3']}; color:{T['ink']}; }}
#tbtn[kind="go"] {{ background:{T['ok_soft']}; color:{T['ok']};
                    border-color:{T['ok']}; font-weight:600; }}
#tbtn[kind="stop"] {{ color:{T['crit']}; }}
#chip {{ background:{T['surface3']}; color:{T['ink2']};
         border-radius:{R['pill']}px; padding:3px 9px; margin-left:6px; }}

/* ---------- 좌측 레일 ---------- */
#rail {{ background:{T['surface2']}; border-right:1px solid {T['line']}; }}
#nav {{ text-align:left; padding:7px 36px 7px 10px; border:none;
        border-radius:{R['md']}px; color:{T['ink2']}; background:transparent; }}
#nav:hover {{ background:{T['surface3']}; color:{T['ink']}; }}
#nav:checked {{ background:{T['accent_soft']}; color:{T['accent_ink']};
                border-left:3px solid {T['accent']}; padding-left:7px; }}
#badge {{ background:{T['surface3']}; color:{T['ink3']};
          border-radius:{R['sm']}px; padding:1px 6px; }}
#badgeOn {{ background:{T['accent']}; color:#ffffff;
            border-radius:{R['sm']}px; padding:1px 6px; }}
#dotWarn {{ background:{T['warn']}; border-radius:3px; }}

/* ---------- 탭 ---------- */
#work::pane {{ border:none; border-top:1px solid {T['line']};
               background:{T['surface']}; }}
#work QTabBar {{ background:{T['surface2']}; }}
#work QTabBar::tab {{ background:transparent; color:{T['ink2']};
                      padding:9px 14px; border:none;
                      border-bottom:2px solid transparent; }}
#work QTabBar::tab:hover {{ color:{T['ink']}; }}
#work QTabBar::tab:selected {{ color:{T['accent_ink']}; background:{T['surface']};
                               border-bottom:2px solid {T['accent']};
                               font-weight:600; }}

/* ---------- 그룹 박스 ---------- */
#group {{ background:{T['surface']}; border:1px solid {T['line']};
          border-radius:{R['lg']}px; }}
#groupHead {{ background:{T['surface2']}; border-bottom:1px solid {T['line_soft']};
              border-top-left-radius:{R['lg']}px;
              border-top-right-radius:{R['lg']}px; }}
#groupBody {{ background:{T['surface']};
              border-bottom-left-radius:{R['lg']}px;
              border-bottom-right-radius:{R['lg']}px; }}

/* ---------- 입력 ---------- */
#field {{ background:{T['surface2']}; border:1px solid {T['line']};
          border-radius:{R['md']}px; padding:6px 9px; color:{T['ink']};
          selection-background-color:{T['accent']}; }}
#field:focus {{ border:1px solid {T['accent']}; background:{T['surface']}; }}
/* 계산값 — 사용자가 못 고치는 값임을 점선으로 알림 */
#field[state="computed"] {{ background:{T['accent_soft']}; color:{T['accent_ink']};
                            border:1px dashed {T['accent']}; }}
/* 오류 — 색만이 아니라 테두리 형태로도 구분 (색각 이상 대응) */
#field[state="bad"] {{ border:1px solid {T['crit']}; }}
QComboBox#field::drop-down {{ border:none; width:18px; }}
QComboBox#field QAbstractItemView {{ background:{T['surface']};
    border:1px solid {T['line']}; selection-background-color:{T['accent_soft']};
    selection-color:{T['accent_ink']}; outline:none; }}

/* ---------- 세그먼트 ---------- */
#segLeft, #segRight {{ background:{T['surface2']}; color:{T['ink2']};
                       border:1px solid {T['line']}; padding:6px 15px; }}
#segLeft {{ border-top-left-radius:{R['md']}px;
            border-bottom-left-radius:{R['md']}px; border-right:none; }}
#segRight {{ border-top-right-radius:{R['md']}px;
             border-bottom-right-radius:{R['md']}px; }}
#segLeft:checked, #segRight:checked {{ background:{T['accent']}; color:#ffffff;
                                       border-color:{T['accent']};
                                       font-weight:600; }}

/* ---------- 버튼 ---------- */
#btn {{ background:{T['surface2']}; border:1px solid {T['line']};
        border-radius:{R['md']}px; padding:6px 13px; color:{T['ink']}; }}
#btn:hover {{ background:{T['surface3']}; }}
#btnPri {{ background:{T['accent']}; border:1px solid {T['accent']};
           border-radius:{R['md']}px; padding:6px 13px; color:#ffffff; }}
#btnPri:hover {{ background:{T['accent_ink']}; }}

/* ---------- 표 ---------- */
QTableWidget {{ background:{T['surface']}; border:1px solid {T['line']};
                border-radius:{R['lg']}px; gridline-color:transparent;
                outline:none; }}
QTableWidget::item {{ padding:4px 12px; border-bottom:1px solid {T['line_soft']}; }}
QHeaderView::section {{ background:{T['surface2']}; color:{T['ink3']};
    border:none; border-bottom:1px solid {T['line']}; padding:8px 12px;
    font-weight:600; }}

/* ---------- 우측 정보 패널 ---------- */
#insp {{ background:{T['surface2']}; border-left:1px solid {T['line']}; }}

/* ---------- 터미널 ---------- */
#term {{ background:{T['term_bg']}; color:{T['term_ink']};
         border:1px solid {T['line']}; border-radius:{R['lg']}px;
         padding:12px 14px; }}

/* ---------- 진행 막대 ---------- */
#prog, #progWarn {{ background:{T['surface3']}; border:none; border-radius:3px; }}
#prog::chunk {{ background:{T['accent']}; border-radius:3px; }}
#progWarn::chunk {{ background:{T['warn']}; border-radius:3px; }}

/* ---------- 스크롤바 ---------- */
QScrollBar:vertical {{ background:transparent; width:10px; margin:0; }}
QScrollBar::handle:vertical {{ background:{T['line']}; border-radius:5px;
                               min-height:30px; }}
QScrollBar::handle:vertical:hover {{ background:{T['ink3']}; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height:0; border:none; }}
QScrollBar::add-page, QScrollBar::sub-page {{ background:transparent; }}
"""


def apply_theme(app, theme=None):
    """QApplication에 테마 적용. 런타임 전환도 이 함수를 다시 부르면 됩니다."""
    app.setStyle("Fusion")          # OS 테마 간섭 차단 — 필수
    app.setStyleSheet(build_qss(theme))


if __name__ == "__main__":
    for name, th in (("LIGHT", LIGHT), ("DARK", DARK)):
        qss = build_qss(th)
        print(f"{name}: {len(qss)} chars, {qss.count('{')} rules")
