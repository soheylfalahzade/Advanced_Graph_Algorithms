import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance

def generate_points(n=20):
    """تولید نقاط تصادفی"""
    return np.random.rand(n, 2) * 100

def compute_greedy_spanner(points, t=2.0):
    """الگوریتم حریصانه برای ساخت اسپانر با ضریب کشش T"""
    n = len(points)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    
    # ۱. تولید تمام یال‌های ممکن و محاسبه طول آن‌ها
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.linalg.norm(points[i] - points[j])
            edges.append((i, j, dist))
    
    # ۲. مرتب‌سازی یال‌ها بر اساس طول (حریصانه)
    edges.sort(key=lambda x: x[2])
    print(f"🛤️ Total potential edges: {len(edges)}")

    # ۳. بررسی شرط اسپانر برای هر یال
    for u, v, weight in edges:
        # اگر مسیری وجود داشت، طول کوتاه‌ترین مسیر فعلی را پیدا کن
        try:
            shortest_path = nx.shortest_path_length(G, source=u, target=v, weight='weight')
        except nx.NetworkXNoPath:
            shortest_path = float('inf')
        
        # شرط اصلی اسپانر: اگر مسیر فعلی خیلی طولانی‌تر از (t * وزن یال) بود، یال را اضافه کن
        if shortest_path > t * weight:
            G.add_edge(u, v, weight=weight)
            
    print(f"✅ Spanner construction finished with {G.number_of_edges()} edges.")
    return G

def plot_spanner(points, G, t):
    """نمایش گراف نهایی"""
    plt.figure(figsize=(10, 10))
    pos = {i: points[i] for i in range(len(points))}
    
    # رسم یال‌ها
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5)
    # رسم نقاط
    plt.scatter(points[:, 0], points[:, 1], color='red', s=50, zorder=5)
    
    for i, p in enumerate(points):
        plt.annotate(str(i), (p[0] + 1, p[1] + 1))
        
    plt.title(f"Greedy Spanner (t={t}) | Edges: {G.number_of_edges()}")
    plt.grid(True)
    plt.savefig('greedy_spanner_result.png')
    print("🖼️ Final result saved as 'greedy_spanner_result.png'")
    plt.show()

if __name__ == "__main__":
    n_points = 20
    stretch_factor = 2.0  # ضریب کشش (t)
    
    my_points = generate_points(n_points)
    spanner_graph = compute_greedy_spanner(my_points, t=stretch_factor)
    
    plot_spanner(my_points, spanner_graph, stretch_factor)