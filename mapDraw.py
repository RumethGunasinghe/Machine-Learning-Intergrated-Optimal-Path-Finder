import folium
# from Classes.Graph import Graph
def draw_interactive_map(nodes,path=None, file_path="empty_map.html"):
    # Center the map on the first node
    start_lat = nodes[0].latitude + 0.001223
    start_lon = nodes[0].longitude + 0.001217
    fmap = folium.Map(location=[start_lat, start_lon], zoom_start=15)

    # Add nodes and edges
    for node in nodes:
        folium.Marker([node.latitude + 0.001223, node.longitude + 0.001217], icon=folium.DivIcon(html=f'<div style="width:30px;height:30px;border-radius:50%;background:#2A81CB;color:white;display:flex;align-items:center;justify-content:center;font-size:10pt;">{node.id}</div>')).add_to(fmap)
        
        for location in node.locations: ##will show the actual camera location. helps with confirming the roads with no trafffic details
            folium.CircleMarker(location=[location.latitude + 0.00153, location.longitude + 0.0013], radius=8, color='blue', fill=True, fill_color='blue').add_to(fmap)
        
        # Draw connections to neighbours
        for neighbour in node.neighbours:
            if neighbour is not None:
                line = folium.PolyLine(
                    locations=[
                        [node.latitude+ 0.001223, node.longitude + 0.001217],
                        [neighbour.latitude + 0.001223, neighbour.longitude + 0.001217]
                    ],
                    color='black',
                    weight=2
                )
                line.add_to(fmap)
    if path:
        for i in range(len(path) -1):
            line = folium.PolyLine(
                locations=[
                    [path[i].latitude+ 0.001223, path[i].longitude + 0.001217],
                    [path[i+1].latitude + 0.001223, path[i+1].longitude + 0.001217]
                ],
                color='red',
                weight=5
            )
            line.add_to(fmap)



    # Save map to file
    fmap.save(file_path)
    print(f"Map saved to {file_path}")


# grapgObj = Graph()
# draw_interactive_map(grapgObj.nodes)


# node970 = next((n for n in grapgObj.nodes if n.id == 970), None)  #only node 970 is located on HIGH STREET_ROAD and it converts into HIGH_ST inbetween 970 and 2846. they wont be recognized as neighbours even though they are in tthe same road since the road names are different for both nodes. 
# for location in node970.locations:
#     print(f" {location.name} ")

