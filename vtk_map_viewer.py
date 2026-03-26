"""VTK 파일의 포인트를 지도 이미지 위에 표시하는 스크립트"""
import struct
import os
import glob
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


# === 설정 ===
VTK_DIR = r"C:\Users\thisi\OneDrive\바탕 화면\TestCase\CrwodSim\8\E8ight\8"
MAP_IMAGE = r"D:\projects\2024-01_MCST_Crowd\2.Src\GUI\CrowdSim\resource\map\nanji_drawing_new.jpg"

# Domain (JSON config 기준)
DOMAIN_MIN = [-155.0, -125.0]
DOMAIN_MAX = [210.0, 165.0]


def read_vtk_points(filepath):
    """바이너리 VTK 파일에서 포인트 좌표를 읽는다."""
    with open(filepath, 'rb') as f:
        # 헤더 5줄 읽기
        for _ in range(4):
            f.readline()
        points_line = f.readline().decode('ascii').strip()
        num_points = int(points_line.split()[1])

        # big-endian float * (num_points * 3)
        data = f.read(num_points * 3 * 4)
        values = struct.unpack(f'>{num_points * 3}f', data)

        points = np.array(values).reshape(num_points, 3)
        return points[:, :2]  # x, y만 반환


def get_vtk_files(directory):
    """디렉토리에서 VTK 파일 목록을 번호 순으로 정렬하여 반환."""
    pattern = os.path.join(directory, "*.vtk")
    files = glob.glob(pattern)
    # 파일명에서 숫자 추출하여 정렬
    def sort_key(f):
        name = os.path.splitext(os.path.basename(f))[0]
        num = name.rsplit('_', 1)[-1]
        return int(num)
    files.sort(key=sort_key)
    return files


def plot_on_map(vtk_file, map_img, ax, domain_min, domain_max):
    """VTK 포인트를 지도 위에 표시."""
    ax.clear()

    img_h, img_w = map_img.shape[:2]

    # 지도 이미지를 도메인 좌표계에 맞춰 표시
    ax.imshow(map_img, extent=[domain_min[0], domain_max[0],
                                domain_min[1], domain_max[1]],
              aspect='equal', origin='upper')

    # VTK 포인트 읽기
    points = read_vtk_points(vtk_file)

    if len(points) == 0:
        ax.set_title(os.path.basename(vtk_file))
        return

    xs, ys = points[:, 0], points[:, 1]

    # 점 표시
    ax.scatter(xs, ys, c='red', s=8, zorder=5, edgecolors='darkred', linewidths=0.3)

    # 각 점 아래에 픽셀 좌표 출력
    for x, y in zip(xs, ys):
        # 도메인 좌표 -> 픽셀 좌표 변환
        px = (x - domain_min[0]) / (domain_max[0] - domain_min[0]) * img_w
        py = (1.0 - (y - domain_min[1]) / (domain_max[1] - domain_min[1])) * img_h
        ax.annotate(f'({int(px)},{int(py)})',
                    xy=(x, y), xytext=(0, -8),
                    textcoords='offset points',
                    fontsize=4, color='yellow',
                    ha='center', va='top',
                    bbox=dict(boxstyle='round,pad=0.1', fc='black', alpha=0.5, lw=0))

    ax.set_xlim(domain_min[0], domain_max[0])
    ax.set_ylim(domain_min[1], domain_max[1])
    ax.invert_yaxis()
    ax.set_title(os.path.basename(vtk_file), fontsize=10)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')


def main():
    vtk_files = get_vtk_files(VTK_DIR)
    if not vtk_files:
        print("VTK 파일을 찾을 수 없습니다.")
        return

    map_img = mpimg.imread(MAP_IMAGE)

    # 도메인 비율에 맞는 figure 크기 계산
    domain_w = DOMAIN_MAX[0] - DOMAIN_MIN[0]  # 365
    domain_h = DOMAIN_MAX[1] - DOMAIN_MIN[1]  # 290
    fig_w = 14
    fig_h = fig_w * domain_h / domain_w

    fig, ax = plt.subplots(1, 1, figsize=(fig_w, fig_h))
    fig.tight_layout(pad=2)

    # 첫 번째 파일 표시
    current_idx = [0]
    plot_on_map(vtk_files[current_idx[0]], map_img, ax, DOMAIN_MIN, DOMAIN_MAX)

    def on_key(event):
        if event.key == 'right':
            current_idx[0] = min(current_idx[0] + 1, len(vtk_files) - 1)
        elif event.key == 'left':
            current_idx[0] = max(current_idx[0] - 1, 0)
        elif event.key == 'home':
            current_idx[0] = 0
        elif event.key == 'end':
            current_idx[0] = len(vtk_files) - 1
        else:
            return
        plot_on_map(vtk_files[current_idx[0]], map_img, ax, DOMAIN_MIN, DOMAIN_MAX)
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('key_press_event', on_key)

    print(f"VTK 파일 {len(vtk_files)}개 로드됨")
    print("좌우 화살표: 이전/다음 프레임, Home/End: 처음/마지막")
    plt.show()


if __name__ == '__main__':
    main()
