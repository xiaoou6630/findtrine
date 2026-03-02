import nbtlib
import os
import uuid
import argparse

def ints_to_uuid(ints):
    """将四个 int 转换为标准 UUID 字符串"""
    if len(ints) != 4:
        return None
    a, b, c, d = ints
    a_u = a & 0xFFFFFFFF
    b_u = b & 0xFFFFFFFF
    c_u = c & 0xFFFFFFFF
    d_u = d & 0xFFFFFFFF
    high = (a_u << 32) | b_u
    low = (c_u << 32) | d_u
    full = (high << 64) | low
    return str(uuid.UUID(int=full))

def parse_bogey_points(bogey, graph_nodes):
    """从 Bogey 解析轮子坐标"""
    points = bogey.get('Points', [])
    results = []
    
    for pi, point in enumerate(points):
        position = point.get('Position', 0)
        nodes = point.get('Nodes', [])
        
        if len(nodes) >= 2:
            node1 = nodes[0]
            node2 = nodes[1]
            
            x1, y1, z1 = node1.get('X', 0), node1.get('Y', 0), node1.get('Z', 0)
            x2, y2, z2 = node2.get('X', 0), node2.get('Y', 0), node2.get('Z', 0)
            dim = node1.get('D', 0)
            
            dim_names = {0: 'minecraft:overworld', -1: 'minecraft:the_nether', 1: 'minecraft:the_end'}
            dim_name = dim_names.get(dim, f'dimension_{dim}')
            
            t = position / 100.0 if position != 0 else 0
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            z = z1 + (z2 - z1) * t
            
            results.append({
                'point_index': pi,
                'position': position,
                'coordinates': (x, y, z),
                'dimension': dim_name,
                'node1': (x1, y1, z1),
                'node2': (x2, y2, z2)
            })
    
    return results

def extract_train_name(train_tag):
    """提取列车名称"""
    name = train_tag.get('Name', train_tag.get('name', 'Unnamed'))
    if isinstance(name, str):
        # 尝试解析JSON格式的字符串
        try:
            import json
            parsed = json.loads(name)
            if isinstance(parsed, dict) and 'text' in parsed:
                return parsed['text']
        except:
            pass
        return name
    elif isinstance(name, nbtlib.tag.Compound) and 'text' in name:
        return str(name['text'])
    elif isinstance(name, nbtlib.tag.String):
        name_str = str(name)
        try:
            import json
            parsed = json.loads(name_str)
            if isinstance(parsed, dict) and 'text' in parsed:
                return parsed['text']
        except:
            pass
        return name_str
    return str(name)

def search_trains_in_file(filepath):
    """从单个文件中搜索列车"""
    if not os.path.exists(filepath):
        print(f"错误: 文件 {filepath} 不存在")
        return []
    
    all_trains = []
    
    try:
        data = nbtlib.load(filepath)
    except Exception as e:
        print(f"错误: 无法加载文件 {filepath}: {e}")
        return []
    
    graphs = []
    if 'data' in data and 'RailGraphs' in data['data']:
        graphs = data['data']['RailGraphs']
    elif 'RailGraphs' in data:
        graphs = data['RailGraphs']
    elif 'graphs' in data:
        graphs = data['graphs']
    elif 'railways' in data and 'graphs' in data['railways']:
        graphs = data['railways']['graphs']
    
    def collect_trains(tag, path):
        if isinstance(tag, nbtlib.tag.List):
            for i, item in enumerate(tag):
                collect_trains(item, f"{path}[{i}]")
        elif isinstance(tag, nbtlib.tag.Compound):
            id_key = None
            if 'Id' in tag:
                id_key = 'Id'
            elif 'id' in tag:
                id_key = 'id'
            
            if id_key and ('Carriages' in tag or 'carriages' in tag):
                name = extract_train_name(tag)
                carriages = tag.get('Carriages', tag.get('carriages', []))
                
                train_info = {
                    'name': name,
                    'path': path,
                    'tag': tag,
                    'carriages': carriages,
                    'graphs': graphs
                }
                all_trains.append(train_info)
            
            for key, value in tag.items():
                collect_trains(value, f"{path}.{key}")
    
    collect_trains(data, "")
    return all_trains

def format_train_info(train_info):
    """格式化列车信息为字符串"""
    result = []
    result.append(f"=== 列车: {train_info['name']} ===")
    result.append(f"路径: {train_info['path']}")
    
    carriages = train_info['carriages']
    graphs = train_info['graphs']
    
    for ci, carriage in enumerate(carriages):
        result.append(f"\n  车厢 {ci+1}:")
        
        # 尝试获取驾驶台坐标
        conductor_pos = None
        conductor_dim = None
        
        if 'Entity' in carriage:
            entity = carriage['Entity']
            if 'Pos' in entity:
                pos = entity['Pos']
                if len(pos) >= 3:
                    conductor_pos = (float(pos[0]), float(pos[1]), float(pos[2]))
            
            # 从 EntityPositioning 获取维度
            if 'EntityPositioning' in carriage and len(carriage['EntityPositioning']) > 0:
                entity_pos = carriage['EntityPositioning'][0]
                if 'Dim' in entity_pos:
                    dim = int(entity_pos['Dim'])
                    dim_names = {0: 'minecraft:overworld', 1: 'minecraft:the_nether', 2: 'minecraft:the_end'}
                    conductor_dim = dim_names.get(dim, f'dimension_{dim}')
        
        # 如果找到驾驶台坐标，显示它
        if conductor_pos:
            x, y, z = conductor_pos
            dim_str = f" 维度 {conductor_dim}" if conductor_dim else ""
            result.append(f"    驾驶台坐标: ({x:.2f}, {y:.2f}, {z:.2f}){dim_str}")
        else:
            # 如果没有驾驶台，显示轮子坐标
            for bogey_name in ['FirstBogey', 'SecondBogey', 'LeadingBogey', 'TrailingBogey']:
                if bogey_name not in carriage:
                    continue
                bogey = carriage[bogey_name]
                points = parse_bogey_points(bogey, graphs)
                
                for pi, point_data in enumerate(points):
                    x, y, z = point_data['coordinates']
                    dim = point_data['dimension']
                    result.append(f"    {bogey_name}.Point[{pi}]: 坐标 ({x:.2f}, {y:.2f}, {z:.2f}) 维度 {dim}")
    
    result.append("\n" + "="*50)
    return "\n".join(result)

def main():
    parser = argparse.ArgumentParser(description="机械动力列车位置查询工具")
    parser.add_argument('--file', '-f', default='E:\\daima\\findtrine\\create_tracks.dat', 
                        help='机械动力列车存档文件路径 (默认: E:\\daima\\findtrine\\create_tracks.dat)')
    parser.add_argument('--name', '-n', default='', 
                        help='列车名称搜索关键词 (留空显示全部)')
    
    args = parser.parse_args()
    filepath = args.file
    search_name = args.name.strip()
    
    print(f"正在读取文件: {filepath}")
    all_trains = search_trains_in_file(filepath)
    
    if not all_trains:
        print("未找到任何列车。")
        return
    
    matched_trains = []
    if search_name:
        for train in all_trains:
            train_name = train['name'].lower()
            if search_name.lower() in train_name:
                matched_trains.append(train)
    else:
        matched_trains = all_trains
    
    if not matched_trains:
        print(f"未找到名称包含 '{search_name}' 的列车。")
        return
    
    print(f"共找到 {len(matched_trains)} 个列车：\n")
    
    for train in matched_trains:
        print(format_train_info(train))

if __name__ == "__main__":
    main()
