# CrowdSim GUI 수정 작업 인계 문서

원본 이슈 리포트: `CrowdSim_GUI_수정요청.html` (2026-07-10 v2, E8ight 개발팀 브리핑).
핵심 증상: GUI에서 Open → Save/Run 하면 원본 JSON의 일부 필드가 유실되어 시나리오가 깨짐(초기 군중 0명 등).

이 문서는 여러 시스템(여러 Claude Code 세션)에서 이어서 작업하기 위한 인계 문서입니다.
작업을 이어받으면 먼저 `git log --oneline -10` 으로 실제 커밋 이력을 확인하세요 — 아래 목록은
`804d981` (2026-07-22 기준) 시점까지 반영되어 있습니다.

## 완료된 작업

1. **좌측 트리 ↔ 우측 프로퍼티 패널 인덱스 불일치 수정** (`view/main/main_window_view.py`)
   - 트리에 `Zone` 항목이 없어서 `Report&Export` 클릭 시 `Zone` 패널이 열리던 버그 수정.
   - `Report&Export`를 `Report`/`Export` 두 개 탭으로 분리, 트리·프로퍼티 인덱스 0~8로 재정렬.

2. **트리/프로퍼티 패널 클릭·더블클릭 UX** (`lib/nextlib/widgets/tree.py`, `lib/nextlib/widgets/dropdown.py`, `main_window_view.py`)
   - 더블클릭 시 제목이 이름 수정(rename) 모드로 들어가던 것 방지.
   - 단일 클릭 = 해당 패널을 뷰포트 맨 위로 스크롤만 함(강제로 열지 않음). 더블클릭 = 해당 패널의
     실제 열림/닫힘 상태를 보고 토글. 아코디언 헤더 버튼 자체의 더블클릭(체크 가능한 버튼이라 클릭마다
     토글되어 열렸다가 바로 닫히는 깜빡임 문제)은 `doubleClickInterval()` 만큼 지연시켜 두 번째 클릭이
     오면 이전 토글을 무효화하는 방식으로 `DropDownItemWidget` 안에서 근본 해결.
   - 트리 다중 선택(2개 이상) 시 선택된 항목들의 패널만 보이고 나머지는 숨김.
   - `DropDown`에 하단 패딩을 추가해 스크롤이 부족해서 항목을 맨 위까지 못 올리는 문제 해결.

3. **`binary_path`(초기 군중 `.e8b`) 유실 수정** (`view/panel/properties/particle_view.py`)
   - GUI가 모델링 못하는 binary 타입 `particle_generation` 항목을 `_binary_passthrough`에 원본 그대로
     보존 후 저장 시 재기록.
   - (후속 수정) binary passthrough 항목과 일반 도메인 항목을 같은 리스트 인덱스로 잘못 써서 서로
     덮어쓰던 버그 수정 — 이제 `offset = len(passthrough)`를 더한 인덱스로 씀.

4. **근본 원인: Run/Save가 매번 빈 템플릿으로 JSON을 재생성하던 구조 수정** (`main_window_view.py`, `solver_input.py`)
   - `save_input_file()`이 이제 기존 JSON을 먼저 로드 후, GUI가 관리하는 리스트(`grid`/`materials`/
     `particle_generation`/`inlet`/`outlet`/`zone`)만 초기화하고 나머지는 보존.
   - `add_result_report()`가 `export_path`/`export_format`을 로드된 값이 있으면 유지.

5. **GUI가 모델링하지 않는 필드 보존(`raw_extra` 패턴)** — `grid_view.py`, `materials_view.py`,
   `inlet_view.py`, `outlet_view.py`, `zone_view.py`, `report_view.py`
   - 각 항목 로드 시 알려진 키 외 나머지를 `raw_extra`(report는 `_raw_extra_items`/`_raw_extra_flags`)에
     저장, 저장 시 그대로 재기록.
   - `outlet.sig_k`/`sig_x`/`settle_radius`, `initial_outlet_id`/`exit_ratio`(S5) 등 GUI에 없는 필드도
     이제 유실되지 않음(단, GUI에서 직접 편집은 아직 불가 — 보존만 됨).
   - `grid`의 `add_grid()`가 매번 고정된 한국어 comment로 기존 값을 덮어쓰던 것도 raw_extra로 대체.

6. **`result_report`의 `items`/`flags` 스키마를 실제 솔버 기준으로 교체** (`solver_input.py`,
   `report_ui.py`, `report_view.py`) — ✅ 이전에 불확실하다고 남겨뒀던 항목, 실제 E8ight S1~S5
   테스트 JSON으로 확인 완료.
   - 예전(GUI 자체 추측) 스키마: `restDensity`, `adjoint`, `prt_idx`, `acceleration_collision`,
     `path_goal_point` 등 — 실제 RuntimeSPH2D가 쓰는 게 아니었음.
   - 실제 스키마로 교체: `items`에 `rest_density`/`zone_id`/`outlet_id`/`path_field_id`/
     `path_direction`/`path_direction_array`/`final_path_vector` 등, `flags`에 `zone`/`solid`/`path_solid`.
   - 이 스키마에도 없는 미지 키는 raw_extra로 보존.

7. **`ExportView` 실제 연결** (`export_view.py`, `main_window_view.py`)
   - 기존엔 인스턴스화도 안 되던 죽은 코드였음. 이제 `Export` 탭으로 정식 노출.
   - "내보내기(동영상)" → 기존 애니메이션 바의 `_anim_export_video()` 재사용.
   - "내보내기(이미지)" → 프레임 범위를 PNG 시퀀스로 저장.
   - "내보내기"(해석 결과, groupBox_4) → ✅ 구현 완료. 프레임 범위에 해당하는 결과 폴더의 원본 VTK
     파일들을 사용자가 고른 폴더로 복사.

8. **Zone 패널** — 정상 동작 확인, 그대로 유지.

9. `requirements.txt`에 `pyinstaller` 추가 (배포용 빌드 대비, 버그 수정과는 무관).

## 남은 작업

- **`outlet.sig_k`/`sig_x`/`settle_radius`, `initial_outlet_id`/`exit_ratio`(S5) GUI 편집 UI 없음** —
  지금은 raw_extra로 보존만 됨. GUI에서 새로 만들거나 값을 수정하려면 `outlet.ui`/`outlet_ui.py`에
  입력 필드 추가 필요.
- **`particle_view.py`의 binary 항목도 편집 UI 없음** — 보존만 되고, GUI에서 새 binary 항목을 만들거나
  기존 값을 수정하는 화면은 없음.
- **P3: 프로젝트 폴더 표준화** — `stl/`·`initial/` 하위 폴더에 에셋을 정리해서 배치하는 규칙. 손댄 적 없음.
- **뷰포트 STL 미리보기** — 입력 탭에서 STL 벽/field 형상이 렌더링되지 않음(현재는 시뮬레이션 실행 후
  결과로만 표시됨). VTK 액터 추가가 필요한 큰 작업.
- **mesh "Select" 버튼** — 경로 텍스트만 채우고, "세그먼트 저장/추가"를 눌러야 실제 반영됨. 라벨과 동작이
  다르다는 지적이 있었음(기능 자체는 정상, UX 개선 여지).

## 참고

- 이 저장소는 `origin` (`https://github.com/thisisHenney/CrowdSim.git`)에 연결되어 있음.
- 여러 시스템에서 동시에 작업 중이므로, 작업 시작 전 항상 `git fetch && git status`로 원격이 앞서
  있는지 먼저 확인하고 `git merge --ff-only origin/main`(또는 `git pull`)으로 동기화할 것.
- 이어서 작업할 때는 이 문서를 먼저 읽고, 필요하면 `git log`/`git show <hash>`로 실제 커밋된 변경
  이력을 함께 확인할 것.
