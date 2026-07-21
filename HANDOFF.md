# CrowdSim GUI 수정 작업 인계 문서

원본 이슈 리포트: `CrowdSim_GUI_수정요청.html` (2026-07-10 v2, E8ight 개발팀 브리핑).
핵심 증상: GUI에서 Open → Save/Run 하면 원본 JSON의 일부 필드가 유실되어 시나리오가 깨짐(초기 군중 0명 등).

## 완료된 작업

1. **좌측 트리 ↔ 우측 프로퍼티 패널 인덱스 불일치 수정** (`view/main/main_window_view.py`)
   - 트리에 `Zone` 항목이 없어서 `Report&Export` 클릭 시 `Zone` 패널이 열리던 버그 수정.
   - `Report&Export`를 `Report`/`Export` 두 개 탭으로 분리, 트리·프로퍼티 인덱스 0~8로 재정렬.

2. **트리 항목 더블클릭 UX** (`lib/nextlib/widgets/tree.py`, `main_window_view.py`)
   - 더블클릭 시 제목이 이름 수정(rename) 모드로 들어가던 것 방지 (`set_editable` 적용).
   - 더블클릭 시 우측 아코디언 패널이 접히도록 토글 동작 추가. 단, "닫혀있던 항목을 더블클릭"하면 그냥 열린 채로 유지되고, "이미 열려있던 항목"을 다시 더블클릭해야 접히도록 `_pending_open_index` 타이밍 로직으로 구분.

3. **`binary_path`(초기 군중 `.e8b`) 유실 수정** (`view/panel/properties/particle_view.py`)
   - GUI가 모델링 못하는 binary 타입 `particle_generation` 항목을 `_binary_passthrough`에 원본 그대로 보존 후 저장 시 재기록.

4. **근본 원인: Run/Save가 매번 빈 템플릿으로 JSON을 재생성하던 구조 수정** (`view/main/main_window_view.py`, `datarw/e8ight/solver_input.py`)
   - `save_input_file()`이 이제 기존 JSON을 먼저 로드 후, GUI가 관리하는 리스트(`grid`/`materials`/`particle_generation`/`inlet`/`outlet`/`zone`)만 초기화하고 나머지는 보존.
   - `add_result_report()`가 `export_path`/`export_format`을 로드된 값이 있으면 유지하도록 수정 (기존엔 무조건 빈 값으로 리셋).

5. **GUI가 모델링하지 않는 필드 보존(`raw_extra` 패턴)** — `grid_view.py`, `materials_view.py`, `inlet_view.py`, `outlet_view.py`, `zone_view.py`
   - 각 리스트 항목 로드 시 알려진 키 외 나머지를 `raw_extra`에 저장, 저장 시 그대로 재기록.
   - `outlet.sig_k`/`sig_x`/`settle_radius`, `initial_outlet_id`/`exit_ratio`(S5) 등 GUI에 없는 필드도 이제 유실되지 않음(단, GUI에서 직접 편집은 아직 불가 — 보존만 됨).

6. **`ExportView` 실제 연결** (`view/panel/properties/export_view.py`, `main_window_view.py`)
   - 기존엔 `main_window_view.py`에 아예 인스턴스화도 안 되던 죽은 코드였음. 이제 `Export` 탭으로 정식 노출.
   - "내보내기(동영상)" → 기존 애니메이션 바의 `_anim_export_video()` 재사용.
   - "내보내기(이미지)" → 프레임 범위를 PNG 시퀀스로 저장하는 기능 신규 구현.

7. **Zone 패널** — 이번 작업 이전부터 진행 중이던 미커밋 파일(`zone_view.py`/`zone.ui`/`zone_ui.py`)이 이미 존재했고 정상 동작 확인. 그대로 유지.

## 남은 작업 (우선순위 순)

- **"해석 결과 내보내기" 버튼 미구현** (`export_view.py`의 `groupBox_4`, `pushButton`) — 시작/종료 시간(초) 기준으로 뭘 내보내야 하는지(어떤 파일 형식, 어느 폴더로) 확인 필요. 추측 구현 시 오히려 잘못될 위험이 있어 보류.
- **`items`/`flags` 키 스키마 정합 불확실** — `solver_input.py`의 `add_result_report()`에 `"restDensity": True,  # "rest_density": True,` 라는 주석이 이미 있음. 실제 서버(RuntimeSPH2D.exe)가 camelCase/snake_case 중 뭘 기대하는지 서버 스키마 문서나 실제 실행 로그로 확인 필요.
- **`outlet.sig_k`/`sig_x`/`settle_radius`, `initial_outlet_id`/`exit_ratio`(S5) GUI 편집 UI 없음** — 지금은 보존만 됨. 실제로 GUI에서 값을 만들거나 수정하려면 `outlet.ui`/`outlet_ui.py`에 입력 필드 추가 필요.
- **`particle_view.py`의 binary 항목도 편집 UI 없음** — 보존만 되고, GUI에서 새 binary 항목을 만들거나 기존 값을 수정하는 화면은 없음.
- **P3: 프로젝트 폴더 표준화** — `stl/`·`initial/` 하위 폴더에 에셋을 정리해서 배치하는 규칙. 손댄 적 없음.
- **뷰포트 STL 미리보기** — 입력 탭에서 STL 벽/field 형상이 렌더링되지 않음(현재는 시뮬레이션 실행 후 결과로만 표시됨). VTK 액터 추가가 필요한 큰 작업.
- **mesh "Select" 버튼** — 경로 텍스트만 채우고, "세그먼트 저장/추가"를 눌러야 실제 반영됨. 라벨과 동작이 다르다는 지적이 있었음(기능 자체는 정상, UX 개선 여지).

## 참고

- 이 저장소는 `origin` (`https://github.com/thisisHenney/CrowdSim.git`)에 연결되어 있음.
- 이어서 작업할 때는 이 문서를 먼저 읽고, 필요하면 `git log`로 실제 커밋된 변경 이력을 함께 확인할 것.
