"""Kruskal 알고리즘으로 최소 신장 트리를 만드는 실행 예제."""

import pyvisalgo as va


def getRoot(vertex):
    """부모를 따라 재귀 호출하여 루트를 찾고, 배열을 바꾸지 않고 반환한다."""
    vis.root_enter(vertex, roots)
    # 자기 자신을 가리키면 더 따라갈 부모가 없습니다.
    # 자기 자신을 반환하는 것이 재귀 호출의 종료 조건입니다.
    if roots[vertex] == vertex:
        vis.root_return(vertex, vertex, roots, is_root=True)
        return vertex
    # 루트가 아니면 부모 정점의 루트를 다시 묻습니다.
    # 예를 들어 3 -> 2 -> 1 -> 0이면 getRoot(0)에서 0을 반환하고,
    # 기다리던 getRoot(1), getRoot(2), getRoot(3)도 차례로 0을 반환합니다.
    root = getRoot(roots[vertex])
    vis.root_return(vertex, root, roots, shortcut=False)
    # 지금은 반환만 합니다. roots[vertex]를 바꾸는 경로 압축은 나중에 추가합니다.
    return root


def union(root_u, root_v):
    """서로 다른 두 집합의 대표를 받아 하나의 집합으로 합친다."""
    # 일반 정점이 아니라 getRoot가 반환한 대표끼리 연결해야 합니다.
    # 대표가 아닌 정점의 부모만 바꾸면 기존 집합의 일부만 옮겨질 수 있습니다.
    # 작은 번호를 대표로 남기는 것은 집합을 관리하는 규칙일 뿐,
    # 간선의 가중치가 작거나 MST의 비용이 더 작다는 뜻은 아닙니다.
    if root_u < root_v:
        roots[root_v] = root_u
    else:
        roots[root_u] = root_v
    vis.union_roots(root_u, root_v, roots)


def kruskal(count, edges):
    """정점 수와 간선 목록을 받아 (선택한 간선 목록, 비용 합)을 반환한다."""
    global roots
    # 정점 번호는 0부터 count - 1까지입니다.
    # 각 간선 (u, v, weight)는 두 정점과 연결 비용을 나타냅니다.
    # 무방향 간선이므로 (v, u, weight)를 다시 저장하지 않습니다.
    # 아직 선택한 간선이 없으므로 빈 목록과 비용 0에서 시작합니다.
    # mst에는 선택한 간선을, total_cost에는 그 가중치 합을 저장합니다.
    mst = []
    total_cost = 0

    # 처음에는 간선을 선택하지 않았으므로 각 정점이 독립된 집합입니다.
    # 자기 자신을 가리키는 정점이 집합의 대표(루트)입니다.
    # 이후 getRoot와 union에서 함께 사용할 수 있도록 전역 배열로 준비합니다.
    # 이 부모 관계는 집합 관리용이며, 실제 선택 간선 목록인 mst와는 다릅니다.
    roots = [i for i in range(count)]
    vis.start(roots)

    # 간선의 세 번째 값인 weight를 기준으로 오름차순 정렬합니다.
    # sorted는 새 목록을 만들므로 원본 데이터의 간선 순서는 바뀌지 않습니다.
    # 같은 가중치를 가진 간선끼리는 원래 입력 순서가 유지됩니다.
    edges = sorted(edges, key=lambda edge: edge[2])
    vis.sort_edges(edges)

    # 가중치가 작은 순서대로 모든 후보를 검사합니다.
    # for문에서 각 간선의 두 끝점과 가중치를 나누어 받습니다.
    # 정점 n개의 사이클 없는 그래프는 간선이 최대 n-1개입니다.
    # 무조건 선택하는 대신 두 대표를 비교해 같은 집합의 간선은 제외합니다.
    # 제외한 후보도 검사 횟수에는 포함되므로, 앞의 count개만 보면 부족할 수 있습니다.
    # 선택한 간선이 count-1개가 되면 모든 정점이 연결되므로 검사를 끝냅니다.
    for u, v, weight in edges:
        if vis.stopped():
            break
        vis.begin_edge(u, v)
        # 현재 후보의 양 끝점이 각각 어느 집합에 속하는지 대표를 구합니다.
        # 이전에 선택한 간선에 따른 집합 합치기가 이 탐색 결과에 반영됩니다.
        root_u = getRoot(u)
        root_v = getRoot(v)
        vis.check_roots(u, v, root_u, root_v, roots)
        # 두 대표가 같으면 선택한 간선들로 이미 연결된 두 정점입니다.
        # 여기에 간선을 더하면 사이클이 생기므로 목록과 비용에 반영하지 않습니다.
        if root_u == root_v:
            vis.reject_edge(u, v, weight)
            continue
        # 선택한 간선은 두 끝점과 가중치를 함께 기록합니다.
        # 서로 다른 집합을 잇는 간선만 선택하고 비용을 누적합니다.
        mst.append((u, v, weight))
        # 선택을 확정한 간선의 가중치만 총비용에 더합니다.
        total_cost += weight
        vis.select_edge(u, v, weight, total_cost)
        # 간선을 확정한 뒤 두 집합을 합쳐 다음 간선의 사이클 검사에 반영합니다.
        # 이 호출이 없으면 이미 연결한 두 정점도 다른 집합으로 잘못 판단합니다.
        union(root_u, root_v)
        # 사이클 없이 정점 n개를 연결하는 트리의 간선은 n-1개입니다.
        # 검사 횟수가 아니라 실제 선택한 간선 수로 완료 여부를 판단합니다.
        # 이후의 후보는 더 검사하지 않아도 됩니다.
        if len(mst) == count - 1:
            break

    return mst, total_cost


if __name__ == "__main__":
    vis = va.visualizer("kruskal")
    while va.running():
        data = va.next_data(__file__)
        count = len(data.vertices)
        print("정점 수:", count)
        print("간선 목록:", data.edges)
        # positions는 그림을 배치하는 좌표일 뿐입니다.
        # Kruskal은 선의 화면상 길이가 아니라 weight를 비교합니다.
        vis.setup(data)
        mst, total_cost = kruskal(count, data.edges)
        # 연결된 그래프라면 MST가, 연결되지 않았다면 각 연결 요소의 신장 트리가 남습니다.
        print("선택한 간선:", mst)
        print("현재 비용:", total_cost)
        # 정점 드래그: 배치 변경, 빈 곳 드래그: 화면 이동, 휠: 확대/축소.
        # H: 설명 숨김, L: 배치 전환, R: 재실행, D: 다음 데이터, Esc: 종료.
        vis.wait()
