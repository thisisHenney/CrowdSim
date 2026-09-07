# CrowdSim 적용 가이드

이 폴더는 HESA 프로젝트에서 가져온 디자인 시스템입니다.

> **적용 상태 (2026-09-07 갱신)**
>
> **방식 A 가 배선되어 있습니다.** `view/design_adapter.py` + `main.py` 초기화 +
> `theme.py` 의 `#field`/`#group` QSS 까지 들어가 있습니다.
>
> 다만 **실제 화면에서 이 위젯을 쓰는 곳은 아직 없습니다.** 인프라만 깔린
> 상태이고, 현재 UI 는 이 배선으로 달라지지 않습니다. 새 화면이나 기존 패널에
> `Field`/`make_table` 을 쓰려면 아래처럼 가져다 쓰면 됩니다.
>
> ```python
> from view.design_adapter import setup, widgets as W
> ```
>
> 아래 3장의 "방식 A" 절과 2건의 판단(테마 연동 색, setStyle 미호출)은
> 실제 코드에 반영되어 있습니다. 되돌리려면 `main.py` 의 try 블록만 지우면 됩니다.

CrowdSim에는 이미 자체 테마 체계가 있어 그냥 얹으면 화면이 깨집니다.
방식 B/C 로 더 나아가기 전에 이 문서를 끝까지 읽으세요.

---

## 1. 현재 상황 (실측)

### 1.1 CrowdSim에는 이미 테마 체계가 있다

`view/theme.py` (497줄)가 이미 다음을 갖추고 있습니다.

- 토큰 dict 8개 (`BG`/`CARD`/`BORDER`/`TEXT`/`DIM`/`ACCENT`/`BAR_BG`/`ALT_ROW`)
- 라이트 / 다크 두 테마
- `build_css()` 로 QSS 생성
- `set_theme()` / `toggle_theme()` 로 전환

**구조가 design-system과 거의 같습니다.** 토큰 dict + QSS 생성이라는 발상이 동일합니다.
따라서 "새 체계를 도입"하는 게 아니라 "두 체계를 합치는" 작업입니다.

### 1.2 진입점은 한 곳뿐이다

```
main.py:16   from view.theme import build_css
main.py:42   app.setStyleSheet(build_css())
```

이것이 유일한 QSS 적용 지점입니다. **되돌리기가 쉽다는 뜻입니다.**

### 1.3 하드코딩된 색의 분포

| 위치 | 개수 | 손대도 되나 |
|---|---|---|
| `view/theme.py` | 28 | 교체 대상 |
| `lib/nextlib/**` | 33 | **손대지 말 것** |
| 그 외 `view/**` | 34 | 정리 대상 |
| **합계** | **95** | **실작업 34곳** |

`lib/nextlib/`는 다른 프로젝트와 공유하는 라이브러리입니다.
여기를 고치면 CrowdSim 밖에도 영향이 갑니다.

### 1.4 커밋되지 않은 변경이 있다 (해소됨)

이 문서를 처음 쓸 때 미커밋 상태였던 zone/export 관련 변경 5건은
`fix/zone-spec-and-ui-polish` 브랜치에 커밋되었습니다.

앞으로도 원칙은 같습니다 - **스타일 작업과 기능 변경을 한 커밋에 섞지 마세요.**
문제가 생겼을 때 원인을 가립니다.

---

## 2. 토큰 이름이 다르다 — 핵심 충돌

두 체계가 같은 개념을 다른 이름으로 부릅니다.

| CrowdSim | design-system | 의미 |
|---|---|---|
| `BG` | `surface` | 기본 배경 |
| `CARD` | `surface` | 입력 필드 배경 |
| `BAR_BG` | `surface2` | 툴바·버튼 배경 |
| `ALT_ROW` | `surface2` | 표 교차 행 |
| `BORDER` | `line` | 경계선 |
| `TEXT` | `ink` | 본문 |
| `DIM` | `ink2` 또는 `ink3` | 보조 텍스트 |
| `ACCENT` | `accent` | 강조 |
| (없음) | `ink3` | 힌트 (3단계) |
| (없음) | `ok`/`warn`/`crit` | 상태색 |
| (없음) | `surface3` | 눌린 상태 |

주의할 점 두 가지입니다.

**`DIM` 하나가 `ink2`와 `ink3` 둘로 갈라집니다.** design-system은 보조 텍스트를
두 단계로 나눕니다. 기계적으로 치환할 수 없고, 각 사용처가 "필수 정보인가"를
보고 판단해야 합니다.

**CrowdSim에는 상태색이 없습니다.** `ok`/`warn`/`crit`이 추가되면
기존에 없던 표현이 생깁니다. 이건 순수한 추가이므로 충돌하지 않습니다.

---

## 3. 적용 방식 3가지

### 방식 A — 위젯만 가져오기 (권장, 위험도 낮음)

`theme.py`는 그대로 두고, CrowdSim에 없는 위젯만 씁니다.

```python
# CrowdSim theme.py 의 토큰을 design-system 이름으로 연결
from view.theme import T as _T
import widgets as W

adapter = {
    "surface": _T("BG"),       "surface2":  _T("BAR_BG"),
    "surface3": _T("ALT_ROW"),
    "ink": _T("TEXT"),         "ink2":      _T("DIM"),
    "ink3": _T("DIM"),         "line":      _T("BORDER"),
    "line_soft": _T("BORDER"), "accent":    _T("ACCENT"),
    # CrowdSim 에 없는 것은 값을 직접 넣습니다
    "accent_soft": "#e3eefc",  "accent_ink": "#075099",
    "ok": "#15803d",  "ok_soft": "#e3f4e9",
    "warn": "#b45309", "crit": "#b91c1c",
}

W.init_fonts()          # QApplication 생성 이후
W.set_theme(adapter)
```

**이 코드는 실제로 검증되었습니다.** `adapter_example.py` 를 실행해 확인할 수 있습니다.

```bash
.venv\Scripts\python.exe design-systemdapter_example.py
```

CrowdSim 의 실제 색(`#2563eb` 등)이 위젯에 주입되고,
기존 `build_css()` 와 함께 써도 충돌하지 않는 것을 확인했습니다.

가져올 만한 것:

| 위젯 | CrowdSim 에 있나 |
|---|---|
| `Field` (라벨+입력+오류 한 덩어리) | 없음 |
| `Group` (제목 바 카드) | `QGroupBox` 로 대체 중 |
| `make_table()` | 없음 |
| `Sparkline` | 없음 |
| `Swatch` | 없음 |

**장점** 기존 화면이 전혀 바뀌지 않습니다. 새 화면에만 씁니다.
**단점** 두 체계가 공존합니다.

#### 방식 A 의 실제 한계 (검증 결과)

`shots/adapter.png` 가 실제 렌더 결과입니다. 색은 CrowdSim 것이 제대로 들어가지만,
**QSS 규칙이 없어 일부 표현이 빠집니다.**

| 위젯 | 상태 | 원인 |
|---|---|---|
| `Field` 기본 | 정상 | `QLineEdit` 규칙이 기존 CSS 에 있음 |
| `Field` 오류 테두리 | **빠짐** | `#field[state="bad"]` 규칙 없음 |
| `Field` 계산값 점선 | **빠짐** | `#field[state="computed"]` 규칙 없음 |
| `Group` 카드 테두리 | **빠짐** | `#group` / `#groupHead` 규칙 없음 |
| `make_table` | 정상 | 파이썬에서 정렬·폰트를 직접 지정 |
| `Sparkline` / `Swatch` | 정상 | QPainter 로 직접 그림 |

오류 메시지 텍스트는 빨갛게 나오므로 정보 전달은 됩니다.
테두리까지 원하면 `view/theme.py` 의 `build_css()` 끝에 다음을 추가하세요.

```python
# view/theme.py build_css() 반환 문자열 끝에 추가
/* design-system 위젯용 */
#field {{ background:{T('CARD')}; border:1px solid {T('BORDER')};
          border-radius:5px; padding:4px 7px; color:{T('TEXT')}; }}
#field:focus {{ border:2px solid {T('ACCENT')}; padding:3px 6px; }}
#field[state="computed"] {{ background:#e3eefc; color:#075099;
                            border:1px dashed {T('ACCENT')}; }}
#field[state="bad"] {{ border:1px solid #b91c1c; }}
#group {{ background:{T('BG')}; border:1px solid {T('BORDER')};
          border-radius:6px; }}
#groupHead {{ background:{T('BAR_BG')};
              border-bottom:1px solid {T('BORDER')}; }}
#groupBody {{ background:{T('BG')}; }}
```

이 8줄만 추가하면 방식 A 로도 완전한 표현이 나옵니다.
기존 위젯에는 영향이 없습니다 (`#field` / `#group` 은 새 위젯만 쓰는 objectName).

**검증 완료:** `shots/adapter_patched.png` 가 패치 적용 후 결과입니다.
계산값 점선 테두리, 오류 빨간 테두리, Group 카드 테두리가 모두 정상 표시됩니다.
`shots/adapter.png`(패치 전)와 비교하면 차이가 보입니다.

### 방식 B — 토큰만 확장 (중간)

`theme.py`의 토큰 dict에 부족한 것을 추가하고, QSS는 기존 것을 유지합니다.

```python
# view/theme.py 의 THEMES 에 추가
"light": {
    ...기존 8개...
    "HINT":  "#78828f",   # ink3 — 3단계 보조
    "OK":    "#15803d",
    "WARN":  "#b45309",
    "CRIT":  "#b91c1c",
    "SUNK":  "#e8ebf0",   # surface3 — 눌린 상태
},
```

**장점** 이름 체계가 CrowdSim 것으로 통일됩니다.
**단점** design-system의 `stylesheet.py`는 못 씁니다 (이름이 다르므로).

### 방식 C — 전면 교체 (위험도 높음)

`theme.py`를 `tokens.py` + `stylesheet.py`로 대체합니다.

**하기 전에 반드시:**

1. 커밋되지 않은 변경 5건 정리
2. 브랜치 분리 (`git switch -c style/design-system`)
3. 적용 전 화면 스크린샷 확보 (비교용)

**작업 범위:** 실제로 손볼 곳은 34곳입니다 (95곳이 아닙니다).
`theme.py` 28개는 교체되어 사라지고, `nextlib` 33개는 건드리지 않습니다.

**QSS 커버리지 차이를 반드시 확인하세요.** CrowdSim의 `build_css()`는
design-system의 `build_qss()`가 다루지 않는 위젯을 다룹니다:

| 위젯 | CrowdSim | design-system |
|---|---|---|
| `QMenuBar` / `QMenu` | 있음 | **없음** |
| `QToolBar` / `QToolButton` | 있음 | 부분 (`#tbtn`) |
| `QStatusBar` | 있음 | **없음** |
| `QDockWidget` | 있음 | **없음** |
| `QSplitter` | 있음 | **없음** |
| `QTreeWidget` / `QListView` | 있음 | **없음** |
| `QCheckBox` / `QRadioButton` | 있음 (SVG 아이콘) | **없음** |
| `QSpinBox` 화살표 | 있음 (SVG) | **없음** |
| `QToolTip` | 있음 | **없음** |

**그대로 교체하면 위 위젯들이 OS 기본 모양으로 돌아갑니다.**
전면 교체를 택한다면 `build_qss()`에 이 규칙들을 먼저 이식해야 합니다.

---

## 4. 어느 방식이든 지킬 것

### 4.1 nextlib은 건드리지 않는다

```
lib/nextlib/**   ← 다른 프로젝트와 공유. 수정 금지
```

여기의 하드코딩 색 33개는 그대로 둡니다.
바꾸려면 nextlib 자체를 별도로 관리해야 합니다.

### 4.2 SVG 아이콘 경로에 주의

`theme.py`는 nextlib의 아이콘을 참조합니다.

```python
_ICONS = os.path.join(os.path.dirname(_nextlib.__file__), "widgets/icons")
```

체크박스·라디오·스핀박스 화살표가 이 경로의 SVG를 씁니다.
`theme.py`를 없애면 이 참조도 함께 사라지므로,
전면 교체 시 아이콘 경로를 새 stylesheet로 옮겨야 합니다.

### 4.3 setStyle("Fusion") 은 화면을 바꾼다 — 가장 주의할 항목

CrowdSim `main.py` 는 `setStyle()` 을 **호출하지 않습니다.**
즉 OS 기본 스타일(Windows 에서는 windowsvista)에서 동작 중입니다.

```python
# main.py 현재 상태 (40~42행)
app = QApplication(sys.argv)
app.setFont(QFont("Segoe UI", 10))
app.setStyleSheet(build_css())        # setStyle 없음
```

design-system 의 `apply_theme()` 은 `app.setStyle("Fusion")` 을 부릅니다.
이를 그대로 적용하면 **QSS 로 덮이지 않은 모든 위젯의 기본 모양이 한꺼번에 바뀝니다.**
체크박스, 스핀박스, 콤보박스 팝업, 다이얼로그 버튼 등이 해당합니다.

세 가지 선택지가 있습니다.

| 선택 | 결과 |
|---|---|
| `setStyle` 호출 안 함 | 현 상태 유지. 가장 안전 |
| `setStyle("Fusion")` 추가 | OS 간 일관성 확보. 단 **전면 재확인 필요** |
| 나중에 결정 | 방식 A 로 시작할 때는 부르지 않으면 됨 |

방식 A(위젯만 가져오기)를 택한다면 `apply_theme()` 을 쓰지 말고
기존 `app.setStyleSheet(build_css())` 를 그대로 두세요.

### 4.4 폰트 설정도 충돌한다

```python
main.py:41   app.setFont(QFont("Segoe UI", 10))          # CrowdSim: 10pt 고정
design-system  app.setFont(QFont(W._UI, FONT["size"]["base"]))  # 9pt
```

design-system 은 기본 9pt 이고 CrowdSim 은 10pt 입니다.
`example.py` 의 폰트 설정을 그대로 가져오면 **전체 글자 크기가 작아집니다.**

`tokens.py` 의 `FONT["size"]` 를 CrowdSim 기준으로 올리거나,
`main.py` 의 `setFont` 를 유지하고 design-system 쪽 설정을 생략하세요.

### 4.5 대비율은 색을 바꿀 때마다 검사

```bash
.venv\Scripts\python.exe design-system\tokens.py
```

WCAG AA(4.5:1) 미만이 나오면 그 색은 쓰지 않습니다.

### 4.6 되돌리는 법

진입점이 `main.py` 한 줄이므로 복구가 간단합니다.

```python
# main.py:42
app.setStyleSheet(build_css())        # 원래대로
```

---

## 5. 권장 순서

CrowdSim은 이미 동작 중인 프로젝트이므로 점진적 접근을 권합니다.

1. **커밋되지 않은 변경 5건 정리** — 스타일 작업과 섞이지 않게
2. **방식 A로 시작** — `Field`, `make_table` 만 새 화면에 써봄
3. **문제 없으면 방식 B** — 상태색(`ok`/`warn`/`crit`) 추가
4. **전면 교체는 마지막** — 그것도 QSS 커버리지를 채운 뒤에

방식 A만으로도 실익이 있습니다. `Field`의 오류 표시(색+형태+텍스트)와
`make_table`의 숫자 우측 정렬은 CrowdSim에 없는 것들입니다.

---

## 6. 참고

- 설계 원칙과 위젯 사용법: `README.md`
- 동작 확인: `.venv\Scripts\python.exe design-system\example.py`
  (CrowdSim venv 에서 정상 동작 확인 완료)
- 두 테마 비교: `shots/light.png`, `shots/dark.png`
- 방식 A 검증: `adapter_example.py` (`--show` 로 창 표시, `--shot` 으로 캡처)
- 패치 전후 비교: `shots/adapter.png` vs `shots/adapter_patched.png`

### 검증 이력

이 문서의 모든 수치와 코드는 실제 실행으로 확인했습니다.

| 항목 | 확인 방법 |
|---|---|
| 하드코딩 색 95개 분포 | `grep -rn "#[0-9a-fA-F]\{6\}"` |
| 진입점 1곳 | `grep -rn "build_css"` |
| 방식 A 어댑터 동작 | `adapter_example.py` 실행 |
| 방식 A 의 QSS 공백 | `shots/adapter.png` 육안 확인 |
| 패치 8줄의 효과 | `shots/adapter_patched.png` 육안 확인 |
| CrowdSim venv 호환 | `example.py --shot` 실행 |
