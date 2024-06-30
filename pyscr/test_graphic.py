import javalang
import os
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

def parse_java_file(file_path):
    """ Parse a Java file to get the method calls. """
    with open(file_path, 'r') as file:
        source_code = file.read()
    tree = javalang.parse.parse(source_code)
    return tree

def get_method_calls(tree, class_name):
    """ Extract method calls from the AST. """
    method_calls = []

    for _, node in tree.filter(javalang.tree.MethodDeclaration):
        current_method = f"{class_name}.{node.name}"
        for path, child in node:
            if isinstance(child, javalang.tree.MethodInvocation):
                target_class = child.qualifier if child.qualifier else class_name
                method_name = child.member
                call_type = "M"  # 기본 호출 유형을 invokevirtual로 가정

                # Static method calls는 qualifier가 있는 경우로 식별
                if child.qualifier:
                    call_type = "S"

                method_calls.append((call_type, current_method, f"{target_class}.{method_name}"))

    return method_calls

def write_method_calls(output_file, method_calls):
    """ Write method calls to the output file with the specified format. """
    with open(output_file, 'w') as f:
        for call_type, current_method, target_class_method in method_calls:
            f.write(f"{call_type}:{current_method} {target_class_method}\n")

def read_method_calls(file_path):
    """ Read method calls from the specified file. """
    method_calls = []
    with open(file_path, 'r') as file:
        for line in file:
            call_type, rest = line.split(":", 1)
            current_method, target_method = rest.rsplit(None, 1)
            method_calls.append((call_type, current_method, target_method))
    return method_calls

def split_method_name(method_name):
    """ Split method name at uppercase letters to create a two-line label. """
    return ''.join([f"\n{char}" if char.isupper() else char for char in method_name]).strip('\n')

def filter_method_calls(method_calls, filter_class):
    """ Filter method calls to include only those involving the specified class and remove class names. """
    filtered_calls = []
    for call_type, current_method, target_method in method_calls:
        if filter_class in current_method or filter_class in target_method:
            # Remove class name from methods and split method name for better readability
            current_method_name = split_method_name(current_method.split('.')[-1])
            target_method_name = split_method_name(target_method.split('.')[-1])
            filtered_calls.append((call_type, current_method_name, target_method_name))
    return filtered_calls

def build_call_graph(method_calls):
    """ Build a call graph using NetworkX. """
    G = nx.DiGraph()
    for call_type, current_method, target_method in method_calls:
        G.add_edge(current_method, target_method, call_type=call_type)
    return G

def draw_call_graph(G):
    """ Draw the call graph using Matplotlib. """
    pos = graphviz_layout(G, prog='dot')  # 'dot' layout for top-down hierarchy
    edge_labels = nx.get_edge_attributes(G, 'call_type')
    
    plt.figure(figsize=(20, 12))  # 가로로 넓게 설정
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=12, font_weight="bold", edge_color="gray")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Filtered Call Graph")
    plt.savefig("call_graph.png")  # 그래프를 파일로 저장
    plt.close()

def main():
    java_files_path = './christmas'
    output_file = 'cfg_method_calls.txt'
    filter_class = 'EventControl'  # 특정 클래스

    method_calls = []

    # 모든 자바 파일 파싱
    for root, _, files in os.walk(java_files_path):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                tree = parse_java_file(file_path)
                class_name = os.path.splitext(file)[0]  # 파일 이름에서 클래스 이름 가져오기
                method_calls.extend(get_method_calls(tree, class_name))

    # 필터링된 호출 관계 저장
    write_method_calls(output_file, method_calls)
    
    # 텍스트 파일에서 호출 관계 읽기
    all_method_calls = read_method_calls(output_file)
    
    # 특정 클래스에 대한 호출 관계 필터링
    filtered_calls = filter_method_calls(all_method_calls, filter_class)
    
    # 호출 그래프 생성
    call_graph = build_call_graph(filtered_calls)
    
    # 호출 그래프 그리기
    draw_call_graph(call_graph)

if __name__ == "__main__":
    main()